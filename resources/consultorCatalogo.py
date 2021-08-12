import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('BamDemoStepsStack-Catalogo61A2213A-2W2J065BGE26') 
def lambda_handler(event, context):
    # TODO implement
    payload = json.loads(event['body'])
    response = table.get_item(
        Key={
                'TipoTransaccion': payload['tipo']
        }
    )
    item = response['Item']
    
    return item