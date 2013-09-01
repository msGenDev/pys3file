
## File transfer

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


## Encrypted file wrapper

Also included is a shell script _am.sh_ that treats the S3-managed file as an encrypted text
file of interest.  Use of  _am.sh_ requires [GnuPG Privacy Guard](http://www.gnupg.org) be installed,
that you have at least one keypair, and that a $HOME/.bucketrc file holding the bucket, key, and
GnuPG recipient.

Here is a sample .bucketrc file

    BUCKET=thebucketname
    KEY=thes3key
    RECIPIENT="Bob Loblaw"

where _BUCKET_ is the S3 bucket that holds the file of interest, _KEY_ is the key under which the file of
interest is held in the S3 bucket, and _RECIPIENT_ is the GnuPG recipient, used to select the
GnuPG key with which to encrypt and decrypt the file of interest.

Run am.sh with no arguments:

    am.sh

This results in the encrypted file being fetched from S3, decrypted with GnuPG, opening the decrypted version
in vi, followed by re-encrypting the edited file and putting back to S3.  All files are named on the fly using
_mktemp_ and are removed after the session using _rm -P ..._, where _-P_ overwrites the file data before the file
is unlinked.  During encryption and decryption, GnuPG will prompt you for your passphrase when it needs it.