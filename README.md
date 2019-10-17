"# Serverless example to build a data pipeline using SQS, Lambda, DynamoDB and S3"
The application receives user data from an SQS queue. Lambda function polls the queue and processes the messages in batches.
Every item is parsed and stored into DynamoDB.

The application can also be used to export data from DynamoDB into S3 using another Lambda function.
In this case, this export is needed only once a day and hence Cloudwatch can be configured to invoke the lambda once a day.

 
