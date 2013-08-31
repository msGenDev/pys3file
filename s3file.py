#!/usr/bin/python

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


def main(op):
    bucket_name = 'thebucket'
    file_name = "thefilename"

    # credentials are in ~/.boto
    conn = boto.connect_s3()

    bucket = conn.lookup(bucket_name)

    if bucket is None:
        print "no bucket"
        sys.exit(0)

    k = Key(bucket)
    k.key = file_name

    if op == "--put":
        fp = file(file_name, "r")
        k.set_contents_from_file(fp)
        fp.close()
    elif op == "--get":
        fp = file(file_name, "w")
        k.get_contents_to_file(fp)
        fp.close()
    else:
        print "unsupported operation: %s" % op

    conn.close()


if __name__ == "__main__":
    operation = sys.argv[1]
    main(operation)
