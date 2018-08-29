#!/bin/sh
echo "pre-commit started"
if git rev-parse --verify HEAD >/dev/null 2>&1
then
    against=HEAD
else
    # Initial commit: diff against an empty tree object
    against=5da2c1fe8f6458e32d11110e0ebdd915e472c6e0
fi
 
# Redirect output to stderr.
exec 1>&2
 
# Check changed files for an AWS keys
KEY_ID=$(git diff --cached --name-only -z $against | xargs -0 cat | perl -nle'print $& if m{(?<![A-Z0-9])[A-Z0-9]{20}(?![A-Z0-9])}')
KEY=$(git diff --cached --name-only -z $against | xargs -0 cat | perl -nle'print $& if m{(?<![^A-Za-z0-9/+=])[A-Za-z0-9/+=]{40}(?![^A-Za-z0-9/+=])}')
 
if [ "$KEY_ID" != "" -o "$KEY" != "" ]; then
    echo "Found patterns for AWS_ACCESS_KEY_ID/AWS_SECRET_ACCESS_KEY"
    echo "Please check your code and remove API keys."
    exit 1
fi
 
# Normal exit
echo "pre-commit stopped"
exit 0