pipeline {
    agent any

    environment {
        PYTHON_VERSION = 'python3'
    }

    stages {

        stage('Checkout') {
            steps {
                echo '📥 GitLab 저장소 가져오기'
                checkout scm
            }
        }

        stage('Python Version Check') {
            steps {
                sh '''
                ${PYTHON_VERSION} --version
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                echo '📦 의존성 설치'
                sh '''
                ${PYTHON_VERSION} -m pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                echo '🧪 자동화 테스트 실행'
                sh '''
                pytest tests/ --junitxml=pytest-report.xml
                '''
            }
        }
    }

    post {
        success {
            echo '✅ CI 테스트 성공'
        }
        failure {
            echo '❌ CI 테스트 실패'
        }
        always {
            echo '📌 테스트 리포트 아카이브'
            junit 'pytest-report.xml'
        }
    }
}
