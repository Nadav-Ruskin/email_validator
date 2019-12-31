class EmailValidationError(Exception):
	"""Basic exception for errors raised by email_validator"""
	def __init__(self, msg=None):
		if msg is None:
			# Set some default useful error message
			msg = "An error occured with the email validator."
		super(EmailValidationError, self).__init__(msg)


class InvalidEmailValidationError(EmailValidationError):
	"""The email has failed a validator"""
	def __init__(self, msg=None):
		message = "Emil validation failed.\n" + (msg or "")
		super(InvalidEmailValidationError, self).__init__(msg=message)


class DependencyError(EmailValidationError):
	"""Something the application depends on is missing"""
	def __init__(self, msg=None):
		message = "Emil validation encountered an internal error.\n" + (msg or "")
		super(InvalidEmailValidationError, self).__init__(msg=message)
