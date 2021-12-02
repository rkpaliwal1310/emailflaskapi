from os import replace
import token
from flask import Flask, request, jsonify, make_response,redirect
from flask.helpers import url_for
from flask.templating import render_template,_render
from flask_sqlalchemy import SQLAlchemy
import uuid # for public id
import mysql  
from sqlalchemy import update,insert
import flask
import smtplib as s
from sqlalchemy.sql.dml import Update
from sqlalchemy.sql.functions import user
from flask_change_password import ChangePassword, ChangePasswordForm, SetPasswordForm
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from functools import wraps

from werkzeug.utils import redirect

# app = Flask(__name__ ,template_folder='template')
app = Flask(__name__)
app.config['SECRET_KEY'] = 'key'
# database name
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['JWT_ALGORITHM'] = 'HS256'

db = SQLAlchemy(app)

# Database ORMs
class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	public_id = db.Column(db.String(50), unique = True)
	name = db.Column(db.String(100))
	email = db.Column(db.String(70), unique = True)
	password = db.Column(db.String(80))
	user_token = db.Column(db.String(500), unique = True)

def token_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		token = None
		# jwt is passed in the request header
		if 'access-token' in request.headers:
			token = request.headers['access-token']
		if not token:
			return ({'message' : 'Token is missing !!'})
		try:
			# print("before Try block run......")
			data = jwt.decode(token, app.config['SECRET_KEY'],app.config['JWT_ALGORITHM'] )
			current_user = User.query.filter_by(public_id = data['public_id']).first()
			# print("Try block run......")
		except:
			return ('Please enter a valid Token..')
		return f(current_user, *args, **kwargs)
	return decorated

@app.route('/user', methods =['GET'])
@token_required
def get_all_users(current_user):
	
	users = User.query.all()
	output = []
	for user in users:
	
		output.append({
			'public_id': user.public_id,
			'name' : user.name,
			'email' : user.email
		})
	print(output)
	return jsonify({'users': output})

@app.route('/login', methods =['POST'])
def login():
	auth = request.form

	if not auth or not auth.get('email') or not auth.get('password'):
		return ('Please enter in a KEY email and password')
	user = User.query.filter_by(email = auth.get('email')).first()

	if not user:
		return ('Could not verify Please enter correct email')
	# if check_password_hash(user.password, auth.get('password')):
	print(user.public_id + " user id...")
	if (user.password == auth.get('password')):
		# generates the JWT Token
		token = jwt.encode({
			'public_id': user.public_id,
			'exp' : datetime.utcnow() + timedelta(hours = 24)
		}, app.config['SECRET_KEY'])
		# token=tokenp

		return ({'token' : token})
		# return make_response(jsonify({'token' : token.decode('UTF-8')}), 201)		
	return make_response('Could not verify Please enter correct pasword')
@app.route('/signup', methods =['POSt'])
def signup():
	data = request.form

	name, email = data.get('name'), data.get('email')
	password = data.get('password')

	user = User.query.filter_by(email = email).first()
	if not user:
		user = User(
			public_id = str(uuid.uuid4()),
			name = name,
			email = email,
			password =password #  generate_password_hash(password)
		)
		db.session.add(user)
		db.session.commit()
		return make_response('Successfully registered...')
	else:
		return make_response('User already exists. Please Login...')

@app.route('/forgot-password', methods =['GET','POST'])
def forgot_password():
    auth = request.form
    if not auth or not auth.get('email'):
	    return ('Please enter in a KEY email')
    user = User.query.filter_by(email = auth.get('email')).first()
    print(user)
    if not user:
	    return ('Could not verify Please enter correct email')
    if (user):
					token = jwt.encode({
						'public_id': user.public_id,
						'exp' : datetime.utcnow() + timedelta(minutes= 10)
					}, app.config['SECRET_KEY'])	
					return (token)  # 

