from modules import app
from flask import url_for
from flask_mail import Mail, Message
from flask_login import current_user
from modules.models import User
from datetime import datetime
import inspect
'''
input: Senders email id and the name of the report which about ot be sent. 
processing: Sends the report as an attachment to the sendersEmail id.
Output:	None.
'''
def sendMail(senderEmail, fileName):
    try:
        now = datetime.now()
        app.logger.info(
            str(now.strftime("%H:%M %Y-%m-%d")) + ' ' + __file__ + ' ' + inspect.stack()[0][3] + ' SenderEmail ' + senderEmail + ' FIleName ' + fileName)
        mail = Mail(app)
        token = User.get_file_download_token(fileName)
        msg = Message(subject = "This is the data for which you had queried in the form.", sender=app.config['MAIL_USERNAME'], recipients=[senderEmail])
        with app.app_context():
            msg.body = f'''Please find your report at the link provided: { url_for('mailDownload', token=token, _external=True) }'''
            mail.send(msg)
        print("sent Successfully!!!!")
    except Exception as e:
        print(e)


'''
input: object of the newly registered user which contains all the information about the new user. 
processing: Sends the mail to the administrator of the organization with the username and email ID of the user.
Output:	None.
'''
def user_register(user):
    try:
        now = datetime.now()
        app.logger.info(
            str(now.strftime("%H:%M %Y-%m-%d")) + ' ' + __file__ + ' ' + inspect.stack()[0][
                3] + ' User Email ' + user.email + ' Username ' + user.username)
        mail = Mail(app)
        admin = User.query.filter_by(admin=1).first()
        msg=Message('New User',sender=app.config['MAIL_USERNAME'],
                    recipients=[admin.email])


        msg.body=f'''A new user with Email : { user.email } and Username : { user.username } has registered!
        '''
        mail.send(msg)
    except Exception as e:
        print(e)




'''
input: object of the user who have forgotten its password. 
processing: Sends the mail to the administrator of the organization with reset password token so the admin can set the 
new password for that user.
Output:	None.
'''
def send_reset_email(user):
    try:
        now = datetime.now()
        app.logger.info(
            str(now.strftime("%H:%M %Y-%m-%d")) + ' ' + __file__ + ' ' + inspect.stack()[0][
                3] + ' User Email ' + user.email + ' Username ' + user.username)
        mail = Mail(app)
        admin = User.query.filter_by(admin=1).first()
        token = user.get_reset_token()
        msg = Message('Password Reset Request',
                      sender=app.config['MAIL_USERNAME'],
                      recipients=[admin.email])
        msg.body = f'''To reset your password, visit the following link:
            {url_for('reset_token', token=token, _external=True)}
            If you did not make this request then simply ignore this email and no changes will be made.
            '''
        mail.send(msg)
        print('sent successfully!!')
    except Exception as e:
        print(e)


def sendQuery(subject, body):
    try:
        now = datetime.now()
        app.logger.info(
            str(now.strftime("%H:%M %Y-%m-%d")) + ' ' + __file__ + ' ' + inspect.stack()[0][3] +
            ' User Email ' + current_user.email + ' Subject ' +subject + ' Body: '+ body)
        mail = Mail(app)
        print(current_user.email)
        msg = Message(subject=subject,
                  sender=current_user.email,
                  recipients=["mannprajapati567@gmail.com"])
        msg.body = body
        mail.send(msg)
    except Exception as e:
        print(e)



