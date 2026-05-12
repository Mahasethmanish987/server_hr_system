def COLOR_MAP = [
    'SUCCESS' : 'good',
    'FAILURE' : 'danger',
    ]

pipeline {
    agent { label 'jenkinsrunner' }

    options {
        timeout(time: 10, unit: 'MINUTES')
    }

    stages {
        stage('Cleanup') {
            steps {
                sh 'docker compose down -v --remove-orphans || true'
            }
        }

        stage('Checkout') {
            steps {
                git branch: 'main', 
                    url: 'git@github.com:Mahasethmanish987/server_hr_system.git'
            }
        }

        stage('Code Quality (Flake8)') {
            steps {
                sh '''
                    docker run --rm -v "$WORKSPACE:/app" -w /app python:3.11-slim \
                        sh -c "pip install --quiet flake8 flake8-checkstyle && \
                               flake8 . --format=checkstyle" > checkstyle-result.xml || true
                '''
            }
        }

                     

        stage('Run Tests') {
            steps {
                withCredentials([file(credentialsId: 'my-app-env-file', variable: 'TEMP_ENV')]) {
                    sh '''
                        #!/bin/bash
                        set -e
                        chmod +x ./entrypoint.sh
                        cp "$TEMP_ENV" .env
                        docker compose build --no-cache
                        docker compose up -d postgres redis
                        sleep 5
                        docker compose run --rm web pytest --cov=. --cov-report=xml 
                    '''
                }
            }
        }
        stage('SonarQube Analysis') {
    steps {
        script {
            def scannerHome = tool 'sonar8.0'

            withSonarQubeEnv('sonarserver') {
                sh """
${scannerHome}/bin/sonar-scanner \
-Dsonar.projectKey=server_hr_system \
-Dsonar.sources=. \
-Dsonar.python.version=3.11 \
-Dsonar.sourceEncoding=UTF-8 \
-Dsonar.python.flake8.reportPaths=checkstyle-result.xml \
-Dsonar.python.coverage.reportPaths=coverage.xml \
-Dsonar.exclusions=**/static/**,**/tests/**
"""
            }
        }
    }
}
stage("Quality Gate") {
    steps {
        script {
            timeout(time: 1, unit: 'HOURS') {
                waitForQualityGate abortPipeline: true
            }
        }
    }
}
    }

    post {
        always {
            sh 'docker compose down -v'
            sh 'rm -f .env'
            echo "slack notification"
            slackSend( 
                channel: '#monitoring-alerts',
                color: COLOR_MAP[currentBuild.currentResult],
                message: "*${currentBuild.currentResult}:* Job ${env.JOB_NAME} build ${env.BUILD_NUMBER} \n More info at: ${env.BUILD_URL}")
        }
        success {
            echo "All tests passed!"
        }
        failure {
            echo "Pipeline failed."
        }
    }
}