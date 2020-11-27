from aws_cdk import (
    aws_ec2 as ec2, 
    aws_elasticloadbalancingv2 as elb, 
    core,
    aws_autoscaling as autoscaling
)

class NlbStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, vpc, nlb_listener_port, nlb_name, nlb_id, internet_facing, targetgroup_port, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        #network load balancer
        nlb = elb.NetworkLoadBalancer(
                self,
                internet_facing= internet_facing,
                load_balancer_name= nlb_name,
                id = nlb_id,
                vpc=vpc, # The object from above vpc from lookup
                vpc_subnets=ec2.SubnetSelection(subnets=vpc.public_subnets)
        )

        #load balancer scuirty group
        sg_nlb = ec2.SecurityGroup(
                self,
                id="sg_nlb",
                vpc=vpc,
                security_group_name="sg_nlb"
        )

        #listener 
        listener = nlb.add_listener("Listener", port=nlb_listener_port, protocol=elb.Protocol.TCP)
        target_group = elb.NetworkTargetGroup(self, vpc=vpc, id="Target", port=targetgroup_port)
        listener.add_target_groups("TargetGroup", target_group)

        #sg_nlb ingress
        sg_nlb.add_ingress_rule(
            peer=ec2.Peer.ipv4("0.0.0.0/0"),
            connection=ec2.Port.tcp(22)
        )
        core.Tag(key="Owner", value="Wahaj-nlb")