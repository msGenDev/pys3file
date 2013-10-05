#!/bin/sh

# Any command that exits with a nonzero exit code causes the trap to fire.
set -e

set -u

cleanup() {
    rm -f -P ${DOWNLOAD_FILE} ${DECRYPTED_FILE} ${DECRYPTED_FILE}.gpg
}
trap cleanup ERR

function sha1() {
   echo $(openssl sha1 $1 | awk -F"= " '{print $2}')
}

# We need these on the path.
which gpg > /dev/null
which openssl > /dev/null

DOWNLOAD_FILE=$(mktemp /tmp/am.XXXX)
DECRYPTED_FILE=$(mktemp /tmp/am.XXXX)

source $HOME/.amrc
./s3file.py --get --bucket ${BUCKET} --key ${KEY} --file ${DOWNLOAD_FILE}
gpg --yes --output ${DECRYPTED_FILE} --decrypt ${DOWNLOAD_FILE}
HASH_BEFORE=$(sha1 ${DECRYPTED_FILE})
vi ${DECRYPTED_FILE}
HASH_AFTER=$(sha1 ${DECRYPTED_FILE})
if [ $HASH_BEFORE != $HASH_AFTER ]; then
   gpg --recipient "${RECIPIENT}" --encrypt ${DECRYPTED_FILE}
   ./s3file.py --put --bucket ${BUCKET} --key ${KEY} --file "${DECRYPTED_FILE}.gpg"
fi
cleanup
