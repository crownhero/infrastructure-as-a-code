Deploy.py for 3-Tier Application Deployment

Overview:
The deploy.py script contains AWS CDK code to facilitate the deployment of a 3-tier application. This application comprises an Amplify frontend, an EC2 instance serving as the backend, and an AWS RDS MySQL database.

Setup Environment:
Before proceeding with deployment, ensure that the required Python dependencies are installed. If not, use pip to install them:

pip install aws-cdk.core aws-cdk.aws-amplify aws-cdk.aws-ec2 aws-cdk.aws-rds

Deployment Process:
To initiate the deployment process, execute the following command:

cdk deploy

This command automates the creation of the following components:

Virtual Private Cloud (VPC): Hosting environment for the application's components.
AWS RDS MySQL Database: Storage for application data.
EC2 Instance: Backend logic implementation.
Amplify Frontend: Linked to the specified GitHub repository.
