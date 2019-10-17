import boto3
import json
import decimal


def lambda_handler(event, context):
    # Helper class to convert a DynamoDB item to JSON.
    class DecimalEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, decimal.Decimal):
                if abs(o) % 1 > 0:
                    return float(o)
                else:
                    return int(o)
            return super(DecimalEncoder, self).default(o)
    
    data = json.loads(event['Records'][0]['body'])
    
    timestamp = data['timestamp'];
    user_id = data['userId'];
    info = data['info'];
        
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('Users')
    
    response = table.put_item(
    Item={
        'EntryCreationTime': timestamp,
        'UserId': user_id,
        'Info': info
        }
    )
    
    print("PutItem succeeded:")
    print(json.dumps(response, indent=4, cls=DecimalEncoder))
    
    return {
        'statusCode': 200,
        'body': json.dumps('Done')
    }
    
    
