The deploy.py file contains aws cdk to deploy a 3-tier application. using aws amplify to host the frontend, an ec2 instance for the backend and aws rds using mysql as the engine.

Setup environment: ensure you have the necessary Python dependencies installed. If not, you can install them using pip: 

pip install aws-cdk.core aws-cdk.aws-amplify aws-cdk.aws-ec2 aws-cdk.aws-rds

To deploy the application run: cdk deploy, this command will create a VPC, RDS MySQL database, EC2 instance for the backend, and an Amplify frontend linked to your GitHub repository
