
## File transfer

This is a simple Python based file transfer utility to get and put files to Amazon S3.  It uses the boto
python library for AWS S3.   It requires Python 2.7 for purposes of using argparse
command line parsing.

I installed boto like this on the Mac:

    sudo easy_install pip
    sudo pip install boto

The utility assumes your S3 credentials are stored in $HOME/.boto in the format

    [Credentials]
    aws_access_key_id = key
    aws_secret_access_key = secret

The AWS IAM user that this utility assumes must have the following permissions at the user (not bucket) level.
Assuming the bucket name is _thebucket_, for bucket listing:

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

and for object read/write within the bucket:

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

    s3file.py --put --file /tmp/foo.txt --bucket thebucket --key thekey

and for downloading

    s3file.py --get --file /tmp/foo.txt --bucket thebucket --key thekey

The PUT operation expects the file denoted by _--file_ to exist, and uploads the content to _thebucket:thekey_.
The GET operation expects the content _thebucket:thekey_ to exist, and downloads the content to the file denoted
by _--file_.

## Encrypted file wrapper

Also included is a shell script _am.sh_ that wraps the file transfer utility above to manage an encrypted text file of
interest.  Use of  _am.sh_ requires [GnuPG Privacy Guard](http://www.gnupg.org) be installed,
that you have at least one GnuPG keypair, and that a $HOME/.bucketrc file exists holding the bucket, key, and
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

This results in the encrypted file being fetched from S3, decrypted with GnuPG, opened in vi and potentially
 modified, followed by
re-encrypting the edited file and putting back to S3.  All temporary files are named on the fly using
_mktemp_ and are removed after the session using _rm -P ..._, where _-P_ overwrites the file data before the file
is unlinked.  During encryption and decryption, GnuPG will prompt you for your passphrase when it needs it.