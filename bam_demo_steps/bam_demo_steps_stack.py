from aws_cdk import (core as cdk,
                        aws_apigateway as _apigateway,
                        aws_lambda as _lambda,
                        aws_dynamodb as dynamodb,
                        aws_stepfunctions as sfn,
                        aws_stepfunctions_tasks as sfntasks,
                        aws_sns as sns,
                        aws_sns_subscriptions as snsSubs)

class BamDemoStepsStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        topic = sns.Topic(self, "FinalProceso",
            display_name="Proceso pago completado"
        )
        topic.add_subscription(snsSubs.EmailSubscription(email_address='raffran@amazon.com'))

        catalogo = dynamodb.Table(self, 
            "Catalogo",
            partition_key=dynamodb.Attribute(name="TipoTransaccion", type=dynamodb.AttributeType.STRING)
        )

        

        consultaCatalogo = _lambda.Function(self,
                                            "consultorCatalogo",
                                            runtime=_lambda.Runtime.PYTHON_3_8,
                                            code=_lambda.Code.from_asset("resources"),
                                            handler="consultorCatalogo.lambda_handler",
                                            environment={
                                                'TABLE_NAME': catalogo.table_name
                                            }
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

        completado = sfn.Succeed(self, "lo logramos!")

        fallo1 = sfn.Fail(self, "No existe el tipo",
            error="Tipo de Pago",
            cause = "No existe el tipo de pago"
        )

        fallo2 = sfn.Fail(self,"fallo traduccion",
            error="traduccion",
            cause="algo salio mal en el traductor"
        )

        fallo_en_catalogo = sfntasks.SnsPublish(
                                self,
                                "No_se_econtro_tipo_de_pago",
                                topic=topic,
                                message=sfn.TaskInput.from_text("no se encontro el tipo de pago"),
                                subject="fallo el proceso de pago"
                            ).next(fallo1)

        fallo_en_traduccion = sfntasks.SnsPublish(
                                self,
                                "No_se_completo_transaccion",
                                topic=topic,
                                message=sfn.TaskInput.from_text("algo salio mal con el pago"),
                                subject="fallo el proceso de pago"
                            ).next(fallo2)

        consultar_catalogo = sfntasks.LambdaInvoke(
                                                    self, 
                                                    "consultarCatalogo",
                                                    lambda_function=consultaCatalogo,
                                                    output_path="$.Payload"
                                                    ).add_catch(fallo_en_catalogo)
        
        traducirYenviar_pago = sfntasks.LambdaInvoke(
                                                    self,
                                                    "Traducir_y_enviar",
                                                    lambda_function=traductorxml,
                                                    input_path="$.guid",
                                                    output_path="$.Payload"
                                                    ).add_catch(fallo_en_traduccion)

        sfn_definition = sfn.Chain.start(consultar_catalogo).next(traducirYenviar_pago).next(completado)

        Machine = sfn.StateMachine(self, 
                        "ProcesoPagos",
                        definition=sfn_definition,)

        invokadorSfn = _lambda.Function(self,
                                            "invokadorSFN",
                                            runtime=_lambda.Runtime.PYTHON_3_8,
                                            code=_lambda.Code.from_asset("resources"),
                                            handler="invokador.lambda_handler",
                                            environment={
                                                'SFNARN': Machine.state_machine_arn
                                            }
                                            )

        Machine.grant_start_execution(invokadorSfn)

        api = _apigateway.RestApi(
                    self,
                    "pagos-api",
                    rest_api_name="Pagos",
                    description="esta API procesa servicios de pagos"
                )
        api_integration = _apigateway.LambdaIntegration(invokadorSfn,
                                request_templates = {"application/json": '{"statusCode":"200"}'}
                                )

        api.root.add_method("POST",api_integration)




