# import smtplib as s

# from flask import sessions
# from app import User, login,request,db
# class psw:
#         ob=s.SMTP("smtp.gmail.com",587)
#         ob.starttls()
#         ob.login("rkpaliwal0001@gmail.com","rkpaliwal@1310")
#         subject="Sending email using python"
#         body="Hello.."

#         message="subject:{}\n\n{}".format(subject,body)
#         ListOfAddress=["rajkumarpaliwal138@gmail.com"]
#         # ListOfAddress=[User.email('email')]
#         ob.sendmail("rkpaliwal0001@gmail.com",ListOfAddress,message)

#         if login in sessions:
#                 auth = request.form

#                 user = User.query.filter_by(email = auth.get('email')).first()

#                 if (user.email == auth.get('eamil')):
                
#                  sessions.query(user).filter(user.email).update({user.password:"Mr."+user.password}, synchronize_session = False)
#                  db.session.commit()

               