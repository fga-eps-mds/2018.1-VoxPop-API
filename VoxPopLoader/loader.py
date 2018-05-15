import json
import logging
import logging.config
import socketserver
import sys
import time
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
                    'name':
                        parliamentary_result['ultimoStatus']['nomeEleitoral'],
                    'gender': parliamentary_result['sexo'],
                    'partido': parliamentary_result['ultimoStatus']['siglaPartido'],
                    'federal_unit':
                        parliamentary_result['ultimoStatus']['siglaUf'],
                    'birth_date': parliamentary_result['dataNascimento'],
                    'education': parliamentary_result['escolaridade'],
                    'email': parliamentary_result['ultimoStatus']['gabinete']['email'],
                    'photo': parliamentary_result['ultimoStatus']['urlFoto']
                }

                requests.post(
                    self.create_parliamentary_url,
                    data=specific_parliamentary_dict,
                    params={"key": VoxPopLoaderTCPHandler.__get_credentials()}
                )
                # Parliamentary.objects.create(**specific_parliamentary_dict)

                logger.info("Parliamentary " + str(parliamentary_id) +
                            " saved!")

            else:
                logger.warning("Parliamentary " + str(parliamentary_id) +
                               " already exists!")

        logger.info("Parliamentarians data collected successful!")

        duration = time.time() - start_time
        logger.info("Get parliamentarians took %.2f seconds." % duration)

    def __get_propositions(self):

        start_time = time.time()
        logger.info("Started getting propositions data...")

        _propositions_result = None
        _propositions_ids_list = []
        _page = 1

        while _propositions_result != []:

            request_url = \
                VoxPopLoaderTCPHandler.__get_concatenated_url(
                    self.propositions_ids_url,
                    _page
                )

            result = requests.get(
                request_url,
                headers={"content-type": "application/json"}
            )
            _propositions_result = json.loads(result.content)['dados']

            for proposition in _propositions_result:
                _propositions_ids_list.append(proposition['id'])

            _page += 1

        logger.info("Propositions IDs collected successful!")

        existing_propositions = requests.get(
            self.get_propositions_url,
            params={"key": VoxPopLoaderTCPHandler.__get_credentials()}
        ).content
        existing_propositions_list = json.loads(existing_propositions)

        logger.info("Existing propositions IDs collected successful!")

        for proposition_id in _propositions_ids_list:

            if str(proposition_id) not in existing_propositions_list:

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
                    'url_full': proposition_result[sp]['url']
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

    def handle(self):
        self.data = self.request.recv(4096).strip().decode()

        if self.__is_authorized():

            if self.__check_method():

                task = self.__get_task()

                if task == "get_parliamentarians":

                    try:
                        logger.info(
                            "{} has requested VoxPopLoader to get".format(
                                self.client_address[0]
                            ) + "parliamentarians data."
                        )
                        self.__get_parliamentarians()
                        self.__send_ok_response("get_parliamentarians")

                    except Exception as e:
                        logger.error(
                            "An error has occurred trying to get" +
                            "parliamentarians data."
                        )
                        logger.error(str(e))

                elif task == "get_propositions":

                    try:
                        logger.info(
                            "{} has requested VoxPopLoader to get".format(
                                self.client_address[0]
                            ) + "propositions data."
                        )
                        self.__get_propositions()
                        self.__send_ok_response("get_propositions")

                    except Exception as e:
                        logger.error(
                            "An error has occurred trying to get" +
                            "propositions data."
                        )
                        logger.error(str(e))

                else:
                    logger.warning(
                       "{} has requested VoxPopLoader with wrong".format(
                            self.client_address[0]
                       ) + "task: {}".format(
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
