docker_status := $(shell systemctl is-active docker)
docker_enabled := $(shell systemctl is-enabled docker)
environment := "dev"

help:
	@echo "Utilize: make <comando> [<argumentos>]"
	@echo
	@echo "Comandos disponíveis:"
	@echo
	@echo "Gerenciar docker"
	@echo "	docker-start	Inicia o serviço do docker"
	@echo "	docker-stop	Para o serviço do docker"
	@echo "	docker-enable	Faz docker iniciar automaticamente ao iniciar o sistema"
	@echo "	docker-disable	Faz docker não iniciar automaticamente ao iniciar o sistema"
	@echo
	@echo "Gerenciar containers da aplicação:"
	@echo "	up		Efetua build da imagem, (re)cria e inicia todos os containers da aplicação"
	@echo "	build		Efetua (re)build da imagem da aplicação"
	@echo "	start		Inicia todos os containers da aplicação (já devem ter sido criados)"
	@echo "	stop		Interrompe todos os containers da aplicação"
	@echo "	remove		Remove todos os containers da aplicação"
	@echo "	status		Exibe o status dos containers da aplicação"
	@echo "	logs		Exibe os logs da aplicação"
	@echo "	bash		Abre um bash dentro do container da aplicação"
	@echo "	cmd		Executa um comando dentro do container da aplicação"
	@echo "			Exemplo: make cmd command=\"python3 manage.py shell\""
	@echo
	@echo "Executar comandos do Django:"
	@echo "	startapp	Cria um novo app. Argumentos necessários: name"
	@echo "			Exemplo: make startapp name=auth"
	@echo "	makemigrations	Gerar migrations para o projeto"
	@echo "	migrate		Aplicar migrations ao banco"
	@echo "	collectstatic	Coletar arquivos estáticos"

# Gerenciar docker

docker-start:
ifeq (${docker_status}, inactive)
	@sudo systemctl start docker
	@echo "VoxPop: Serviço do Docker iniciado com sucesso!"
else
	@echo "VoxPop: Serviço do Docker já está ativo!"
endif

docker-stop:
ifeq (${docker_status}, active)
	@sudo systemctl stop docker
	@echo "VoxPop: Serviço do Docker interrompido com sucesso!"
else
	@echo "VoxPop: Serviço do Docker já está inativo!"
endif

docker-enable:
ifeq (${docker_enabled}, disabled)
	@sudo systemctl enable docker
	@echo "VoxPop: Serviço do Docker agora iniciará junto com o sistema!"
else
	@echo "VoxPop: Serviço do Docker já inicia junto com o sistema!"
endif

docker-disable:
ifeq (${docker_enabled}, enabled)
	@sudo systemctl disable docker
	@echo "VoxPop: Serviço do Docker deixará de iniciar junto com o sistema!"
else
	@echo "VoxPop: Serviço do Docker já não inicia junto com o sistema!"
endif

# Gerenciar containers da aplicação
compose_file := "provision/dev/docker-compose.yml"

up:
ifeq (${docker_status}, active)
	@sudo docker-compose -f ${compose_file} up -d --force-recreate
	@echo "VoxPop: Containers (re)criados e iniciados com sucesso!"
else
	@echo "VoxPop: Serviço do Docker está inativo!"
endif

build:
ifeq (${docker_status}, active)
	@sudo docker-compose -f ${compose_file} build
	@echo "VoxPop: (Re)build de imagem efetuado com sucesso!"
else
	@echo "VoxPop: Serviço do Docker está inativo!"
endif

start:
ifeq (${docker_status}, active)
	@sudo docker-compose -f ${compose_file} start
	@echo "VoxPop: Containers da aplicação iniciados com sucesso!"
else
	@echo "VoxPop: Serviço do Docker está inativo!"
endif

stop:
ifeq (${docker_status}, active)
	@sudo docker-compose -f ${compose_file} stop
	@echo "VoxPop: Containers da aplicação interrompidos com sucesso!"
else
	@echo "VoxPop: Serviço do Docker está inativo!"
endif

remove:
ifeq (${docker_status}, active)
	@sudo docker-compose -f ${compose_file} rm
	@echo "VoxPop: Containers da aplicação removidos com sucesso!"
else
	@echo "VoxPop: Serviço do Docker está inativo!"
endif

status:
ifeq (${docker_status}, active)
	@sudo docker-compose -f ${compose_file} ps
else
	@echo "VoxPop: Serviço do Docker está inativo!"
endif

logs:
ifeq (${docker_status}, active)
	@sudo docker-compose -f ${compose_file} logs -f
else
	@echo "VoxPop: Serviço do Docker está inativo!"
endif

bash:
ifeq (${docker_status}, active)
	@sudo docker-compose -f ${compose_file} exec api bash
else
	@echo "VoxPop: Serviço do Docker está inativo!"
endif

cmd:
ifeq (${docker_status}, active)
	@sudo docker-compose -f ${compose_file} exec api ${command}
else
	@echo "VoxPop: Serviço do Docker está inativo!"
endif

# Executar comandos do Django

startapp:
ifeq (${docker_status}, active)
	@sudo docker-compose -f ${compose_file} exec api python3 manage.py startapp ${name}
else
	@echo "VoxPop: Serviço do Docker está inativo!"
endif

makemigrations:
ifeq (${docker_status}, active)
	@sudo docker-compose -f ${compose_file} exec api python3 manage.py makemigrations
else
	@echo "VoxPop: Serviço do Docker está inativo!"
endif

migrate:
ifeq (${docker_status}, active)
	@sudo docker-compose -f ${compose_file} exec api python3 manage.py migrate
else
	@echo "VoxPop: Serviço do Docker está inativo!"
endif

collectstatic:
ifeq (${docker_status}, active)
	@sudo docker-compose -f ${compose_file} exec api python3 manage.py collectstatic --noinput
else
	@echo "VoxPop: Serviço do Docker está inativo!"
endif
