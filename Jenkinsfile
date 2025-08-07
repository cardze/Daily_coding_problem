pipeline {
    agent {
      docker {
        image 'python:3'
        label 'my-build-agent'
      }
    }
    stages {
        stage('Test') {
            steps {
              sh """
              pip install -r requirements.txt
              pytest test.py
              """
            }
        }
    }
}