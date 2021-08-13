import json
import random

def lambda_handler(event, context):
    # TODO implement
    roll = random.randint(0,10)
    o = event['origin']
    map= event['db']['mapa']
    if roll <=5:
        payload= map.replace("Tipo", o['tipo'],1)
        payload= payload.replace("Monto", o['monto'])
        print(payload)
        return payload
    elif roll >= 6:
        return "la transaccion fallo en el servidor destino"