# @app.route('/url?access-token={{token}}',methods=['GET','PUT'])
@app.route('/url',methods=['GET','PUT'])
@token_required
def url(current_user):
         
		auth = request.headers
		if not auth or not auth.get('email'):
			return ('Please enter in a KEY email')
		user = User.query.filter_by(email = auth.get('email')).first()
		user_token = auth.get('access-token')
		print("HELLO...")
		print(user_token)
		if not user:
			return ('Could not verify Please enter correct email')
		user.user_token=user_token
		db.session.commit()
			
		if(user):

			ob=s.SMTP("smtp.gmail.com",587)
			ob.starttls()
			ob.login("rkpaliwal0001@gmail.com","rkpaliwal@1310")
			subject="Sending email using python"
			# body=('http://127.0.0.1:4000/new_password/'+token)
			body=('http://127.0.0.1:4000/new_password')
			message="subject:{}\n\n{}".format(subject,body)
			ListOfAddress=[user.email]
			# ListOfAddress=["rajkumarpaliwal138@gmail.com"]
			ob.sendmail("rkpaliwal0001@gmail.com",ListOfAddress,message)
			# m=replace(body,passw)
			# print(m)
			return ("Email successfully send...")  #
	
@app.route('/new_password', methods =['GET','POST'])
def new_password():
	if(request.method=='POST'):
		# email1=request.form['email']
		auth = request.form
		if not auth or not auth.get('email'):
			return ('Please enter in a KEY email')
		user = User.query.filter_by(email = auth.get('email')).first()
		# tok=User.query.filter_by(user.user_taken)
		# print(user.user_token)
		password=request.form['password']
		print("HELLO...")
		# print(password)
		us=user.user_token
		if not us:
			return("SORRY....The URL is no longer valid")
		else:
			if not user:
				return ('Could not verify Please enter correct email')
			user.password=password
			user.user_token=""
			db.session.commit()
			# return "You is"+email + password

	return render_template('/new_password.html')
		
if __name__ == "__main__":
	app.run(debug = True,port=4000)














# from os import replace
# import token
# from flask import Flask, request, jsonify, make_response,redirect
# from flask.helpers import url_for
# from flask.templating import render_template,_render
# from flask_sqlalchemy import SQLAlchemy
# import uuid # for public id
# import mysql  
# from sqlalchemy import update
# import flask
# import smtplib as s
# from sqlalchemy.sql.dml import Update
# from sqlalchemy.sql.functions import user
# from flask_change_password import ChangePassword, ChangePasswordForm, SetPasswordForm
# from werkzeug.security import generate_password_hash, check_password_hash
# import jwt
# from datetime import datetime, timedelta
# from functools import wraps

# from werkzeug.utils import redirect

# # app = Flask(__name__ ,template_folder='template')
# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'key'
# # database name
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/flask'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# app.config['JWT_ALGORITHM'] = 'HS256'

# db = SQLAlchemy(app)

# # Database ORMs
# class User(db.Model):
# 	id = db.Column(db.Integer, primary_key = True)
# 	public_id = db.Column(db.String(50), unique = True)
# 	name = db.Column(db.String(100))
# 	email = db.Column(db.String(70), unique = True)
# 	password = db.Column(db.String(80))



# def token_required(f):
# 	@wraps(f)
# 	def decorated(*args, **kwargs):
# 		token = None
# 		# jwt is passed in the request header
# 		if 'access-token' in request.headers:
# 			token = request.headers['access-token']
# 		if not token:
# 			return ({'message' : 'Token is missing !!'})
# 		try:
# 			print("before Try block run......")
# 			data = jwt.decode(token, app.config['SECRET_KEY'],app.config['JWT_ALGORITHM'] )
# 			current_user = User.query.filter_by(public_id = data['public_id']).first()
# 			print("Try block run......")
# 		except:
# 			return ('Please enter a valid Token..')
# 		return f(current_user, *args, **kwargs)
# 	return decorated

