class EmailValidationError(Exception):
	"""Basic exception for errors raised by email_validator"""
	def __init__(self, message=None):
		if message is None:
			# Default library error message
			message = "An error has occured in the email validator."
		super(EmailValidationError, self).__init__(message)


class InvalidEmailValidationError(EmailValidationError):
	"""The email has failed a validator"""
	def __init__(self, message=None):
		message = "Email validation failed.\n" + (message or "")
		super(InvalidEmailValidationError, self).__init__(message)


class DependencyError(EmailValidationError):
	"""Something the application depends on is missing"""
	def __init__(self, message=None):
		message = "Email validation encountered a dependency error.\n" + (message or "")
		super(DependencyError, self).__init__(message)
