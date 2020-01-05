# email validator
https://github.com/Nadav-Ruskin/email_validator
https://hub.docker.com/repository/docker/nadavru/email_validator


An email validation service, meant to be used by a service to validate emails from user space.


`docker run -d -p 127.0.0.1:8080:8080 -e PORT=8080 --name emailvalidator_container nadavru/email_validator` should get the service going. Feel free to test using:
```bash
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"email":"ruskin.nadav@gmail.com"}' \
  http://0.0.0.0:8080/email/validate
```

The project is built using `Build.py`. It has its own requirements, so run `pip3 install -r requirements.txt` first. Known commands:
`python3 Build.py --build`
`python3 Build.py --run`
`python3 Build.py --start`
`python3 Build.py --kill`
`python3 Build.py --rm`
`python3 Build.py --rmi`
`python3 Build.py --test`

If ran with multiple arguments, `Build.py` will run in the sequence they're listed above (build first, test last).

If you're planning on running it on your machine without docker, consider installing chromedriver from /scripts/install_chromedriver.sh (you might need chrome too, check out the Dockerfile).

