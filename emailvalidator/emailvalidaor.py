from werkzeug import datastructures
import os
import json
import shutil
import jsonschema
import exceptions
import re

SCRIPT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
SCHEMA_PATH = os.path.join(SCRIPT_DIRECTORY, "jsons", "schema.json")


class EmailValidaor():
	def __init__(self, email_address):
		self._EMAIL_ADDRESS = email_address
		try:
			with open(SCHEMA_PATH, 'r') as f:
				schema = json.load(f)
		except IOError as e:
			raise exceptions.DependencyError("IOError while loading schema.\n ({}): {}".format(e.errno, e.strerror))
		if not schema:
			raise exceptions.DependencyError("Input schema is empty or missing.")
		self._SCHEMA = schema

	def Validate_Mail(self):
		self._Validator_Schema()
		self._Validator_Regex()

	def _Validator_Schema(self):
		try:
			jsonschema.validate(self._EMAIL_ADDRESS, self._SCHEMA)
		except jsonschema.exceptions.ValidationError as e:
			raise exceptions.InvalidEmailValidationError("Input json invalidates schema. json:\n{}\nError message: {}".format(str(self._EMAIL_ADDRESS), str(e)))
		except jsonschema.exceptions.SchemaError as e:
			raise exceptions.DependencyError("Bad schema loaded. \nError message: {}".format(str(e)))

	def _Validator_Regex(self):
		# Pattern detects at least one character before the at sign, one character before the period that comes after it, and one character after that period:
		pattern = '.+@.+\\..+'
		if re.match(pattern, email_address):
			pass
		else:
			raise exceptions.InvalidEmailValidationError("Email failed basic regex test, it's probably wrong. json:\n{}\nError message: {}".format(str(self._EMAIL_ADDRESS), str(e)))