pipeline{
    agent any

    stages {

        stage("Clone Repo"){
            steps{
                git 'https://github.com/chukkaladhanya/fastapi_jenkins.git'
            }
        }

        stage("install dependencies"){
            steps{
                sh 'pip install -r requirements.txt'
            }
        }

        stage("run test cases"){
            steps{
                sh 'pytest'
            }
        }

        stage("start fastapi application"){
            steps{
                sh 'uvicorn main:app --host 0.0.0.0 --port 8000'
            }
        }
    }
}