pipeline {
    agent any

    environment {
        AWS_REGION = 'us-east-1'
        ECR_REPO = 'medical-rag'
        IMAGE_TAG = 'latest'
        ECR_REGISTRY = '313901886195.dkr.ecr.us-east-1.amazonaws.com'
        SERVICE_NAME = 'llmops-medical-service'
        SERVICE_REGION = 'us-east-1'
    }
    stages {
        stage('Clone GitHub Repo') {
            steps {
                script {
                    echo 'Cloning GitHub repo to Jenkins...'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/andela-Taiwo/Medical-RAG-Bot.git']])
                }
            }
        }

        // stage('Build and Push Docker Image to ECR') {
        //     steps {
        //         withCredentials([[
        //             $class: 'AmazonWebServicesCredentialsBinding',
        //             credentialsId: 'aws-token',
        //             accessKeyVariable: 'AWS_ACCESS_KEY_ID',
        //             secretKeyVariable: 'AWS_SECRET_ACCESS_KEY'
        //         ]]) {
        //             script {
        //                 // Ensure Docker daemon is running (DinD)
        //                 sh 'ps aux | grep dockerd || dockerd &'
        //                 sleep 10
                        
        //                 // Login to ECR
        //                 sh """
        //                     aws ecr get-login-password --region ${AWS_REGION} | \
        //                     docker login --username AWS --password-stdin ${ECR_REGISTRY}
        //                 """
                        
        //                 // Build and push
        //                 sh """
        //                     docker build -t ${ECR_REGISTRY}/${ECR_REPO}:${IMAGE_TAG} .
        //                     docker push ${ECR_REGISTRY}/${ECR_REPO}:${IMAGE_TAG}
        //                 """
        //             }
        //         }
        //     }
        // }


        stage('Build, Scan, and Push Docker Image to ECR') {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-token']]) {
                    script {
                        def accountId = sh(script: "aws sts get-caller-identity --query Account --output text", returnStdout: true).trim()
                        def ecrUrl = "${accountId}.dkr.ecr.${env.AWS_REGION}.amazonaws.com/${env.ECR_REPO}"
                        def imageFullTag = "${ecrUrl}:${IMAGE_TAG}"

                        sh """
                        aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ecrUrl}
                        docker build -t ${env.ECR_REPO}:${IMAGE_TAG} .
                        trivy image --severity HIGH,CRITICAL --format json -o trivy-report.json ${env.ECR_REPO}:${IMAGE_TAG} || true
                        docker tag ${env.ECR_REPO}:${IMAGE_TAG} ${imageFullTag}
                        docker push ${imageFullTag}
                        """

                        archiveArtifacts artifacts: 'trivy-report.json', allowEmptyArchive: true
                    }
                }
            }
        }

        

        stage('Deploy to AWS App Runner') {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-token']]) {
                    script {
                        def accountId = sh(script: "aws sts get-caller-identity --query Account --output text", returnStdout: true).trim()
                        def ecrUrl = "${accountId}.dkr.ecr.${env.AWS_REGION}.amazonaws.com/${env.ECR_REPO}"
                        def imageFullTag = "${ecrUrl}:${IMAGE_TAG}"

                        echo "Triggering deployment to AWS App Runner..."

                        sh '''
                        # Deploy or update App Runner service
                        SERVICE_ARN=$(aws apprunner list-services \
                            --query "ServiceSummaryList[?ServiceName=='llmops-medical-service'].ServiceArn" \
                            --output text 2>/dev/null || echo "")
                        
                        if [ -z "$SERVICE_ARN" ]; then
                            echo "Creating App Runner service..."
                            aws apprunner create-service \
                                --service-name llmops-medical-service \
                                --source-configuration '{
                                    "AuthenticationConfiguration": {
                                        "AccessRoleArn": "${APP_RUNNER_ROLE}"
                                    },
                                    "ImageRepository": {
                                        "ImageIdentifier": "${ECR_REPO}:latest",
                                        "ImageRepositoryType": "ECR"
                                    }
                                }' \
                                --instance-configuration '{
                                    "Cpu": "1 vCPU",
                                    "Memory": "2 GB"
                                }'
                        else
                            echo "Updating App Runner service..."
                            aws apprunner update-service \
                                --service-arn "$SERVICE_ARN" \
                                --source-configuration '{
                                    "ImageRepository": {
                                        "ImageIdentifier": "${ECR_REPO}:latest"
                                    }
                                }'
                        fi
                        
                        echo "✅ Deployment initiated"

                        aws apprunner start-deployment --service-arn \$SERVICE_ARN --region ${AWS_REGION}
                        '''
                    }
                }
            }
        }
    }
}