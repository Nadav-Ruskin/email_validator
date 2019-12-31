from flask import Flask, render_template, request, redirect, session, url_for, jsonify
import emailvalidaor
import exceptions
app = Flask(__name__)
app.secret_key = 'howdy_pardner'
email_validator = emailvalidaor.EmailValidaor()
debug = False


@app.route('/email/validate', methods=['POST'])
def email_validate():
	content = request.json
	print(content['mytext'])
	return jsonify({"uuid":uuid}

if __name__ == "__main__":
	if debug:
		app.run(debug=True, use_debugger=False, use_reloader=False)
	else:
		app.run(host='0.0.0.0')
