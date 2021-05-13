from datetime import datetime
import sqlite3 as sl
from modules import app
from modules.mailDict import sendMail
from modules.handlers import handleDownloads
conn = sl.connect('logs.db')

cursor = conn.execute("SELECT * FROM EMAIL")
value = cursor.fetchall()
minute = ''
now = datetime.now()
print(now.strftime("%H:%M %Y-%m-%d"))

def epochConvert(year=now.year, month=now.month, day=now.day, hh=now.hour, mm=now.minute):
    return int(
        datetime(int(year), int(month), int(day), int(hh), int(mm)).timestamp())

for emails in value:
    print(emails, now)
    if emails[2] == 'Daily':
        if (epochConvert() >= epochConvert(hh=emails[3].split(':')[0],mm=emails[3].split(':')[1])) and (epochConvert(hh=emails[3].split(':')[0],mm=emails[3].split(':')[1]) > (epochConvert() - 300)):
            with app.app_context():
                fileName = handleDownloads.createDownloadFile(id = emails[0],fileType = 'csv', pythonFileName = "cronjob")
                sendMail.sendMail(emails[1],fileName)
    elif emails[2] == 'Weekly':
        if (((epochConvert() >= epochConvert(hh=emails[3].split(',')[0].split(':')[0],mm=emails[3].split(',')[0].split(':')[1]))\
                and (epochConvert(hh=emails[3].split(',')[0].split(':')[0],mm=emails[3].split(',')[0].split(':')[1]) > (epochConvert() - 300)))\
                and (datetime.today().strftime('%A') == emails[3].split(',')[1])):
            fileName = handleDownloads.createDownloadFile(id = emails[0],fileType = 'csv', pythonFileName = "cronjob")
            with app.app_context():
                sendMail.sendMail(emails[1], fileName)
    else:
        if ((((epochConvert() >= epochConvert(hh=emails[3].split(',')[0].split(':')[0],mm=emails[3].split(',')[0].split(':')[1]))\
                and (epochConvert(hh=emails[3].split(',')[0].split(':')[0],mm=emails[3].split(',')[0].split(':')[1]) > (epochConvert() - 300))))\
                and (emails[3].split(',')[1] == str(now.day))):
            fileName = handleDownloads.createDownloadFile(id = emails[0],fileType = 'csv', pythonFileName = "cronjob")
            with app.app_context():
                sendMail.sendMail(emails[1], fileName)