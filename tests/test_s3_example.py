import boto3
import pytest
from moto import mock_s3
from botocore.exceptions import ParamValidationError
from src.boto3_example import S3Example


@mock_s3
def test_my_model_save():
    conn = boto3.resource('s3', region_name='us-east-1')
    # We need to create the bucket since this is all in Moto's 'virtual' AWS account
    conn.create_bucket(Bucket='mybucket')

    model_instance = S3Example('mybucket', 'steve', 'is awesome')
    model_instance.save()

    body = conn.Object('mybucket', 'steve').get()['Body'].read().decode("utf-8")

    assert body == 'is awesome'


@mock_s3
def test_s3_save_failure():
    conn = boto3.resource('s3', region_name='us-east-1')

    with pytest.raises(ParamValidationError):
        # We need to create the bucket since this is all in Moto's 'virtual' AWS account
        conn.create_bucket(Bucket='mybucket')

        model_instance = S3Example('mybucket/', 'steve', 'is awesome') # Intentionally passing invalid bucket name so that boto3 raises an error
        model_instance.save()