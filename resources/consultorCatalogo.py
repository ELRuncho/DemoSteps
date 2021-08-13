import json
from os import environ
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(environ.get('TABLE_NAME')) 
def lambda_handler(event, context):
    # TODO implement
    payload = json.loads(event['body'])
    try:
        response = table.get_item(
            Key={
                'TipoTransaccion': payload['tipo']
            }
        )
        item = response['Item']
    except Exception as e:
        item = e
    
    return item