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
                    rm -f gunicorn.pid
                    rm -f access.log
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
                    # Step 1 - Create fresh virtual environment
                    python3 -m venv venv

                    # Step 2 - Activate venv
                    . venv/bin/activate

                    # Step 3 - Install all dependencies + gunicorn
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install pytest build gunicorn

                    # Step 4 - Confirm gunicorn binary exists on disk
                    echo "--- Verifying gunicorn binary ---"
                    ls -la venv/bin/gunicorn

                    # Step 5 - Run Tests
                    echo "--- Running Tests ---"
                    pytest tests/ -v --junitxml=test-results.xml

                    # Step 6 - Build Package
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
                    # Step 1 - Kill OLD gunicorn PROCESS
                    echo "--- Stopping old gunicorn process ---"
                    pkill -f "gunicorn" || true
                    sleep 2

                    # Step 2 - Set workspace path
                    WORKSPACE_DIR=$(pwd)

                    # Step 3 - Start gunicorn as daemon detached from Jenkins
                    echo "--- Starting gunicorn detached from Jenkins ---"
                    JENKINS_NODE_COOKIE=dontKillMe \
                    nohup $WORKSPACE_DIR/venv/bin/gunicorn \
                	-w 2 \
               	 	-b 0.0.0.0:5000 \
                	app.main:app \
                	--chdir $WORKSPACE_DIR >> $WORKSPACE_DIR/app.log 2>&1 &

                    # Step 4 - Wait for process to boot
                    sleep 5

                    # Step 5 - Test app is responding
                    echo "--- Testing App ---"
                    curl -s http://localhost:5000 && echo "✅ App is UP!" || echo "❌ App not responding"
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