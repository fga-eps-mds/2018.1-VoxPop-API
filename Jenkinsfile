#!groovy

pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
            checkout scm
            slackSend color: "warning", message: "Started `${env.JOB_NAME}#${env.BUILD_NUMBER}`"
            }
        }
        stage('Setup environment') {
            steps {
                sh '. /var/lib/jenkins/workspace/.virtualenvs/api/bin/activate'
                sh '/var/lib/jenkins/workspace/.virtualenvs/api/bin/pip install -r requirements.txt'
                sh '/var/lib/jenkins/workspace/.virtualenvs/api/bin/python3 manage.py makemigrations --noinput'
                sh '/var/lib/jenkins/workspace/.virtualenvs/api/bin/python3 manage.py migrate --noinput'

            }
        }
        stage('Test') {
            steps {
                sh "flake8 --exclude='manage.py, voxpopapi/settings.py, migrations, templates, */models.py, */tests.py, */admin.py, provision, nginx, docs, setup.py' ."
                sh '/var/lib/jenkins/workspace/.virtualenvs/api/bin/python3 manage.py test'
            }
        }
        stage('Homologation deploy') {
            when {
                branch 'dev'
            }
            steps {
                sh 'ansible-playbook -i provision/hosts provision/hml/deploy.yml'
            }
        }
        stage('Production deploy') {
            when {
                branch 'master'
            }
            steps {
                sh 'ansible-playbook -i provision/hosts provision/prod/deploy.yml'
            }
        }
    }
    post {
        success {
            slackSend color: "good", message: "Build successful: `${env.JOB_NAME}#${env.BUILD_NUMBER}` <${env.BUILD_URL}|Open in Jenkins>"
        }
        failure {
            slackSend color: "danger", message: "Build failed :face_with_head_bandage: \n`${env.JOB_NAME}#${env.BUILD_NUMBER}` <${env.BUILD_URL}|Open in Jenkins>"
        }
    }
}
