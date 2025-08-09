pipeline {
  agent any
  stages {
    stage('version') {
      steps {
        sh 'source ~/.zshrc'
        sh 'conda activate base'
        sh 'python --version'
      }
    }
    stage('hello') {
      steps {
        sh 'python hello.py'
      }
    }
    stage('test') {
      steps {
        sh 'pytest --maxfail=1 --disable-warnings -q'
      }
    }
    stage('test-performance') {
      steps {
        sh 'pytest --maxfail=1 --disable-warnings --durations=0 -q'
        sh 'pytest --maxfail=1 --disable-warnings --durations=1 -q'
      }
    }
  }
}