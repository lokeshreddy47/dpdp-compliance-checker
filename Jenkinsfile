pipeline {
    agent any

    stages {

        stage('Build Backend Docker Image') {
            steps {
                sh 'docker build -t dpdp-backend .'
            }
        }

        stage('Run Backend Container') {
            steps {
                sh 'docker stop dpdp-backend-container || true'
                sh 'docker rm dpdp-backend-container || true'
                sh 'docker run -d -p 8000:8000 --name dpdp-backend-container dpdp-backend'
            }
        }
    }
}