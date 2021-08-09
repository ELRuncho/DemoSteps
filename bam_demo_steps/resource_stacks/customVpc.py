from aws_cdk import core as cdk


class CustomVPCStack():

    def __init__(self, scope: cdk.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

