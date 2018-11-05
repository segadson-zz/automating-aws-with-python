import boto3
import click
from botocore.exceptions import ClientError

session = boto3.Session(profile_name='pythonAutomation')
s3 = session.resource('s3')

@click.group()
def cli():
    "We3botron deploys websites to AWS"
    pass


@cli.command('list-buckets')
def list_buckets ():
    "List all s3 buckets"
    for bucket in s3.buckets.all():
        print (bucket)

@cli.command('list-buckets-objects')
@click.argument('bucket')
def list_buckets_objects(bucket):
    "list objects in an s3 bucket"
    for obj in s3.Bucket(bucket).objects.all():
        print (obj)

@cli.command('setup-bucket')
@click.argument('bucket')
def setup_bucket(bucket):
    "create new bucket"
    s3s3_bucket = None
    try:
       s3_bucket = s3.create_bucket(
            Bucket=bucket
            )
    except ClientError as e:
        if e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
            s3_bucket = s3.Bucket(bucket)
        else:
            raise e
    #Setting policy
    policy="""
         {
             "Version": "2012-10-17",
             "Statement": [
                 {
                     "Sid": "PublicReadGetObject",
                     "Effect": "Allow",
                     "Principal": "*",
                     "Action": "s3:GetObject",
                     "Resource": "arn:aws:s3:::%s/*"
                 }
             ]
        }
        """% s3_bucket.name #so can use anyname

    policy = policy.strip() #stripping of white space
    pol = s3_bucket.Policy()
    pol.put(Policy=policy)

    #setting website configuration
    we = s3_bucket.Website()
    we.put(WebsiteConfiguration={
        'ErrorDocument': {
        'Key': 'error.html'
        },
        'IndexDocument':
         {'Suffix': 'index.html'
         }})

    return

if __name__ == '__main__':
    cli()
