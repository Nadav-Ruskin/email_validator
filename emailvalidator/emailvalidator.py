from werkzeug import datastructures
import os
import json
import shutil
import jsonschema
import re
import dns.resolver
import socket
import smtplib
import exceptions


SCRIPT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
SCHEMA_PATH = os.path.join(SCRIPT_DIRECTORY, 'jsons', 'schema.json')


class emailvalidator():
#	Json philosophy: Only output what's needed. Let validators edit an external json and let the process end on first fail.

	@staticmethod
	def Validate_Email(input_json) -> dict:
		return_dict = {}
		schema = emailvalidator._Fetch_Schema()

		return_dict['schema'] = {}
		if not emailvalidator._Validate_Schema(return_dict['schema'], input_json, schema): return return_dict

		email_address = input_json['email']
		email_split = email_address.split('@')
		email_domain = email_split[1]
		email_mailbox = email_split[0]

		return_dict['regex'] = {}
		if not emailvalidator._Validate_Regex(return_dict['regex'], email_address): return return_dict

		mx_record = emailvalidator._Fetch_MX_Record(email_domain)
		return_dict['dns'] = {}
		if not emailvalidator._Validate_DNS(return_dict['dns'], mx_record): return return_dict
		return_dict['mailbox'] = {}
		if not emailvalidator._Validate_Mailbox(return_dict['mailbox'], mx_record, email_address): return return_dict
		
		return return_dict

	@staticmethod
	def _Fetch_Schema():
		try:
			with open(SCHEMA_PATH, 'r') as f:
				schema = json.load(f)
		except IOError as e:
			raise exceptions.DependencyError('IOError while loading schema.\n ({}): {}'.format(e.errno, e.strerror))
		if not schema:
			raise exceptions.DependencyError('Input schema is empty or missing.')
		return schema

	@staticmethod
	def _Fetch_MX_Record(email_domain):
		try:
			records = dns.resolver.query(email_domain, 'MX')
			return str(records[0].exchange)
		except dns.resolver.NXDOMAIN:
			pass

	@staticmethod
	def _Validate_Schema(dict_root: dict, input_json: str, schema):
		try:
			jsonschema.validate(input_json, schema)
			dict_root['valid'] = True
			return True
		except jsonschema.exceptions.ValidationError as e:
			raise exceptions.EmailValidationError('Input json invalidates schema. json:\n{}\nError message: {}'.format(str(input_json), str(e)))
		except jsonschema.exceptions.SchemaError as e:
			raise exceptions.DependencyError('Bad schema loaded. \nError message: {}'.format(str(e)))
		dict_root['valid'] = False
		return False
		

	@staticmethod
	def _Validate_Regex(dict_root: dict, email_address):
		# Pattern detects at least one character before the at sign, one character before the period that comes after it, and one character after that period:
		pattern = '.+@.+\\..+'
		if re.match(pattern, email_address):
			dict_root['valid'] = True
			return True
		dict_root['valid'] = False
		return False
			

	@staticmethod
	def _Validate_DNS(dict_root: dict, mx_record: str):
		if mx_record:
			dict_root['valid'] = True
			return True
		dict_root['valid'] = False
		return False


	@staticmethod
	def _Validate_Mailbox(dict_root: dict, mx_record: str, email_address: str):
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

		# 250 is success
		dict_root['valid'] = code == 250
		dict_root['code'] = code
		
		return dict_root['valid']
