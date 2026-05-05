pipeline {

    agent any  // Run on any available Jenkins agent

    // ─── Global Variables ───────────────────────────────────────
    environment {
        GITHUB_CREDENTIALS = credentials('github-credentials')  // Jenkins saved credentials
        APP_NAME            = "my-python-app"
        DEPLOY_PORT         = "5000"
        PYTHON              = "python"
    }

    stages {

        // ─── STAGE 1 : CHECKOUT ──────────────────────────────────
        stage('Checkout') {
            steps {
                echo '========== Checking out code from GitHub =========='
                git(
                    url           : 'https://github.com/Rishabhgoyal0183/Python_Demo.git',
                    branch        : 'main',
                    credentialsId : 'github-credentials'   // must match what you saved in Jenkins
                )
                echo 'Code checked out successfully!'
            }
        }

        // ─── STAGE 2 : CLEAN ─────────────────────────────────────
        stage('Clean') {
            steps {
                echo '========== Cleaning old build files =========='
                script {
                    // Delete old virtual environment and build folders

                        sh '''
                            rm -rf venv
                            rm -rf dist
                            rm -rf build
                            rm -rf *.egg-info
                            find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
                            find . -name "*.pyc" -delete 2>/dev/null || true
                        '''
                                   }
                echo 'Clean completed!'
            }
        }

        // ─── STAGE 3 : BUILD ─────────────────────────────────────
       stage('Build') {
    steps {
        echo '========== Building the Application =========='
        sh '''
            # Create fresh virtual environment
            python3 -m venv venv

            # Activate and install dependencies
            . venv/bin/activate
            pip install --upgrade pip
            pip install -r requirements.txt
            pip install pytest build

            # Run Tests
            echo "--- Running Tests ---"
            pytest tests/ -v --junitxml=test-results.xml

            # Build Package
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

        // ─── STAGE 4 : DEPLOY ────────────────────────────────────
        stage('Deploy') {
    steps {
        echo '========== Deploying the Application =========='
        sh '''
            # Kill any old running instance
            pkill -f "gunicorn" || true

            # Wait 2 seconds
            sleep 2

            # Activate venv
            . venv/bin/activate

            # Start app with gunicorn in background
            nohup gunicorn -w 2 -b 0.0.0.0:5000 app.main:app > app.log 2>&1 &

            # Wait and confirm it started
            sleep 3
            echo "--- Checking if app is running ---"
            ps aux | grep gunicorn
            echo "App deployed at http://$(curl -s ifconfig.me):5000"
        '''
    }
}
}