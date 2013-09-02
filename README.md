
## File transfer

This is a simple Python based file transfer utility to get and put files to Amazon S3.  It uses the
[boto Python library](http://boto.s3.amazonaws.com/s3_tut.html)
for AWS S3, and requires Python 2.7 for purposes of using _argparse_ command line parsing.

I installed boto like this on the Mac:

    sudo easy_install pip
    sudo pip install boto

The utility assumes an existing [AWS IAM user](http://docs.aws.amazon.com/IAM/latest/UserGuide/Using_SettingUpUser.html)
whose credentials are stored in $HOME/.boto in the format

    [Credentials]
    aws_access_key_id = key
    aws_secret_access_key = secret

The AWS IAM user must have the following [permissions](http://docs.aws.amazon.com/IAM/latest/UserGuide/PermissionsOverview.html) at the user (not bucket) level.
Assuming [the bucket exists](http://docs.aws.amazon.com/AmazonS3/latest/gsg/CreatingABucket.html) and its name
is _thebucket_, for object read/write within the bucket

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

 and for bucket listing

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
by _--file_.  Files uploaded to S3 also undergo
[server-side encryption](http://docs.aws.amazon.com/AmazonS3/latest/dev/UsingServerSideEncryption.html).

## Encrypted file wrapper

Also included is a shell script _am.sh_ that wraps the file transfer utility above to manage an encrypted text file of
interest.  Use of  _am.sh_ requires [GnuPG Privacy Guard](http://www.gnupg.org) be installed,
that you have at least one GnuPG keypair, and that a $HOME/.amrc file exists holding the values for bucket name, key, and
GnuPG recipient.

Here is a sample .amrc file

    BUCKET=thebucketname
    KEY=thes3key
    RECIPIENT="Bob Loblaw"

where the combination of  _BUCKET:KEY_ is where to store the file of interest and _RECIPIENT_ is the GnuPG
recipient.  The recipient is a GnuPG concept and its value is used to select from your GnuPG keyring the
public key with which to encrypt the file content.

Run _am.sh_ with no arguments:

    am.sh

This results in the encrypted file being fetched from S3, decrypted with GnuPG,
opened [read-only in vi](http://vimdoc.sourceforge.net/htmldoc/starting.html#-R), followed by re-encrypting the
possibly modified file and putting it back to S3.  The downloaded and decrypted files are named on the
fly using [mktemp](http://unixhelp.ed.ac.uk/CGI/man-cgi?mktemp) and are removed after the session using _rm -P ..._,
where _-P_ overwrites the file data before the file is unlinked.  During encryption, GnuPG will prompt you for
your passphrase when it needs it.