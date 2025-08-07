pipeline{

  agent any

  stages {
    stage("build"){
      steps{
        sh "pip install pytest"
      }
    }
    stage("test"){
      steps{
        sh "pytest test.py"
      }
    }
  }
  

}
