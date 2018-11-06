# !/usr/bin/python
# -*- coding: utf-8
"""Webotrong: Deploy websites with AWS
Webotron automates the process of deploying static websites with AWS
-configure AWS S3 list_buckets
"""

import boto3
import click

from bucket import BucketManager

# create Session
session = boto3.Session(profile_name='pythonAutomation')
bucket_manager = BucketManager(session)
# s3 = session.resource('s3') Bucket Manager will hold the S3 Resource


@click.group()
def cli():
    """We3botron deploys websites to AWS"""
    pass


@cli.command('list-buckets')
def list_buckets():
    """List all s3 buckets"""
    for bucket in bucket_manager.all_buckets():
        print(bucket)


@cli.command('list-buckets-objects')
@click.argument('bucket')
def list_buckets_objects(bucket):
    """list objects in an s3 bucket"""
    for obj in bucket_manager.all_objects(bucket):
        print(obj)


@cli.command('setup-bucket')
@click.argument('bucket')
def setup_bucket(bucket):
    """create new bucket"""
    s3_bucket = bucket_manager.init_bucket(bucket)
    print(s3_bucket)
    bucket_manager.set_policy(s3_bucket)
    bucket_manager.configure_website(s3_bucket)

    return

@cli.command('sync')
@click.argument('pathname', type=click.Path(exists=True))
@click.argument('bucket')
def sync(pathname, bucket):
    """Sync Contents of PATHNAME to Bucket"""
    bucket_manager.sync(pathname, bucket)


if __name__ == '__main__':
    cli()
