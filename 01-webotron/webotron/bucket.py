# -*- conding: utf-8 -*-

"""Classes for S3 Buckets."""
from pathlib import Path
import mimetypes
from botocore.exceptions import ClientError
import util
from hashlib import md5
from functools import reduce
import boto3

class BucketManager:
    """Manage an S3 Bucket."""

    CHUNK_SISE = 8388608
    def __init__(self, session):
        """Create a BucketManager object."""
        self.s3 = session.resource('s3')
        self.transfer_config = boto3.s3.transfer.TransferConfig(
            multipart_chunksize=self.CHUNK_SISE,
            multipart_threshold=self.CHUNK_SISE
        )
        self.manifest = {}

    def get_region_name(self, bucket):
        """Get the bucket's region name."""
        bucket_location = self.s3.meta.client.get_bucket_location(Bucket=bucket.name)
        return bucket_location["LocationConstraint"] or 'us-east-1'

    def get_bucket_url(self, bucket):
        """Get the website URL for this bucket."""
        return "http://{}.{}".format(bucket.name, util.get_endpoint(self.get_region_name(bucket)).host)

    def all_buckets(self):
        """Get an interator for all buckets."""
        return self.s3.buckets.all()

    def all_objects(self, bucket_name):
        """Get an interator for all objects in a bucket."""
        return self.s3.Bucket(bucket_name).objects.all()

    def init_bucket(self, bucket_name):
        """Create and config a bucket."""
        try:
            s3_bucket = self.s3.create_bucket(Bucket=bucket_name)
        except ClientError as e:
            if e.response['Error']['Code'] == 'BucketAlreadyExists':
                s3_bucket = self.s3.Bucket(bucket_name)
            else:
                raise e
        return s3_bucket

    def set_policy(self, bucket):
        """Set bucket policy to be readable by everyone."""
        policy = """
        {
          "Version":"2012-10-17",
          "Statement":[{
          "Sid":"PublicReadGetObject",
          "Effect":"Allow",
          "Principal": "*",
              "Action":["s3:GetObject"],
              "Resource":["arn:aws:s3:::%s/*"
              ]
            }
          ]
        }
        """ % bucket.name
        policy = policy.strip()
        pol = bucket.Policy()
        pol.put(Policy=policy)

    def configure_website(self, bucket):
        """Configure website for a bucket."""
        bucket.Website().put(WebsiteConfiguration={
            'ErrorDocument': {
                'Key': 'error.html'
                },
            'IndexDocument': {
                'Suffix': 'index.html'
            }
        })

    def load_manifest(self, bucket):
        """Load manifest for caching purposes."""
        paginator = self.s3.meta.client.get_paginator('list_objects_v2')
        for page in paginator.paginate(Bucket=bucket.name):
            for obj in page.get('Contents', []):
                self.manifest[obj['Key']] = obj['ETag']

    @staticmethod
    def hash_data(data):
        """Generate md5 hash for data."""
        hash = md5()
        hash.update(data)
        return hash

    def get_etag(self, path):
        """Generate etag for a file."""
        hashes = []
        with open(path, 'rb') as f:
            while True:
                data = f.read(self.CHUNK_SISE)
                if not data:
                    break
                hashes.append(self.hash_data(data))
        if not hashes:
            return
        elif len(hashes) ==1:
            return '"{}"'.format(hashes[0].hexdigest())
        else:
            hash = self.hash_data(reduce(lambda x, y: x + y, (h.digest() for h in hashes)))
            return '"{}-{}"'.format(hash.hexdigest(), len(hashes))

    def upload_file(self, bucket, path, key):
        """Upload files to a bucket."""
        content_type = mimetypes.guess_type(key)[0] or 'text/plain'
        etag = self.get_etag(path)
        if self.manifest.get(key, '') == etag:
            print("Skipping {}, etags match".format(key))
            return
        return bucket.upload_file(
            path,
            key,
            ExtraArgs={
                'ContentType': content_type
            },
            Config=self.transfer_config
        )

    def sync(self, pathname, bucket_name):
        """Sync files to a bucket."""
        bucket = self.s3.Bucket(bucket_name)
        self.load_manifest(bucket)
        root = Path(pathname).expanduser().resolve()

        def handle_directory(target):
            for p in target.iterdir():
                if p.is_dir():
                    handle_directory(p)
                if p.is_file():
                    self.upload_file(bucket, str(p), str(p.relative_to(root)))

        handle_directory(root)