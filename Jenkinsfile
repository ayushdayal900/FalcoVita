pipeline {
    agent any

    stages {

        // clone the repository
        stage('Clone') {
            steps {
                git branch: 'main', url: 'https://github.com/ayushdayal900/FalcoVita.git'
            }
        }

        // install frontend dependencies
        stage('Install Frontend Dependencies') {
            steps {
                dir('frontend') {
                    sh 'npm install'
                }
            }
        }

        // install backend dependencies
        stage('Install Backend Dependencies') {
            steps {
                dir('backend') {
                    sh 'pip install -r requirements.txt'
                }
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
