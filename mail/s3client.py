import os
import io
import boto3


s3_client = boto3.client(
    's3',
    endpoint_url=os.environ.get('AWS_ENDPOINT_URL'),
    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
    region_name='ams3',
)

def upload_file_to_s3(
        local_file_path,
        s3_path,
        bucket_name=os.environ.get('AWS_BUCKET_NAME'),
        acl=os.environ.get('AWS_ACL')
):

    with open(local_file_path, 'rb') as f:
        file = io.BytesIO(f.read())

    s3_client.upload_fileobj(
        file,
        bucket_name,
        s3_path,
        ExtraArgs={
            'ACL': acl
        }
    )
