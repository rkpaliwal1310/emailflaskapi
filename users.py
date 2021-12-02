# from flask_sqlalchemy import SQLAlchemy
# from app import db,app

# db = SQLAlchemy(app)
# class User(db.Model):     

#         id = db.Column(db.Integer, primary_key = True)
#         public_id = db.Column(db.String(50), unique = True)
#         name = db.Column(db.String(100))
#         email = db.Column(db.String(70), unique = True)
#         password = db.Column(db.String(80))

#         def __init__(self, id,name,password):
#             self.id=id
#             self.name=name
#             self.password=password

#         @classmethod
#         def find_by_name(cls,name):
#             return cls.query.filter_by(name=name).first()

#         @classmethod
#         def find_by_id(cls,id):
#             return cls.query.filter_by(id=id).first()
