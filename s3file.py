#!/usr/bin/env python

import sys
from functools import partial

import boto
from boto.s3.key import Key

GET = '--get'
PUT = '--put'
ERROR = -1


def transfer_file(bucket_name, file_key, file_name, operation):
    conn = boto.connect_s3()
    bucket = conn.lookup(bucket_name)
    if bucket is None:
        print "no such bucket or permissions problem on bucket %s" % bucket_name
        sys.exit(ERROR)
    key = Key(bucket, file_key)
    function = key.get_contents_to_file if operation == GET else partial(key.set_contents_from_file, encrypt_key=True)
    fp = file(file_name, "r" if operation == PUT else "w")
    function(fp)
    fp.close()
    conn.close()


def parse_arguments():
    import argparse

    parser = argparse.ArgumentParser(description='Simple S3 file transfer tool')
    parser.add_argument(GET, action="store_true", help='get the file')
    parser.add_argument(PUT, action="store_true", help='put the file')
    parser.add_argument('--file', default='', required=True, help='file to get or put')
    parser.add_argument('--bucket', default='', required=True, help='bucket name')
    parser.add_argument('--key', default='', required=True, help='key to store file under')
    args = parser.parse_args()
    if args.get and args.put:
        print "Only one of --get or --put must be specified"
        sys.exit(ERROR)
    if not args.get and not args.put:
        print "At least one of --get or --put must be specified"
        sys.exit(ERROR)
    operation = GET if args.get else PUT
    args.operation = operation
    return args


if __name__ == "__main__":
    options = parse_arguments()
    transfer_file(options.bucket, options.key, options.file, options.operation)
