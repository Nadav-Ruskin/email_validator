#! /bin/bash
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"email":"ruskin.nadav@gmail.com"}' \
  http://0.0.0.0:5000/email/validate