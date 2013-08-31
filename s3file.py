#!/usr/local/bin/python

'''
The AWS IAM user needs these permissions. Note these permissions
are set on the user, not the bucket.

{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "s3:*"
      ],
      "Sid": "Stmt1377903120000",
      "Resource": [
        "arn:aws:s3:::thebucket/*"
      ],
      "Effect": "Allow"
    }
  ]
}

and

{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "s3:*"
      ],
      "Sid": "Stmt1377903717000",
      "Resource": [
        "arn:aws:s3:::thebucket"
      ],
      "Effect": "Allow"
    }
  ]
}
'''

import sys

import boto
from boto.s3.key import Key

GET = '--get'
PUT = '--put'


def transfer_file(bucket_name, file_name, operation):
    # credentials are in ~/.boto
    conn = boto.connect_s3()
    bucket = conn.lookup(bucket_name)
    if bucket is None:
        print "no such bucket or permissions problem on bucket %s" % bucket_name
        sys.exit(0)
    key = Key(bucket, file_name)
    file_mode = "r" if operation == PUT else "w"
    function = key.get_contents_to_file if operation == GET else key.set_contents_from_file
    fp = file(file_name, file_mode)
    function(fp)
    fp.close()
    conn.close()


def parse_arguments():
    import argparse

    parser = argparse.ArgumentParser(description='Simple S3 file transfer tool')
    parser.add_argument(GET, action="store_true", help='get the file')
    parser.add_argument(PUT, action="store_true", help='put the file')
    parser.add_argument('--file', default='', required=True, help='file name to get')
    parser.add_argument('--bucket', default='', required=True, help='bucket name')
    args = parser.parse_args()
    if args.get and args.put:
        print "Only one of --get or --put must be specified"
        sys.exit(0)
    if not args.get and not args.put:
        print "At least one of --get or --put must be specified"
        sys.exit(0)
    operation = GET if args.get else PUT
    args.operation = operation
    return args


if __name__ == "__main__":
    options = parse_arguments()
    transfer_file(options.bucket, options.file, options.operation)
