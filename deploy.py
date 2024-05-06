from aws_cdk import core
from aws_cdk.aws_amplify import CfnApp
from aws_cdk.aws_ec2 import Instance, InstanceType, SubnetType, Vpc, SecurityGroup, Peer, Port
from aws_cdk.aws_rds import DatabaseInstance, DatabaseInstanceEngine, InstanceType as RdsInstanceType, StorageType

class ThreeTierAppStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create VPC
        vpc = Vpc(self, 'MyVpc', max_azs=2)

        # Create Security Group for EC2 instance
        ec2_security_group = SecurityGroup(self, 'MyInstanceSecurityGroup',
                                           vpc=vpc,
                                           allow_all_outbound=True,  
                                           description='Security group for EC2 instance')

        ec2_security_group.add_ingress_rule(peer=Peer.any_ipv4(), connection=Port.tcp(80), description='Allow HTTP traffic')
        ec2_security_group.add_ingress_rule(peer=Peer.any_ipv4(), connection=Port.tcp(22), description='Allow SSH connection')

        # Create RDS MySQL Database
        rds_security_group = SecurityGroup(self, 'MyRDSSecurityGroup',
                                           vpc=vpc,
                                           allow_all_outbound=True,
                                           description='Security group for RDS instance')

        rds_database = DatabaseInstance(self, 'MyRDSInstance',
                                         engine=DatabaseInstanceEngine.mysql(version='5.7'),
                                         instance_type=RdsInstanceType.of(instance_class='t2.micro', instance_size='micro'),
                                         vpc=vpc,
                                         vpc_subnets=SubnetType.ISOLATED,  # Or use appropriate subnet type
                                         security_groups=[rds_security_group],
                                         storage_type=StorageType.GP2,  # Specify the storage type
                                         allocated_storage=20)  # Specify the allocated storage in GB

        # Add inbound rule to allow MySQL traffic from EC2 instance to RDS instance
        rds_security_group.add_ingress_rule(peer=ec2_security_group, connection=Port.tcp(3306), description='Allow inbound MySQL traffic')

        # Create EC2 instance for backend
        backend_instance = Instance(self, 'MyBackendInstance',
                                    instance_type=InstanceType.of(instance_class='t2.micro', instance_size='micro'),
                                    machine_image=ami-053a617c6207ecc7b,  # You need to replace this with a valid AMI ID
                                    vpc=vpc,
                                    vpc_subnets=SubnetType.PUBLIC,
                                    security_group=ec2_security_group)

        # Create Amplify frontend
        amplify_app = CfnApp(self, 'MyAmplifyApp',
                             name='my-test-amplify-app',
                             repository='https://github.com/my/repo.git',  # GitHub repository URL
                             oauth_token='YOUR_GITHUB_OAUTH_TOKEN',  # OAuth token for GitHub authentication
                             build_spec='build.yml')

app = core.App()
ThreeTierAppStack(app, "ThreeTierAppStack")
app.synth()
