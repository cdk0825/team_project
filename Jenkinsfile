pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo '📥 GitLab 저장소 가져오기'
                checkout scm
            }
        }

        stage('Python Version Check') {
            steps {
                // environment 변수를 쓸 때는 $변수명 형식을 권장합니다.
                sh 'python --version'
                sh 'pip --version'
            }
        }

        stage('Install Dependencies & Test') {
            steps {
                echo '📦 가상환경 생성 및 의존성 설치'
                sh """
                set -e
                
                # 2. 가상환경 활성화 및 패키지 설치
                pip install --upgrade pip
                
                # requirements.txt가 있을 때만 설치
                if [ -f requirements.txt ]; then
                    pip install -r requirements.txt
                fi
                
                # pytest는 필수 설치
                pip install pytest
                
                # 3. 테스트 실행 (이 단계에서 실행해야 가상환경 패키지를 인식함)
                pytest tests/ --junitxml=pytest-report.xml || true
                """
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
            junit allowEmptyResults: true, testResults: 'pytest-report.xml'
        }
    }
}
