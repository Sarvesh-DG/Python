import boto3
from moto import mock_dynamodb2
from src.boto3_example import DynamodBExample


@mock_dynamodb2
def test_create_dynamo_table():
    '''
        Implement the test logic here for testing create_dynamo_table method
    '''
    assert False


@mock_dynamodb2
def test_add_dynamo_record_table():
    '''
        Implement the test logic here for testing add_dynamo_record_table method
    '''
    assert False

@mock_dynamodb2
def test_add_dynamo_record_table_failure():
    '''
        Implement the test logic here test_add_dynamo_record_table method for failures
    '''
    assert False
