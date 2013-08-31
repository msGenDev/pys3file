
Simple Python based file transfer to/from Amazon S3 that uses the boto
python library for AWS S3.   Requires Python 2.7 for purposes of using argparse
command line parsing.

I installed boto like this on the Mac:

    sudo easy_install pip
    sudo pip install boto

The utility assumes your S3 credentials are stored in $HOME/.boto in the format

    [Credentials]
    aws_access_key_id = key
    aws_secret_access_key = secret

The AWS IAM user must have these permissions at the user (not bucket) level:

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

Usage for uploading looks like

    s3file.py --put --file foo.txt --bucket thebucket

and for downloading

    s3file.py --get --file foo.txt --bucket thebucket


