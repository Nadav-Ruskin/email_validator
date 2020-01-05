import requests
import json
import unittest
# run with python3 -m tests/unittest test_app

class EmailValidatorExternalTests(unittest.TestCase):
	def test_curl(self):
		url = "http://0.0.0.0:8080/email/validate"
		headers = {'Content-type': 'application/json'}
		response = requests.post(url, data='{"email":"ruskin.nadav@gmail.com"}', headers=headers)
		data = response.content.decode('utf-8')
		assert(data == '{"dns":{"valid":true},"mailbox":{"code":250,"valid":true},"regex":{"valid":true},"reputation":{"reputation":"Favorable  |  Neutral","valid":true},"schema":{"valid":true}}\n')
