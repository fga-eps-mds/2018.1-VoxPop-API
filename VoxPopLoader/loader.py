import datetime
import json
import logging
import logging.config
import socketserver
import sys
import time
import xml.etree.ElementTree as ET
from base64 import b64encode

import requests


logging.config.fileConfig('logging.conf')

logger = logging.getLogger('VoxPopLoader')

# logger.debug('debug message')
# logger.info('info message')
# logger.warn('warn message')
# logger.error('error message')
# logger.critical('critical message')


class VoxPopLoader():
    """docstring for VoxPopLoader."""
    def __init__(self, host, port):
        super(VoxPopLoader, self).__init__()
        self.host = host
        self.port = port

    def serve_forever(self):
        with socketserver.TCPServer(
            (self.host, self.port),
            VoxPopLoaderTCPHandler
        ) as httpd:
            # Activate the server; this will keep running until you
            # interrupt the program with Ctrl-C
            try:
                logger.info(
                    "Started VoxPopLoader on {}:{}".format(
                        self.host,
                        self.port
                    )
                )
                httpd.serve_forever()
            except KeyboardInterrupt:
                logger.info(
                    "VoxPopLoader execution stopped!"
                )
            httpd.server_close()


class VoxPopLoaderTCPHandler(socketserver.BaseRequestHandler):
    """docstring for VoxPopLoaderTCPHandler."""

    def setup(self):

        _itens_per_page = 100
        _sort_by_name = "nome"
        _sort_by_year = "ano"

        self.itens_per_page_filter = \
            "itens={quantity}".format(quantity=_itens_per_page)
        self.sort_by_name_filter = "ordenarPor={option}".format(
            option=_sort_by_name
        )
        self.sort_by_year_filter = "ordenarPor={option}".format(
            option=_sort_by_year
        )
        self.page_filter = "pagina="

        self.base_url = "https://dadosabertos.camara.leg.br/api/v2/"
        self.parliamentarians_ids_url = \
            "{base}deputados?{itens_per_page}&{sort_by}&{page}".format(
                base=self.base_url,
                itens_per_page=self.itens_per_page_filter,
                sort_by=self.sort_by_name_filter,
                page=self.page_filter
            )
        self._specific_parliamentary_url = "{base}deputados/".format(
            base=self.base_url
        )
        self.propositions_ids_url = \
            "{base}proposicoes?{itens_per_page}&{page}".format(
                base=self.base_url,
                itens_per_page=self.itens_per_page_filter,
                page=self.page_filter
            )
        self._specific_proposition_url = "{base}proposicoes/".format(
            base=self.base_url
        )

        self.api_base_url = "api:8000"
        self.propositions_url = \
            "http://{base}/api/propositions/?limit=10000".format(
                base=self.api_base_url
            )
        self.loader_url = "http://{base}/api/loader/".format(
            base=self.api_base_url
        )
        self.get_parliamentarians_url = \
            "{loader}get_parliamentarians/".format(
                loader=self.loader_url
            )
        self.create_parliamentary_url = \
            "{loader}create_parliamentary/".format(
                loader=self.loader_url
            )
        self.get_propositions_url = \
            "{loader}get_propositions/".format(
                loader=self.loader_url
            )
        self.create_proposition_url = \
            "{loader}create_proposition/".format(
                loader=self.loader_url
            )
        self.create_vote_url = \
            "{loader}create_vote/".format(
                loader=self.loader_url
            )
        self.votes_url = \
            "http://www.camara.leg.br/SitCamaraWS/Proposicoes.asmx/" + \
            "ObterVotacaoProposicao?"

    @classmethod
    def __get_credentials(cls):
        with open('.loader_credentials.json', 'r') as f:
            read_data = f.read()

        read_data = json.loads(read_data)
        username = read_data['username']
        password = read_data['password']

        utf_8_authorization = "{username}:{password}".format(
            username=username, password=password
        ).encode()

        return "Basic " + b64encode(utf_8_authorization).decode("ascii")

    @classmethod
    def __get_concatenated_url(cls, url, string):

        response_url = "{url}{string}".format(url=url, string=string)
        return response_url

    def __get_votes_url(self, type, number, year):

        response_url = "{url}tipo={type}&numero={number}&ano={year}".format(
            url=self.votes_url,
            type=type,
            number=number,
            year=year
        )
        return response_url

    def __get_task(self):
        try:
            task_index = {}
            task_index['begin'] = self.data.index('"task": "')
            task_index['end'] = task_index['begin']

            while self.data[task_index['end']] != "\n":
                task_index['end'] += 1

            task = self.data[
                task_index['begin']+9:task_index['end']-1
            ]

        except ValueError:
            task = ""

        return task

    def __send_ok_response(self, task):
        response = "HTTP/1.1 200 OK\n" + \
            "Content-Type: application/json\n" + \
            "\n{\n  \"task\": \"%s\"," % task + \
            "  \"status\": \"OK\"\n}"
        response = response.encode()

        self.request.send(response)

    def __send_bad_request_response(self, task):
        response = "HTTP/1.1 400 Bad Request\n" + \
            "Content-Type: application/json\n" + \
            "\n{\n  \"task\": \"%s\"," % task + \
            "  \"status\": \"Unkown task\"\n}"
        response = response.encode()

        self.request.send(response)

    def __send_unauthorized_response(self):
        response = "HTTP/1.1 401 Unauthorized\n" + \
            "Content-Type: application/json\n" + \
            "\n{\n  \"status\": \"Unauthorized\"\n}"
        response = response.encode()

        self.request.send(response)

    def __send_method_not_allowed_response(self):
        response = "HTTP/1.1 405 Method Not Allowed\n" + \
            "Content-Type: application/json\n" + \
            "\n{\n  \"status\": \"Only POST is permitted\"\n}"
        response = response.encode()

        self.request.send(response)

    def __is_authorized(self):
        try:
            authorization_index = {}
            authorization_index['begin'] = self.data.index('Basic ')
            authorization_index['end'] = authorization_index['begin']

            while self.data[authorization_index['end']] != "\r":
                authorization_index['end'] += 1

            received_authorization = self.data[
                authorization_index['begin']:authorization_index['end']
            ]

            return received_authorization == \
                VoxPopLoaderTCPHandler.__get_credentials()

        except ValueError:
            return False

    def __check_method(self):
        return self.data.split(' ', 1)[0] == "POST"

    def __get_parliamentarians(self):

        start_time = time.time()
        logger.info("Started getting parliamentarians data...")

        _parliamentarians_result = None
        _parliamentarians_ids_list = []
        _page = 1
        us = 'ultimoStatus'

        while _parliamentarians_result != []:

            request_url = \
                VoxPopLoaderTCPHandler.__get_concatenated_url(
                    self.parliamentarians_ids_url,
                    _page
                )

            result = requests.get(
                request_url,
                headers={"content-type": "application/json"}
            )
            _parliamentarians_result = json.loads(result.content)['dados']

            for parliamentary in _parliamentarians_result:
                _parliamentarians_ids_list.append(parliamentary['id'])

            _page += 1

        logger.info("Parliamentarians IDs collected successful!")

        existing_parliamentarians = requests.get(
            self.get_parliamentarians_url,
            params={"key": VoxPopLoaderTCPHandler.__get_credentials()}
        ).content
        existing_parliamentarians_list = json.loads(existing_parliamentarians)

        logger.info("Existing parliamentarians IDs collected successful!")

        for parliamentary_id in _parliamentarians_ids_list:

            if str(parliamentary_id) not in existing_parliamentarians_list:

                try:
                    request_url = \
                        self.__get_concatenated_url(
                            self._specific_parliamentary_url,
                            parliamentary_id
                        )

                    result = requests.get(
                        request_url,
                        headers={"content-type": "application/json"}
                    )

                    parliamentary_result = \
                        json.loads(result.content)['dados']

                    specific_parliamentary_dict = {
                        'parliamentary_id': parliamentary_result['id'],
                        'name': parliamentary_result[us]['nomeEleitoral'],
                        'gender': parliamentary_result['sexo'],
                        'political_party':
                            parliamentary_result[us]['siglaPartido'],
                        'federal_unit': parliamentary_result[us]['siglaUf'],
                        'birth_date': parliamentary_result['dataNascimento'],
                        'education': parliamentary_result['escolaridade'],
                        'email': parliamentary_result[us]['gabinete']['email'],
                        'photo': parliamentary_result[us]['urlFoto']
                    }

                    requests.post(
                        self.create_parliamentary_url,
                        data=specific_parliamentary_dict,
                        params={
                            "key": VoxPopLoaderTCPHandler.__get_credentials()
                        }
                    )
                    # Parliamentary.objects.create(**specific_parliamentary_dict)

                    logger.info("Parliamentary " + str(parliamentary_id) +
                                " saved!")

                except Exception as e:
                    logger.error(
                        "An error has occurred trying to save" +
                        " parliamentary " + str(parliamentary_id) + " data."
                    )
                    logger.error(str(e))

            else:
                logger.warning("Parliamentary " + str(parliamentary_id) +
                               " already exists!")

        logger.info("Parliamentarians data collected successful!")

        duration = time.time() - start_time
        logger.info("Get parliamentarians took %.2f seconds." % duration)

    def __get_propositions(self):

        start_time = time.time()
        logger.info("Started getting propositions data...")

        # years_list = ['2015', '2016', '2017', '2018']
        #
        # for year in years_list:

        years = ['2018', '2017', '2016', '2015']
        voted_list = []

        for year in years:

            voted_r = requests.get(
                'http://www.camara.leg.br/SitCamaraWS/Proposicoes.asmx/' +
                'ListarProposicoesVotadasEmPlenario?ano={year}&tipo='.format(
                    year=year
                )
            )

            root = ET.fromstring(str(voted_r.content, 'utf-8'))

            for proposition in root:
                if proposition[0].text not in voted_list:
                    voted_list.append(proposition[0].text)

        logger.info("Propositions IDs collected successful!")

        get_propositions = requests.get(
            self.propositions_url,
            headers={"content-type": "application/json"}
        )
        get_propositions_results = json.loads(
            get_propositions.content
        )['results']
        get_propositions_list = []

        for prop_result in get_propositions_results:
            get_propositions_list.append(prop_result['native_id'])

        # logger.debug(get_propositions_list)

        logger.info("Existing propositions IDs collected successful!")

        # for proposition_id in _propositions_ids_list:
        for proposition_id in voted_list:

            if str(proposition_id) not in get_propositions_list:

                request_url = \
                    self.__get_concatenated_url(
                        self._specific_proposition_url,
                        proposition_id
                    )

                result = requests.get(
                    request_url,
                    headers={"content-type": "application/json"}
                )

                proposition_result = \
                    json.loads(result.content)['dados']

                sp = 'statusProposicao'

                specific_proposition_dict = {
                    'native_id': proposition_result['id'],
                    # Tipo de proposição
                    'proposition_type': proposition_result['descricaoTipo'],
                    # Sigla do tipo de proposição
                    'proposition_type_initials':
                        proposition_result['siglaTipo'],
                    # Número da proposição
                    'number': proposition_result['numero'],
                    # Ano de apresentação
                    'year': proposition_result['ano'],
                    # Ementa da proposição
                    'abstract': proposition_result['ementa'],
                    # Tramitação
                    'processing':
                        proposition_result[sp]['descricaoTramitacao'],
                    # Situação
                    'situation': proposition_result[sp]['descricaoSituacao'],
                    # URL da proposição na íntegra
                    'url_full': proposition_result[sp]['url'],
                    # Última atualização da proposição
                    'last_update': proposition_result[sp]['dataHora']
                }

                requests.post(
                    self.create_proposition_url,
                    data=specific_proposition_dict,
                    params={"key": VoxPopLoaderTCPHandler.__get_credentials()}
                )
                # Proposition.objects.create(**specific_proposition_dict)

                logger.info("Proposition " + str(proposition_id) +
                            " saved!")

            else:
                logger.warning("Proposition " + str(proposition_id) +
                               " already exists!")

        logger.info("Propositions data collected successful!")

        duration = time.time() - start_time
        logger.info("Get propositions took %.2f seconds." % duration)

    def __get_votes(self):

        existing_propositions = requests.get(
            self.propositions_url,
            headers={"content-type": "application/json"}
        )
        existing_propositions_results = json.loads(
            existing_propositions.content
        )['results']
        existing_propositions_list = []

        for prop_result in existing_propositions_results:
            if int(prop_result['year']) >= 2014:
                existing_propositions_list.append({
                    'type': prop_result['proposition_type_initials'],
                    'number': prop_result['number'],
                    'year': prop_result['year'],
                    'native_id': prop_result['native_id']
                })

        # logger.debug(get_propositions_list)

        logger.info("Existing propositions informations collected successful!")

        count = 0

        for proposition in existing_propositions_list:

            # logger.debug(self.__get_votes_url(
            #     proposition['type'],
            #     proposition['number'],
            #     proposition['year']
            # ))

            vote_request = requests.get(
                self.__get_votes_url(
                    proposition['type'],
                    proposition['number'],
                    proposition['year']
                )
            )

            count += 1

            # logger.debug('Tried ' + str(count))
            # logger.debug(proposition)

            if str(vote_request.status_code) == '200':

                logger.info("Voting found on proposition " +
                            str(proposition['native_id']) + "!")

                root = ET.fromstring(str(vote_request.content, 'utf-8'))

                max_date = datetime.datetime.strptime(
                    '01/01/1990',
                    '%d/%m/%Y'
                ).date()

                for voting in root.find('Votacoes'):

                    date = datetime.datetime.strptime(
                        voting.attrib['Data'],
                        '%d/%m/%Y'
                    ).date()

                    if date > max_date:
                        max_date = date
                        recent_voting = voting

                votes_list = []
                for vote in recent_voting.find('votos'):

                    specific_vote_dict = {
                        'parliamentary': vote.attrib['ideCadastro'],
                        'option': vote.attrib['Voto'].strip()[0],
                        'proposition': proposition['native_id']
                    }

                    if specific_vote_dict['option'] == '-':
                        specific_vote_dict['option'] = 'M'
                    elif specific_vote_dict['option'] == 'S':
                        specific_vote_dict['option'] = 'Y'

                    votes_list.append(specific_vote_dict)

                requests.post(
                    self.create_vote_url,
                    data={'votes_list': json.dumps(votes_list)},
                    params={
                        "key": VoxPopLoaderTCPHandler.__get_credentials()
                    }
                )

                logger.info("Votes from proposition " +
                            str(specific_vote_dict['proposition']) +
                            " saved!")

                # logger.info("Vote from parliamentary " +
                #             str(specific_vote_dict['parliamentary']) +
                #             " and " + "proposition " +
                #             str(specific_vote_dict['proposition']) +
                #             " saved!")

    def handle(self):
        self.data = self.request.recv(4096).strip().decode()

        if self.__is_authorized():

            if self.__check_method():

                task = self.__get_task()

                if task == "get_parliamentarians":

                    try:
                        logger.info(
                            "{} has requested VoxPopLoader to get ".format(
                                self.client_address[0]
                            ) + " parliamentarians data."
                        )
                        self.__get_parliamentarians()
                        self.__send_ok_response("get_parliamentarians")

                    except Exception as e:
                        logger.error(
                            "An error has occurred trying to get" +
                            " parliamentarians data."
                        )
                        logger.error(str(e))

                elif task == "get_propositions":

                    try:
                        logger.info(
                            "{} has requested VoxPopLoader to get ".format(
                                self.client_address[0]
                            ) + " propositions data."
                        )
                        self.__get_propositions()
                        self.__send_ok_response("get_propositions")

                    except Exception as e:
                        logger.error(
                            "An error has occurred trying to get" +
                            " propositions data."
                        )
                        logger.error(str(e))

                elif task == "get_votes":

                    try:
                        logger.info(
                            "{} has requested VoxPopLoader to get".format(
                                self.client_address[0]
                            ) + " votes data."
                        )
                        self.__get_votes()
                        self.__send_ok_response("get_votes")

                    except Exception as e:
                        logger.error(
                            "An error has occurred trying to get" +
                            " votes data."
                        )
                        logger.error(str(e))

                else:
                    logger.warning(
                       "{} has requested VoxPopLoader with wrong".format(
                            self.client_address[0]
                       ) + " task: {}".format(
                            task
                        )
                    )
                    self.__send_bad_request_response(task)

            else:
                logger.warning(
                    "{} has requested VoxPopLoader with wrong method.".format(
                        self.client_address[0]
                    )
                )
                self.__send_method_not_allowed_response()

        else:
            logger.warning(
                "{} has requested VoxPopLoader without authorization.".format(
                    self.client_address[0]
                )
            )
            self.__send_unauthorized_response()


def main():
    if len(sys.argv) == 3:

        if sys.argv[1] == 'runservice':

            service_address = sys.argv[2].split(':')
            host = service_address[0]
            port = service_address[1]

            LOADER = VoxPopLoader(host, int(port))
            LOADER.serve_forever()

        else:
            logging.error(
                'Unkown command: {unkown}'.format(
                    unkown=sys.argv[1]
                )
            )

    else:
        logging.error('Run service with: python loader.py runservice' +
                      '<HOST>:<IP>')


if __name__ == "__main__":
    main()
