import json

def handle(event, context):

    body = "Yoo, what's good Lambda?"
    statusCode = 200

    return {
        'statusCode': statusCode,
        'body': json.dumps(body)
    }