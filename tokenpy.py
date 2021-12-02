# from app import app,User
# from flask import Flask, request, jsonify, make_response
# import jwt
# from datetime import datetime, timedelta
# class tokenp(): 
#             auth = request.form
#             # if not auth or not auth.get('email'):
#             #    return ('Please enter in a KEY email')
            
#             user = User.query.filter_by(email = auth.get('email')).first()
#             token = jwt.encode({
#                 'public_id': user.public_id,
#                 'exp' : datetime.utcnow() + timedelta(hours = 24)
#             }, app.config['SECRET_KEY'])
#             # print(token)