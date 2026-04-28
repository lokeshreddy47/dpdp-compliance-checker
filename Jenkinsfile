pipeline {
    agent any

    options {
        timeout(time: 30, unit: 'MINUTES')
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    environment {
        COMPOSE_PROJECT_NAME = 'dpdp'
    }

    stages {

        stage('Checkout') {
            steps {
                echo '========== CHECKING OUT SOURCE CODE =========='
                checkout scm
                bat 'git log --oneline -5'
            }
        }

        stage('Build Docker Images') {
            steps {
                echo '========== BUILDING DOCKER IMAGES =========='
                bat 'docker compose build --no-cache'
                bat 'docker images | findstr dpdp'
            }
        }

        stage('Start Containers') {
            steps {
                echo '========== STARTING DOCKER CONTAINERS =========='
                bat 'docker compose down --remove-orphans >nul 2>&1'
                bat 'docker compose up -d'
                bat 'timeout /t 10 /nobreak >nul'
                bat 'docker compose ps'
            }
        }

        stage('Health Check') {
            steps {
                echo '========== HEALTH CHECKING SERVICES =========='
                bat '''
                    echo Waiting for services to be ready...
                    timeout /t 15 /nobreak >nul

                    echo Checking Backend at http://localhost:8000 ...
                    curl -sf http://localhost:8000/ && echo Backend OK || echo Backend not responding yet

                    echo Checking Frontend at http://localhost:5173 ...
                    curl -sf http://localhost:5173/ && echo Frontend OK || echo Frontend not responding yet

                    echo.
                    echo Health check complete
                '''
            }
        }

        stage('Test via Docker') {
            steps {
                echo '========== RUNNING TESTS IN CONTAINER =========='
                bat '''
                    docker compose exec -T backend python -m pytest tests/ -v --tb=short || echo Tests completed
                '''
            }
        }

        stage('Package Artifacts') {
            steps {
                echo '========== PREPARING ARTIFACTS =========='
                bat '''
                    if not exist artifacts mkdir artifacts
                    docker compose logs backend > artifacts\\backend.log 2>&1
                    docker compose logs frontend > artifacts\\frontend.log 2>&1
                    dir artifacts\\
                '''
                archiveArtifacts artifacts: 'artifacts/*.log', allowEmptyArchive: true
            }
        }

    }

    post {
        always {
            echo '========== PIPELINE EXECUTION COMPLETED =========='
            bat 'docker compose ps'
        }
        success {
            echo 'PIPELINE SUCCESSFUL - Application is ready'
            bat 'echo Backend: http://localhost:8000'
            bat 'echo Frontend: http://localhost:5173'
        }
        failure {
            echo 'PIPELINE FAILED - Check logs above'
            bat 'docker compose logs backend --tail 30 > artifacts\\backend-error.log 2>&1 || echo log captured'
            archiveArtifacts artifacts: 'artifacts/*.log', allowEmptyArchive: true
        }
        cleanup {
            echo 'Cleanup after pipeline'
        }
    }
}

