import boto3


class S3Example(object):
    def __init__(self, bucket_name, name, value):
        self.bucket_name = bucket_name
        self.name = name
        self.value = value

    def save(self):
        s3 = boto3.client('s3', region_name='us-east-1')
        s3.put_object(Bucket=self.bucket_name, Key=self.name, Body=self.value)


class DynamodBExample(object):
    def __init__(self):
        print('Initializing class')

    def create_movies_table(self) -> None:
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

        table = dynamodb.create_table(
            TableName='Movies',
            KeySchema=[
                {
                    'AttributeName': 'year',
                    'KeyType': 'HASH'  # Partition key
                },
                {
                    'AttributeName': 'title',
                    'KeyType': 'RANGE'  # Sort key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'year',
                    'AttributeType': 'N'
                },
                {
                    'AttributeName': 'title',
                    'AttributeType': 'S'
                },

            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )

    def add_dynamo_record(self, table_name: str, item: str) -> None:
        dynamo_resource = boto3.resource('dynamodb', region_name='us-east-1')

        table = dynamo_resource.Table(table_name)

        table.put_item(
            Item=item
        )
