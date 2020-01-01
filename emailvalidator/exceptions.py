class EmailValidationError(Exception):
	"""Basic exception for errors raised by email_validator"""
	def __init__(self, message=None):
		if message is None:
			# Default library error message
			message = "An error has occured in the email validator."
		super().__init__(message)

class DependencyError(EmailValidationError):
	"""Something the application depends on is missing"""
	def __init__(self, message=None):
		message = "Email validation encountered a dependency error.\n" + (message or "")
		super().__init__(message)

class InternalError(EmailValidationError):
	"""Something went wrong with the internal flow of the library"""
	def __init__(self, message=None):
		message = "Email validation encountered an internal error.\n" + (message or "")
		super().__init__(message)
