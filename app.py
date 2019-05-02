import json
from troposphere import Tags, Template, Ref, Output

from troposphere import ec2

class App():

    def __init__(self, raw_data):
        self.data = None
        self.resources = {}
        self.outputs = {}
        self.template = Template()
        self.load_data(raw_data)


    def load_data(self, raw_data):
        try:
            self.data = json.loads(raw_data)
        except:
            print ("Error loading data from file")


    def generate_template(self):
        data = self.data

        self.header()
        resources = data["Resources"]
        outputs = data["Outputs"]

        if len(resources) > 0:
            self.load_resources(resources)

        if len(outputs) > 0:
            self.add_outputs(outputs)

        template = self.template.to_json()
        return template


    def print_template(self):
        # write a json file with template contents
        template = self.template.to_json()
        return template


    def header(self):
        data = self.data
        environtment_name = data["Metadata"]["Environment"]

        self.template.set_version("2010-09-09")
        self.template.set_description("Service VPC")
        self.template.set_metadata({
            "DependsOn": [],
            "Environment": environtment_name,
            "StackName": environtment_name+"-VPC"
        })


    def load_resources(self, resources):
        # add resources to template dynamically
        for label, data in resources.items():
            resource_type = data["Type"].split("::")[-1]
            if resource_type == "InternetGateway":
                self.add_InternetGateway(label, data)

            if resource_type == "VPC":
                self.add_VPC(label, data)

            if resource_type == "VPCGatewayAttachment":
                self.add_VPCGatewayAttachment(label, data)

            if resource_type == "NetworkAcl":
                self.add_NetworkAcl(label, data)

            if resource_type == "NetworkAclEntry":
                self.add_NetworkAclEntry(label, data)


    def get_tags(self, props):
        tags = {}
        for item in props["Tags"]:
            tags[item["Key"]] = item["Value"]

        return tags


    def add_VPC(self, label, raw_props):
        tags = self.get_tags(raw_props["Properties"])

        res = self.template.add_resource(
            ec2.VPC(
                'VPC',
                CidrBlock='10.0.0.0/16',
                EnableDnsHostnames='true',
                EnableDnsSupport='true',
                InstanceTenancy='default',
                Tags=Tags(tags)))
        self.resources[label] = res


    def add_VPCGatewayAttachment(self, label, raw_props):
        vpc_ref = self.resources["VPC"]
        inetGateWay_ref = self.resources["InternetGateway"]

        res = self.template.add_resource(
            ec2.VPCGatewayAttachment(
            label,
            VpcId=Ref(vpc_ref),
            InternetGatewayId=Ref(inetGateWay_ref),
        ))

        self.resources[label] = res


    def add_NetworkAcl(self, label, raw_props):
        tags = self.get_tags(raw_props["Properties"])
        vpc_ref = self.resources["VPC"]

        res = self.template.add_resource(
            ec2.NetworkAcl(
                label,
                VpcId=Ref(vpc_ref),
                Tags=Tags(tags)))

        self.resources[label] = res


    def add_NetworkAclEntry(self, label, raw_props):
        props = raw_props["Properties"]
        vpc_netAcl_ref = self.resources["VpcNetworkAcl"]

        if "PortRange" in props:
            port_range=ec2.PortRange(
                To=props["PortRange"]["To"],
                From=props["PortRange"]["From"])
        else:
           port_range=ec2.PortRange(
                To=False,
                From=False)

        res = self.template.add_resource(
            ec2.NetworkAclEntry(
                label,
                CidrBlock=props["CidrBlock"],
                Egress=props["Egress"],
                NetworkAclId=Ref(vpc_netAcl_ref),
                PortRange=port_range,
                Protocol=props["Protocol"],
                RuleAction=props["RuleAction"],
                RuleNumber=props["RuleNumber"],
            ))

        self.resources[label] = res


    def add_InternetGateway(self, label, raw_props):
        tags = self.get_tags(raw_props["Properties"])
        res = self.template.add_resource(
            ec2.InternetGateway(
                label,
                Tags=Tags(tags)))
        self.resources[label] = res


    def add_outputs(self, raw_outputs):
        for label, data in raw_outputs.items():
            data_ref = data["Value"]["Ref"]
            ref_output = self.resources[data_ref]
            self.template.add_output(
                Output(
                    label,
                    Value=Ref(ref_output)
                ))

