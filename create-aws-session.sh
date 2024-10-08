#!/bin/bash

# Before execute this script. you must set AccNum Environment varialbe on your local device 

output_file=~/session.json

if [ -z "$1"  ]; then
  echo "You should input MFA serial codes"
  exit 1
fi

if [ "$1" -lt 6 ]; then
  echo "MFA serial codes should be 6 digit-number"
  exit 1
fi

aws sts assume-role --profile mz-tf-user --role-arn arn:aws:iam::$AccNum:role/iam-role-josh-assume-admin --role-session-name MySession --serial-number arn:aws:iam::$AccNum:mfa/josh-iphone --token $1 > $output_file

aws configure set aws_access_key_id $(cat $output_file | jq -r .Credentials.AccessKeyId)
aws configure set aws_secret_access_key $(cat $output_file | jq -r .Credentials.SecretAccessKey)
aws configure set aws_session_token $(cat $output_file | jq -r .Credentials.SessionToken)

rm -f $output_file

#### TIL Memo #### 
# jq -r : 문자열 양 끝 "" 제거
# -z : zero
# -lt: lessthan
