from server import app
from emailvalidator import emailvalidator
import unittest
# run with python3 -m tests/unittest test_app


SUSPICIOUS_DOMAINS_FILE_LOCATION = 'tests/dependencies/suspiciousdomains_High.txt'

class EmailValidatorTests(unittest.TestCase):
	def setUp(self):
		self.app = app.test_client()

	def test_success(self):
		response = self.app.post('/email/validate', json={'email':'ruskin.nadav@gmail.com'})
		data = response.data.decode('utf-8')
		assert(data == '{"dns":{"valid":true},"mailbox":{"code":250,"valid":true},"regex":{"valid":true},"reputation":{"reputation":"Favorable  |  Neutral","valid":true},"schema":{"valid":true}}\n')
	
	def test_bad_mailbox(self):
		response = self.app.post('/email/validate', json={'email':'obviously_fake@gmail.com'})
		data = response.data.decode('utf-8')
		assert(data == '{"dns":{"valid":true},"mailbox":{"code":550,"reason":"SMPT_CONVERSATION_FAILED","valid":false},"regex":{"valid":true},"schema":{"valid":true}}\n')
	
	def test_bad_mailbox(self):
		response = self.app.post('/email/validate', json={'email':'obviously_fake@gmail.com'})
		data = response.data.decode('utf-8')
		assert(data == '{"dns":{"valid":true},"mailbox":{"code":550,"reason":"SMPT_CONVERSATION_FAILED","valid":false},"regex":{"valid":true},"schema":{"valid":true}}\n')

	def test_bad_dns(self):
		response = self.app.post('/email/validate', json={'email':'obviously_fake@obviously_fake.com'})
		data = response.data.decode('utf-8')
		assert(data == '{"dns":{"reason":"MX_FETCH_FAIL","valid":false},"regex":{"valid":true},"schema":{"valid":true}}\n')
	
	def test_bad_regex(self):
		response = self.app.post('/email/validate', json={'email':'barely_even_an_email'})
		data = response.data.decode('utf-8')
		assert(data == '{"regex":{"valid":false},"schema":{"valid":true}}\n')

	def test_bad_request(self):
		response = self.app.post('/email/validate', json={'esnail': 'aka normal mail'})
		data = response.data.decode('utf-8')
		assert(data == '{"schema":{"reason":"JSON_INVALIDATES_SCHEMA","valid":false}}\n')

	def test_bad_rep(self):
		with open(SUSPICIOUS_DOMAINS_FILE_LOCATION, 'r') as file:
			email_domain = file.readline().rstrip()
			assert(email_domain)
		return_dict = {}
		return_dict['reputation'] = {}
		emailvalidator._Validate_Web_Reputation(return_dict['reputation'], email_domain)
		assert(str(return_dict) == "{'reputation': {'valid': False, 'reputation': '', 'reason': 'REPUTATION_NOT_GOOD'}}")