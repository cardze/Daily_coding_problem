pipeline{

  agent any

  stages {

    stage('Install Python Dependencies') {
                steps {
                    sh '''
                        # Install pip if not present (e.g., in a minimal Docker image)
                        apt-get update && apt-get install -y python3 python3-pip

                        # Install project dependencies
                        pip install -r requirements.txt
                    '''
                }
            }

    stage("test"){
      steps{
        sh "pytest test.py"
      }
    }
  }
  

}
