#!/usr/bin/env python3
from aws_cdk import core

from cdk.nlb_stack import NlbStack
from cdk.vpc_stack import CustomVpcStack
import os

class Finexio(core.App):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #Nlb env
        nlb_listener_port = self.get_nlb_config("listener_port")
        nlb_name = self.get_nlb_config("load_balancer_name")
        nlb_id = self.get_nlb_config("id")
        internet_facing = self.get_nlb_config("internet_facing") 
        targetgroup_port = self.get_nlb_config("targetgroup_port") 


        #vpc env
        cidr_vpc = self.get_vpc_config("vpc_cidr")
        cidr_mask = self.get_vpc_config("cidr_mask")
        nat_gateways = self.get_vpc_config("nat_gateways")


        stack_vpc = CustomVpcStack(
                self,
                "vpc",
                env={
                'account': os.environ['CDK_DEFAULT_ACCOUNT'], 
                'region': os.environ['CDK_DEFAULT_REGION']
                },
                cidr_vpc=cidr_vpc,
                cidr_mask=cidr_mask,
                nat_gateways=nat_gateways
        )
        NlbStack(
                self,
                "nlb",
                env={
                'account': os.environ['CDK_DEFAULT_ACCOUNT'], 
                'region': os.environ['CDK_DEFAULT_REGION'],
                },
                internet_facing=internet_facing,
                nlb_name=nlb_name,
                nlb_listener_port=nlb_listener_port,
                nlb_id=nlb_id,
                targetgroup_port=targetgroup_port,
                vpc=stack_vpc.vpc
        )

    def get_nlb_config(self, attribute):
        return self.node.try_get_context('Nlb').get(attribute)

    def get_vpc_config(self, attribute):
        return self.node.try_get_context('VPC').get(attribute)

Finexio().synth()