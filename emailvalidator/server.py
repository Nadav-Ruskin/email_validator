from flask import Flask, render_template, request, redirect, session, url_for, jsonify
from emailvalidator import emailvalidator

# debug = False
app = Flask(__name__)
app.secret_key = 'howdy_pardner'

@app.route('/email/validate', methods=['POST'])
def add_message():
	content = request.get_json()
	answer = emailvalidator.Validate_Email(content)
	return answer


if __name__ == "__main__":
	if debug:
		app.run(debug=True, use_debugger=False, use_reloader=False)
	else:
		app.run(host='0.0.0.0')
