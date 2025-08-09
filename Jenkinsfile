pipeline {
  agent any
  stages {
    stage('version') {
      steps {
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
        sh '''
        export PATH="/Users/cardze/miniforge3/bin:$PATH"
        echo $PATH
        conda --version
        conda activate base
        pytest --maxfail=1 --disable-warnings -q
        '''
      }
    }
    stage('test-performance') {
      steps {
        sh '''
        export PATH="/Users/cardze/miniforge3/bin:$PATH"
        echo $PATH
        conda --version
        conda activate base
        pytest --maxfail=1 --disable-warnings --durations=0 -q
        pytest --maxfail=1 --disable-warnings --durations=1 -q
        '''
      }
    }
  }
}