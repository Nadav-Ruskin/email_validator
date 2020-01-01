from flask import Flask, render_template, request, redirect, session, url_for, jsonify
import emailvalidaor
import exceptions
app = Flask(__name__)
app.secret_key = 'howdy_pardner'
debug = False



@app.route('/email/validate', methods=['POST'])
def add_message():
	content = request.get_json()
	print (content)
	email_validator = emailvalidaor.EmailValidaor(content)
	
	return email_validator.Validate_Email()
	# content = request.json
    # print('is this your email? ' + content['email'])
    # return jsonify({"hello":3})


# @app.route('/email/validate', methods=['POST'])
# def email_validate(message):
# 	content = jsonify(request.json)
# 	print("BROTHER I JUST GOT CONTENT! " + str(content))
# 	email_validator = emailvalidaor.EmailValidaor(content) # (jsonify({"uuid":uuid}))
# 	return email_validator.Validate_Mail()

if __name__ == "__main__":
	if debug:
		app.run(debug=True, use_debugger=False, use_reloader=False)
	else:
		app.run(host='0.0.0.0')
