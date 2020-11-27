from aws_cdk import core
import aws_cdk.aws_ec2 as ec2


class CustomVpcStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, cidr_vpc, cidr_mask, nat_gateways, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here

        self.vpc = ec2.Vpc(self, "VPC",
                           max_azs=2,
                           cidr=cidr_vpc,
                           # configuration will create 3 groups in 2 AZs = 6 subnets.
                           subnet_configuration=[ec2.SubnetConfiguration(
                               subnet_type=ec2.SubnetType.PUBLIC,
                               name="Public",
                               cidr_mask=cidr_mask
                           ), ec2.SubnetConfiguration(
                               subnet_type=ec2.SubnetType.PRIVATE,
                               name="Private",
                               cidr_mask=cidr_mask
                           )
                           ],
                           # nat_gateway_provider=ec2.NatProvider.gateway(),
                           nat_gateways=nat_gateways,
                           )
                           
        core.Tag(key="Owner", value="Wahaj-vpc")
        core.CfnOutput(self, "Output",
                       value=self.vpc.vpc_id)