# @app.route('/user', methods =['GET'])
# @token_required
# def get_all_users(current_user):
	
# 	users = User.query.all()
# 	output = []
# 	for user in users:
	
# 		output.append({
# 			'public_id': user.public_id,
# 			'name' : user.name,
# 			'email' : user.email
# 		})
# 	print(output)
# 	return jsonify({'users': output})

# @app.route('/login', methods =['POST'])
# def login():
# 	auth = request.form

# 	if not auth or not auth.get('email') or not auth.get('password'):
# 		return ('Please enter in a KEY email and password')
# 	user = User.query.filter_by(email = auth.get('email')).first()

# 	if not user:
# 		return ('Could not verify Please enter correct email')
# 	# if check_password_hash(user.password, auth.get('password')):
# 	print(user.public_id + " user id...")
# 	if (user.password == auth.get('password')):
# 		# generates the JWT Token
# 		token = jwt.encode({
# 			'public_id': user.public_id,
# 			'exp' : datetime.utcnow() + timedelta(hours = 24)
# 		}, app.config['SECRET_KEY'])
# 		# token=tokenp

# 		return ({'token' : token})
# 		# return make_response(jsonify({'token' : token.decode('UTF-8')}), 201)		
# 	return make_response('Could not verify Please enter correct pasword')
# @app.route('/signup', methods =['POSt'])
# def signup():
# 	data = request.form

# 	name, email = data.get('name'), data.get('email')
# 	password = data.get('password')

# 	user = User.query.filter_by(email = email).first()
# 	if not user:
# 		user = User(
# 			public_id = str(uuid.uuid4()),
# 			name = name,
# 			email = email,
# 			password =password #  generate_password_hash(password)
# 		)
# 		db.session.add(user)
# 		db.session.commit()
# 		return make_response('Successfully registered...')
# 	else:
# 		return make_response('User already exists. Please Login...')

# @app.route('/forgot-password', methods =['GET','POST'])
# def forgot_password():
#     auth = request.form
#     if not auth or not auth.get('email'):
# 	    return ('Please enter in a KEY email')
#     user = User.query.filter_by(email = auth.get('email')).first()

#     if not user:
# 	    return ('Could not verify Please enter correct email')
#     if (user):
# 					token = jwt.encode({
# 						'public_id': user.public_id,
# 						'exp' : datetime.utcnow() + timedelta(hours = 24)
# 					}, app.config['SECRET_KEY'])	

# 					ob=s.SMTP("smtp.gmail.com",587)
# 					ob.starttls()
# 					ob.login("rkpaliwal0001@gmail.com","rkpaliwal@1310")
# 					subject="Sending email using python"
# 					# body=('http://127.0.0.1:4000/new_password/'+token)
# 					body=('http://127.0.0.1:4000/new_password')
# 					message="subject:{}\n\n{}".format(subject,body)
# 					ListOfAddress=[user.email]
# 					# passw=('file:///C:/Users/Zehntech/newflask/venv/templates/new_password.html')
# 					# body.replace(passw)
# 					ob.sendmail("rkpaliwal0001@gmail.com",ListOfAddress,message)
# 					# m=replace(body,passw)
# 					# print(m)
# 					return ("Email successfully send...")  # 
	
# @app.route('/new_password', methods =['GET','POST'])
# def new_password():
# 	if(request.method=='POST'):
# 		# email1=request.form['email']
# 		auth = request.form
# 		if not auth or not auth.get('email'):
# 			return ('Please enter in a KEY email')
# 		user = User.query.filter_by(email = auth.get('email')).first()
# 		password=request.form['password']
# 		print("HELLO...")
# 		print(password)
# 		if not user:
# 			return ('Could not verify Please enter correct email')
# 		user.password=password
# 		db.session.commit()
# 		# return "You is"+email + password

# 	return render_template('/new_password.html')
		
# if __name__ == "__main__":
# 	app.run(debug = True,port=4000)
