import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Catalogo') 
def lambda_handler(event, context):
    # TODO implement
    try:
        response = table.get_item(
            Key={
                'TipoTransaccion': event['tipo']
            }
        )
        item = response['Item']
    except Exception as e:
        item = e

    
    return item#{
        #'statusCode': 200,
        #'body': json.dumps('Hello from Lambda!')
    #}