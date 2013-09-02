#!/bin/sh

set -e
set -u

cleanup() {
    rm -f -P ${DOWNLOAD_FILE} ${DECRYPTED_FILE} ${DECRYPTED_FILE}.gpg
}
trap cleanup ERR

type gpg > /dev/null

DOWNLOAD_FILE=$(mktemp /tmp/am.XXXX)
DECRYPTED_FILE=$(mktemp /tmp/am.XXXX)

source $HOME/.bucketrc
./s3file.py --get --bucket ${BUCKET} --key ${KEY} --file ${DOWNLOAD_FILE}
gpg --yes --output ${DECRYPTED_FILE} --decrypt ${DOWNLOAD_FILE}
vi -R -n -f ${DECRYPTED_FILE}
gpg --recipient "${RECIPIENT}" --encrypt ${DECRYPTED_FILE}
./s3file.py --put --bucket ${BUCKET} --key ${KEY} --file "${DECRYPTED_FILE}.gpg"
cleanup
