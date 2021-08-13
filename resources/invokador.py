import json
from os import environ
import boto3

sfnClient = boto3.client('stepfunctions')
sfnArn = environ.get('SFNARN') 
def lambda_handler(event, context):
    # TODO implement
    payload = json.loads(event['body'])

    try:
        sfnClient.start_execution(
            stateMachineArn=sfnArn,
            input=event['body']
        )
        return {'statusCode':200, 'body':json.dumps('Se esta procesando el Pago')}
    except:
        return {'statusCode':500, 'body':json.dumps('hubo un error')}