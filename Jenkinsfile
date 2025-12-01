pipeline{
    agent any

    environment {
        AWS_REGION = 'us-east-1'
        ECR_REPO = 'medical-rag'
        IMAGE_TAG = 'latest'
	}

    stages{
        stage('Cloning Github repo to Jenkins'){
            steps{
                script{
                    echo 'Cloning Github repo to Jenkins............'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/andela-Taiwo/Medical-RAG-Bot.git']])
                }
            }
        }


    stage('Build and Push Docker Image to ECR') {
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: 'aws-token',
                    accessKeyVariable: 'AWS_ACCESS_KEY_ID',
                    secretKeyVariable: 'AWS_SECRET_ACCESS_KEY'
                ]]) {
                    script {
                        // Ensure Docker daemon is running (DinD)
                        def accountId = sh(script: "aws sts get-caller-identity --query Account --output text", returnStdout: true).trim()
                        sh 'ps aux | grep dockerd || dockerd &'
                        sleep 10
                        
                        // Login to ECR
                        sh """
                            aws ecr get-login-password --region ${AWS_REGION} | \
                            docker login --username AWS --password-stdin  ${accountId}.dkr.ecr.${AWS_REGION}.amazonaws.com
                        """
                        
                        // Build and push
                        sh """
                            docker build -t ${accountId}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO}:${IMAGE_TAG} .
                            docker push ${accountId}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO}:${IMAGE_TAG}
                        """
                    }
                }
            }
        }

    stage('Deploy to ECS Fargate') {
    steps {
        withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-token']]) {
            script {
                sh """
                aws ecs update-service \
                  --cluster medical-rag-bot \
                  --service medical-rag-bot-def-service-85n6xyip \
                  --force-new-deployment \
                  --region ${AWS_REGION}
                """
                }
            }
        }
     }
    }
}