pipeline {

    agent {
        label 'jenkinsrunner'
    }

    stages {

        stage('Fetch Code') {
            steps {
                git branch: 'main',
                url: 'https://github.com/Mahasethmanish987/server_hr_system.git'
            }
        }
        stage('Give permissions') {
            steps {
                sh 'chmod +x ./entrypoint.sh'
                
            }
        }

        stage('Build Containers') {
            steps {

                sh 'docker compose build'
            }
        }

        stage('Run Containers') {
            steps {
                sh 'docker compose run --rm web pytest'
            }
        }

    }

    post {

        success {
            echo 'Application deployed successfully'
        }

        failure {
            echo 'Deployment failed'
        }
    }
}