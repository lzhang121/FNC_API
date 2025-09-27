pipeline {
    agent any

    tools {
        // This requires a Python installation named 'Python3' to be configured
        // in Jenkins -> Manage Jenkins -> Global Tool Configuration.
        python 'Python3'
    }

    environment {
        // Define the path to the virtual environment
        VENV = ".venv"
    }

    stages {
        stage('Checkout') {
            steps {
                // Get some code from a GitHub repository
                git branch: 'main', url: 'https://github.com/lzhang121/FNC_API.git'
                script {
                    // Set the GIT_COMMITTER_NAME and GIT_COMMITTER_EMAIL
                    // to avoid issues with git commands in the pipeline
                    sh 'git config user.name "Jenkins"'
                    sh 'git config user.email "jenkins@example.com"'
                }
            }
        }

        stage('Setup Environment') {
            steps {
                script {
                    // Create a virtual environment
                    sh "python -m venv ${VENV}"
                    // Activate the virtual environment and install dependencies
                    sh "${VENV}/bin/pip install --upgrade pip"
                    sh "${VENV}/bin/pip install -r requirements.txt"
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    // Clean old allure results
                    sh 'rm -rf allure-results/*'
                    // Run pytest and generate allure results
                    sh "${VENV}/bin/pytest --env=test --alluredir=allure-results"
                }
            }
        }

        stage('Publish Allure Report') {
            steps {
                allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
            }
        }
    }

    post {
        always {
            // Clean up the workspace
            cleanWs()
        }
    }
}
