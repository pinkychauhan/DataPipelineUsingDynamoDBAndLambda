import boto3
import json
import csv
import io
from datetime import date, datetime, timedelta
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    
    csv_io = io.StringIO()
    csv_file = csv.writer(csv_io,delimiter=',')

    # writing the column names
    csv_file.writerow(["EntryCreationTime", "UserId", "Info"])
    
    # get records from the previous day from DynamoDB
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('Users')
    
    yesterday = date.today() - timedelta(days = 1)
    print(yesterday)
    
    timestamp_lowerbound = str(yesterday) + ' 00:00:00.000000';
    timestamp_upperbound = str(yesterday) + ' 23:59:59.999999';
    
    filter_expression = Key('EntryCreationTime').between(timestamp_lowerbound, timestamp_upperbound)
    projection_expression = "EntryCreationTime, UserId, Info"
   
    response = table.scan(
        FilterExpression=filter_expression,
        ProjectionExpression=projection_expression
        )
    for item in response['Items']:
        csv_file.writerow([item['EntryCreationTime'],
                           item['UserId'],
                           item['Info']
                           ])
    
    while 'LastEvaluatedKey' in response:
        response = table.scan(
            ProjectionExpression=projection_expression,
            FilterExpression=filter_expression,
            ExclusiveStartKey=response['LastEvaluatedKey']
            )
        for item in response['Items']:
            csv_file.writerow([item['EntryCreationTime'],
                           item['UserId'],
                           item['Info']
                           ])

    # upload csv to s3
    file_name = 'report' + str(yesterday) + '.csv'
    client = boto3.client('s3')
    client.put_object(Body=csv_io.getvalue(), 
                        Bucket='users', 
                        Key=file_name)

    return {
        'statusCode': 200,
        'body': json.dumps('Done!')
    }








