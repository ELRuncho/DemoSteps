import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('BamDemoStepsStack-Catalogo61A2213A-2W2J065BGE26') 
def lambda_handler(event, context):
    # TODO implement
    response = table.get_item(
        Key={
                'TipoTransaccion': event['body']['tipo']
        }
    )
    item = response['Item']
    print(item)
    return json.dumps(item)#{
        #'statusCode': 200,
        #'body': json.dumps('Hello from Lambda!')
    #}