from modules import app
import json
from flask_mail import Mail, Message
'''
input: Updated information of mail server in json format.
processing: Updates the mail server configuration according to the input.
Output:	None.
'''
def mailConfig(data):
    with open('modules/config.json') as configFile:
        config_data = json.load(configFile)
    backup_config_data = config_data
    for key, value in data.items():
        if value != "":
            config_data[key] = value
        configFile.close()
    try:
        app.config.update(config_data)
        mail = Mail(app)
        msg = Message(subject="Mail server testing email",
                      sender=config_data['MAIL_USERNAME'], recipients=[config_data['MAIL_USERNAME']])
        msg.body = 'This is an testing email to check whether the details for the mail server that you entered' \
                   'were correct or not.'
        mail.send(msg)
        with open('modules/config.json', 'w') as configFile:
            json.dump(config_data, configFile)
            configFile.close()
        configFile.close()

        return {"message":"Mail settings were updated successfully!"}
    except Exception as e:
        print(e)
        app.config.update(backup_config_data)
        return {"message":"The mail server settings were not updated. Please check the all the mail server details again."}