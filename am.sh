#!/bin/sh

# Any command that exits with a nonzero exit code causes the trap to fire.
set -e

set -u

cleanup() {
    rm -f -P ${DOWNLOAD_FILE} ${DECRYPTED_FILE} ${DECRYPTED_FILE}.gpg
}
trap cleanup ERR

# We need gpg on the path.
which gpg > /dev/null

DOWNLOAD_FILE=$(mktemp /tmp/am.XXXX)
DECRYPTED_FILE=$(mktemp /tmp/am.XXXX)

source $HOME/.amrc
./s3file.py --get --bucket ${BUCKET} --key ${KEY} --file ${DOWNLOAD_FILE}
gpg --yes --output ${DECRYPTED_FILE} --decrypt ${DOWNLOAD_FILE}
view ${DECRYPTED_FILE}
gpg --recipient "${RECIPIENT}" --encrypt ${DECRYPTED_FILE}
./s3file.py --put --bucket ${BUCKET} --key ${KEY} --file "${DECRYPTED_FILE}.gpg"
cleanup
