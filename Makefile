docker_status := $(shell systemctl is-active docker)
environment := "dev"

help:
	@echo "Utilize: make <comando> [<argumentos>]"
	@echo
	@echo "Comandos disponíveis:"
	@echo
	@echo "Gerenciar containers da aplicação:"
	@echo "	up		Efetua build da imagem e cria/inicia todos os containers da aplicação"
	@echo "	start		Inicia todos os containers da aplicação (já devem ter sido criados)"
	@echo "	stop		Interrompe todos os containers da aplicação"
	@echo "	remove		Remove todos os containers da aplicação"
	@echo "	status		Exibe o status dos containers da aplicação"
	@echo "	tail		Exibe os logs da aplicação"
	@echo
	@echo "Executar comandos do Django:"
	@echo "	startapp	Cria um novo app. Argumentos necessários: name"
	@echo "			Exemplo: make startapp name=auth"
	@echo "	makemigrations	Gerar migrations para o projeto"
	@echo "	migrate		Aplicar migrations ao banco"
	@echo "	collectstatic	Coletar arquivos estáticos"
	@echo "	collectstatic	Coletar arquivos estáticos"

# Gerenciar containers da aplicação
up:
ifeq (${docker_status}, active)
	sudo docker-compose up
else
	echo ${docker_status}
endif
