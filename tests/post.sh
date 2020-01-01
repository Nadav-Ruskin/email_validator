#! /bin/bash
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"email":"xxx@yyy.zzz"}' \
  http://0.0.0.0:5000/email/validate