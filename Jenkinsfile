pipeline {
    agent any

    environment {
        GITHUB_CREDENTIALS = credentials('github-credentials')
        APP_NAME           = "my-python-app"
        DEPLOY_PORT        = "5000"
    }

    stages {

        stage('Checkout') {
            steps {
                echo '========== Checking out code from GitHub =========='
                git(
                    url           : 'https://github.com/Rishabhgoyal0183/Python_Demo.git',
                    branch        : 'main',
                    credentialsId : 'github-credentials'
                )
                echo 'Code checked out successfully!'
            }
        }

        stage('Clean') {
            steps {
                echo '========== Cleaning old build files =========='
                sh '''
                    rm -rf venv
                    rm -rf dist
                    rm -rf build
                    rm -rf *.egg-info
                    find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
                    find . -name "*.pyc" -delete 2>/dev/null || true
                '''
                echo 'Clean completed!'
            }
        }

        stage('Build') {
            steps {
                echo '========== Building the Application =========='
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install pytest build
                    echo "--- Running Tests ---"
                    pytest tests/ -v --junitxml=test-results.xml
                    echo "--- Building Package ---"
                    python3 -m build
                '''
            }
            post {
                always {
                    junit 'test-results.xml'
                }
                failure {
                    echo '❌ Tests failed! Stopping deployment.'
                }
            }
        }

        stage('Deploy') {
    steps {
        echo '========== Deploying the Application =========='
        sh '''
            # Kill any old running instance
            pkill -f "gunicorn" || true
            sleep 2

            # Use gunicorn FROM INSIDE venv (not system gunicorn)
            WORKSPACE_DIR=$(pwd)

            # Start app using venv's guxnicorn directly with full path
            nohup $WORKSPACE_DIR/venv/bin/gunicorn \
                -w 2 \
                -b 0.0.0.0:5000 \
                app.main:app \
                --chdir $WORKSPACE_DIR > $WORKSPACE_DIR/app.log 2>&1 &

            sleep 3

            # Verify it started
            echo "--- Checking if app is running ---"
            ps aux | grep gunicorn | grep -v grep

            # Test the app
            curl -s http://localhost:5000 || echo "App not responding yet"

            echo "App deployed at http://$(curl -s ifconfig.me):5000"
        '''
    }
}

    }

    post {
        success {
            echo '✅ Pipeline completed! App is live.'
        }
        failure {
            echo '❌ Pipeline failed! Check the logs above.'
        }
        always {
            echo 'Pipeline finished.'
        }
    }
}