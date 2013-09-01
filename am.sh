#!/bin/sh

set -u

source $HOME/.bucketrc

DOWNLOAD_FILE=$(mktemp /tmp/am.XXXX)
DECRYPTED_FILE=$(mktemp /tmp/am.XXXX)

./s3file.py --get --bucket $BUCKET --key $KEY --file ${DOWNLOAD_FILE}
gpg --yes --output ${DECRYPTED_FILE} --decrypt ${DOWNLOAD_FILE}
vi ${DECRYPTED_FILE}
if [ $? == 0 ]; then
   gpg --recipient "$RECIPIENT" --encrypt ${DECRYPTED_FILE}
   ./s3file.py --put --bucket $BUCKET --key $KEY --file "${DECRYPTED_FILE}.gpg"
   rm -P ${DOWNLOAD_FILE} ${DECRYPTED_FILE} ${DECRYPTED_FILE}.gpg
else 
   echo "upload skipped because vi exit code != 0"
fi
