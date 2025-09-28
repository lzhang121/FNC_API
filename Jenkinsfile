pipeline {
    agent any

    parameters {
        choice(name: 'env', choices: ['test01', 'test03', 'prod'], description: 'Select the environment to run the tests against.')
    }

    environment {
        // 定义虚拟环境路径
        VENV = "${WORKSPACE}/.venv"
        // pip 缓存目录，避免重复下载依赖
        PIP_CACHE_DIR = "/var/jenkins_home/.cache/pip"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/lzhang121/FNC_API.git'
                script {
                    sh 'git config user.name "Jenkins"'
                    sh 'git config user.email "jenkins@example.com"'
                }
            }
        }

        stage('Setup Environment') {
            steps {
                script {
                    // 如果 .venv 不存在，才创建并安装依赖
                    if (!fileExists("${VENV}/bin/activate")) {
                        echo "Creating virtual environment and installing dependencies..."
                        sh "python3 -m venv ${VENV}"
                        sh "${VENV}/bin/pip install --upgrade pip"
                        sh "PIP_CACHE_DIR=${PIP_CACHE_DIR} ${VENV}/bin/pip install -r requirements.txt"
                    } else {
                        echo "Using cached virtual environment"
                        // 如果 requirements.txt 改了，可以手动强制更新
                        // sh "${VENV}/bin/pip install -r requirements.txt"
                    }
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    sh 'rm -rf allure-results/*'
                    sh "${VENV}/bin/pytest --env=${params.env} --alluredir=allure-results"
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
            // 保留 .venv，避免每次都重装依赖
            sh 'rm -rf allure-results/*'
        }
    }
}
