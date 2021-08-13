import json
from os import environ
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(environ.get('TABLE_NAME')) 
def lambda_handler(event, context):
    # TODO implement
    response={}

    try:
        responsedb = table.get_item(
            Key={
                'TipoTransaccion': event['tipo']
            }
        )

        response['origin']=event
        response['db']= responsedb['Item']

        return response
        
    except:
        raise Exception ("Registro no encontrado")