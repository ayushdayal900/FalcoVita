pipeline {
    agent any

    triggers {
        pollSCM('H/5 * * * *')  // polls GitHub every 5 minutes
    }

    stages {

        // clone the repository
        stage('Clone') {
            steps {
                git branch: 'main', url: 'https://github.com/ayushdayal900/FalcoVita.git'
            }
        }


        // build all docker images via docker-compose
        stage('Build Docker Images') {
            steps {
                sh 'docker-compose build'
            }
        }

        // stop and remove old containers to avoid port conflicts
        stage('Teardown Old Containers') {
            steps {
                sh 'docker-compose down --remove-orphans || true'
            }
        }

        // start all services in detached mode
        stage('Deploy') {
            steps {
                sh 'docker-compose up -d'
            }
        }
    }
}
