pipeline {
    agent any

    stages {

        stage('Build Backend Docker Image') {
            steps {
                bat 'docker build -t dpdp-backend .'
            }
        }

        stage('Run Backend Container') {
            steps {
                bat 'docker run -d -p 8000:8000 dpdp-backend'
            }
        }

    }
}