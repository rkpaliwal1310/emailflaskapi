# from flask import Flask, request, jsonify, make_response
# from flask.helpers import url_for
# from flask.templating import render_template,_render
# from flask_sqlalchemy import SQLAlchemy
# import smtplib as s
# from werkzeug.security import generate_password_hash, check_password_hash
# import jwt
# from datetime import datetime, timedelta
# from functools import wraps
# from app import User

# app = Flask(__name__)

# class forgot_pass:
#         @app.route('/forgot-password', methods =['GET'])
#         def forgot_password():
#             auth = request.form
#             if not auth or not auth.get('email'):
#                 return ('Please enter in a KEY email')
#             user = User.query.filter_by(email = auth.get('email')).first()

#             if not user:
#                 return ('Could not verify Please enter correct email')
#             if (user):
#                             token = jwt.encode({
#                                 'public_id': user.public_id,
#                                 'exp' : datetime.utcnow() + timedelta(hours = 24)
#                             }, app.config['SECRET_KEY'])	

#                             ob=s.SMTP("smtp.gmail.com",587)
#                             ob.starttls()
#                             ob.login("rkpaliwal0001@gmail.com","rkpaliwal@1310")
#                             subject="Sending email using python"
#                             # body=(localhost+'/'+reset-password Api+'/' + token)
#                             body=('http://127.0.0.1:4000/forgot-password/'+token)
#                             # r=(render_template('forgot-password.html'))
#                             message="subject:{}\n\n{}".format(subject,body)
#                             # ListOfAddress=["rajkumarpaliwal138@gmail.com"]
#                             ListOfAddress=[user.email]
#                             ob.sendmail("rkpaliwal0001@gmail.com",ListOfAddress,message)
#                             # return flask.render_template('forgot-password.html')
#                             return ("Email successfully send...")  # ,r
#                             # return redirect(url_for(forgot_password))