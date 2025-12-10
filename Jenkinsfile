pipeline {
  agent any
  stages {
    stage('version') {
      steps {
        sh 'python3 --version'
      }
    }
    stage('hello') {
      steps {
        sh 'python3 hello.py'
      }
    }
    stage('test') {
      steps {
        sh 'python3 -m pytest --maxfail=1 --disable-warnings -q'
      }
    }
    stage('test-performance') {
      steps {
        sh '''
        python3 -m pytest --maxfail=1 --disable-warnings --durations=0 -q
        python3 -m pytest --maxfail=1 --disable-warnings --durations=1 -q
        '''
      }
    }
  }
}