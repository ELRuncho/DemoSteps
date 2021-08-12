from aws_cdk import (core as cdk,
                        aws_apigateway as _apigateway,
                        aws_lambda as _lambda,
                        aws_dynamodb as dynamodb,
                        aws_stepfunctions as sfn,
                        aws_stepfunctions_tasks as sfntasks)

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
                                            handler="consultorCatalogo.lambda_handler"
                                            )
        traductorxml = _lambda.Function(self, 
                                        "traductorxml",
                                        runtime=_lambda.Runtime.PYTHON_3_8,
                                        code=_lambda.Code.from_asset("resources"),
                                        handler="traductorxml.lambda_handler"
                                        )

        catalogo.grant_read_data(consultaCatalogo)

        #----------------------------------------------------------------
        # defining sfn tasks and flow
        #----------------------------------------------------------------
        consultar_catalogo = sfntasks.LambdaInvoke(
                                                    self, 
                                                    "consultar",
                                                    lambda_function=consultaCatalogo,
                                                    output_path="$.Payload"
                                                    )
        
        traducirYenviar_pago = sfntasks.LambdaInvoke(
                                                    self,
                                                    "Traducir_y_enviar",
                                                    lambda_function=traductorxml,
                                                    input_path="$.guid",
                                                    output_path="$.Payload"
                                                    )
        

        sfn_definition = consultar_catalogo.next(traducirYenviar_pago).next(sfn.Choice(self, "Completado"))

        sfn.StateMachine(self, 
                        "ProcesoPagos",
                        definition=sfn_definition)

        api = _apigateway.RestApi(
                    self,
                    "pagos-api",
                    rest_api_name="Pagos",
                    description="esta API procesa servicios de pagos"
                )
        api_integration = _apigateway.LambdaIntegration(consultaCatalogo,
                                request_templates = {"application/json": '{"statusCode":"200"}'}
                                )

        api.root.add_method("POST",api_integration)




