# -*- conding: utf-8 -*-

"""Script to upload file to S3 bucket"""
from pathlib import Path
import boto3
import click

@click.command()
@click.option('--profile', default=None, help="Use a given AWS profile")
@click.argument('filename', type=click.Path(exists=True))
@click.argument('bucketname')
def upload_file(profile, filename, bucketname):
    """Upload file to a bucket."""

    session_cfg = {}
    if profile:
        session_cfg['profile_name'] = profile

    session = boto3.Session(**session_cfg)
    bucket = session.resource('s3').Bucket(bucketname)
    return bucket.upload_file(filename, filename)


if __name__ == '__main__':
    upload_file()
