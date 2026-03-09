pipeline{
    agent any

    stages {

        stage('Clean Workspace') {
            steps {
                deleteDir()  // This deletes all files in the current workspace
            }
        }

        stage("Clone Repo"){
            steps{
                git branch: 'main', url: 'https://github.com/chukkaladhanya/fastapi_jenkins.git'
            }
        }

        stage("install dependencies"){
            steps{
                    sh '''
                        python3 -m venv venv
                        . venv/bin/activate
                        pip install --upgrade pip
                        pip install -r requirements.txt
                    '''
            }
        }

        stage("run test cases"){
            steps{
                sh '''
                . venv/bin/activate
                pytest'''
            }
        }
    }
}