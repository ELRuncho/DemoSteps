from aws_cdk import (core as cdk,
                        aws_apigateway as _apigateway,
                        aws_lambda as _lambda,
                        aws_dynamodb as dynamodb)

class BamDemoStepsStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        catalogo = dynamodb.Table(self, 
            "Catalogo",
            partition_key=dynamodb.Attribute(name="TipoTransaccion", type=dynamodb.AttributeType.STRING)
        )

        consultaCatalogo = _lambda.Function(self,
                                            "consultorCatalogo",
                                            runtime=_lambda.Runtime.PYTHON_3_8,
                                            code=_lambda.Code.from_asset("resources"),
                                            handler="consultorCatalogo.handler"
                                            )
        traductorxml = _lambda.Function(self, 
                                        "traductorxml",
                                        runtime=_lambda.Runtime.PYTHON_3_8,
                                        handler="traductorxml.handler"
                                        )



