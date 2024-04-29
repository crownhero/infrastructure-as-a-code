from aws_cdk import core
from aws_cdk.aws_amplify import CfnApp
from aws_cdk.aws_ec2 import Instance, InstanceType, SubnetType, Vpc
from aws_cdk.aws_rds import DatabaseInstance, DatabaseInstanceEngine, InstanceType as RdsInstanceType
from aws_cdk.aws_ec2 import SecurityGroup, Peer, Port

class ThreeTierAppStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create VPC
        vpc = Vpc(self, 'MyVpc', max_azs=2)

        security_group = SecurityGroup(self, 'MyInstanceSecurityGroup',
                                       vpc=vpc,
                                       allow_all_outbound=True,  
                                       description='Security group for EC2 instance')

        security_group.add_ingress_rule(peer=Peer.any_ipv4(), connection=Port.tcp(80), description='Allow HTTP traffic')
        security_group.add_ingress_rule(peer=Peer.any_ipv4(), connection=Port.tcp(22), description='Allow SSH connection')
        
        # Create RDS MySQL Database
        rds_database = DatabaseInstance(self, 'MyRDSInstance',
                                         engine=DatabaseInstanceEngine.mysql(version='5.7'),
                                         instance_type=RdsInstanceType.of(instance_class='t2.micro', instance_size='micro'),
                                         vpc=vpc)

        # Create EC2 instance for backend
        backend_instance = Instance(self, 'MyBackendInstance',
                                    instance_type=InstanceType.of(instance_class='t2.micro', instance_size='micro'),
                                    machine_image=ami-08447c25f2e9dc66c,  # You need to replace this with a valid AMI ID
                                    vpc=vpc,
                                    vpc_subnets=SubnetType.PUBLIC,
                                    security_group=security_group)  

        # Create Amplify frontend
        amplify_app = CfnApp(self, 'MyAmplifyApp',
                             name='my-test-amplify-app',
                             repository='https://github.com/my/repo.git',  # GitHub repository URL
                             oauth_token='YOUR_GITHUB_OAUTH_TOKEN',  # OAuth token for GitHub authentication
                             build_spec='build.yml')  

app = core.App()
ThreeTierAppStack(app, "ThreeTierAppStack")
app.synth()
