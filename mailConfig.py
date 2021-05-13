import json
from modules import app
from flask_mail import Mail, Message
print("------------------Mail Configuration------------------------------------------------")
while True:
    mail_server = input("Enter your SMTP outgoing mail server: ")
    portNumber = input("Enter your outgoing port number: ")
    username = input("Enter your outgoing username: ")
    numbers = [1,2]
    ssl_value = ["True", "False"]
    try:
        use_ssl = int(input("Does your mail server use SSL\nChoose 1 For Yes and 2 For No:\n1.Yes\n2.No\n:"))
    except:
        print('Please enter either 1 for YES or 2 for NO in the input when asked to enter the SSL Details.')
    password = input('Password: ')
    cpassword = input('Confirm Password: ')

    if password == cpassword and (len(password)!=0) and (use_ssl in numbers):
        with open('modules/config.json') as file:
            config_data = json.load(file)
            config_data["MAIL_SERVER"] = mail_server
            config_data["MAIL_PORT"] = portNumber
            config_data["MAIL_USE_SSL"] = ssl_value[use_ssl-1]
            config_data["MAIL_USERNAME"] = username
            config_data["MAIL_PASSWORD"] = password
            try:
                app.config.update(config_data)
                mail = Mail(app)
                msg = Message(subject="Mail server testing email",
                              sender=config_data['MAIL_USERNAME'], recipients=[config_data['MAIL_USERNAME']])
                msg.body = 'This is an testing email to check whether the details for the mail server that you entered' \
                           'were correct or not.'
                with app.app_context():
                    mail.send(msg)
                with open('modules/config.json', 'w') as configFile:
                    json.dump(config_data, configFile)
                    configFile.close()
                file.close()
                break
            except Exception as e:
                print('Please check the all the mail server details again',e)
    else:
        print('Please check the password or the SSL options again!!!')