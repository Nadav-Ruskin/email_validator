import exceptions
import config
from werkzeug import datastructures
import json
import shutil
import jsonschema
import re
import dns.resolver
import socket
import smtplib
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from unidecode import unidecode




class emailvalidator():


	@staticmethod
	def Validate_Email(input_json) -> dict: 
		# By json convention and because the validotrs depend on one another, fail fast and report only applicable work (not a thousand 'resource missing' messages)
		return_dict = {}
		schema = emailvalidator._Fetch_Schema() # failure to fetch the schema would be considered entirely private, of no matter to the user, and should not be reported to the user.

		return_dict['schema'] = {}
		emailvalidator._Validate_Schema(return_dict['schema'], input_json, schema)
		if not return_dict['schema']['valid']: return return_dict

		email_address = input_json['email']
		email_split = email_address.split('@')
		email_domain = email_split[1]
		email_mailbox = email_split[0]

		return_dict['regex'] = {}
		emailvalidator._Validate_Regex(return_dict['regex'], email_address)
		if not return_dict['regex']['valid']: return return_dict
		mx_record = emailvalidator._Fetch_MX_Record(email_domain)
		return_dict['dns'] = {}
		emailvalidator._Validate_DNS(return_dict['dns'], mx_record)
		if not return_dict['dns']['valid']: return return_dict
		return_dict['mailbox'] = {}
		emailvalidator._Validate_Mailbox(return_dict['mailbox'], mx_record, email_address)
		if not return_dict['mailbox']['valid']: return return_dict
		return_dict['reputation'] = {}
		emailvalidator._Validate_Web_Reputation(return_dict['reputation'], email_domain)
		if not return_dict['reputation']['valid']: return return_dict
		
		
		return return_dict

	@staticmethod
	def _Fetch_Schema():
		try:
			with open(config.SCHEMA_PATH, 'r') as f:
				schema = json.load(f)
		except IOError as e:
			raise exceptions.DependencyError('IOError while loading schema.\n ({}): {}'.format(e.errno, e.strerror))
		if not schema:
			raise exceptions.DependencyError('Fetched schema is empty or missing.')
		return schema

	@staticmethod
	def _Validate_Schema(dict_root: dict, input_json: str, schema):
		dict_root['valid'] = False
		try:
			jsonschema.validate(input_json, schema)
			dict_root['valid'] = True
		except jsonschema.exceptions.ValidationError as e:
			dict_root['reason'] = 'JSON_INVALIDATES_SCHEMA'
		except jsonschema.exceptions.SchemaError as e:
			raise exceptions.DependencyError('Bad schema loaded. \nError message: {}'.format(str(e))) # This is an internal error

	@staticmethod
	def _Fetch_MX_Record(email_domain):
		try:
			records = dns.resolver.query(email_domain, 'MX')
			return str(records[0].exchange)
		except dns.resolver.NXDOMAIN: # Fail silently, the validator will catch this
			return ''

	@staticmethod
	def _Validate_Regex(dict_root: dict, email_address):
		# Pattern detects at least one character before the at sign, one character before the period that comes after it, and one character after that period:
		pattern = '.+@.+\\..+'
		if re.match(pattern, email_address):
			dict_root['valid'] = True
		else:
			dict_root['valid'] = False

	@staticmethod
	def _Validate_DNS(dict_root: dict, mx_record: str):
		dict_root['valid'] = bool(mx_record)
		if not mx_record:
			dict_root['reason'] = 'MX_FETCH_FAIL'

	@staticmethod
	def _Validate_Mailbox(dict_root: dict, mx_record: str, email_address: str):
		dict_root['valid'] = False
		# Get local server hostname
		host = socket.gethostname()

		# SMTP lib setup (use debug level for full output)
		server = smtplib.SMTP()
		server.set_debuglevel(0)

		# SMTP Conversation
		server.connect(mx_record)
		server.helo(host)
		server.mail('me@domain.com')
		code, message = server.rcpt(email_address)
		server.quit()

		dict_root['code'] = code

		# 250 is a success code
		if code == config.SMTP_REPLY_CODE_OK:
			dict_root['valid'] = True
		else:
			dict_root['reason'] = 'SMPT_CONVERSATION_FAILED'
		

	@staticmethod
	def _Validate_Web_Reputation(dict_root: dict, email_domain: str):
		dict_root['valid'] = False
		
		chrome_options = Options()
		chrome_options.add_argument("--no-sandbox")
		chrome_options.add_argument("--disable-dev-shm-usage")
		chrome_options.add_argument("--headless")
		driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver', chrome_options=chrome_options)
		driver.get(config.TALOS_ADDRESS + email_domain) # Talos also offers straight out email reputation but that seems a bit too obvious to use.
		response = driver.page_source
		driver.quit()
		soap = BeautifulSoup(response, 'html.parser')
		span_lst = []
		reputation = ''
		for div in soap.findAll('div', {"id": "email-data-wrapper"}):
			for table in div.findAll('td'):
				for span in table.findAll('span'):
					span_lst.append(span.text)
		if span_lst:
			if 'Web Reputation' in span_lst[1]:
				if span_lst[4]:
					reputation = unidecode(span_lst[4]) # str(span_lst[4].encode('ascii', 'ignore'))
		dict_root['reputation'] = reputation
		if not ('Questionable' in reputation or 'Untrusted' in reputation or not bool(reputation)): 		
			dict_root['valid'] = True
		else:
			dict_root['reason'] = 'REPUTATION_NOT_GOOD'
		
		