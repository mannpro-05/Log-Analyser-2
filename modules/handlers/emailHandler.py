import sqlite3 as sl
import inspect
from modules import app
from datetime import datetime
import json
'''
input: ID of the record and the EMAILS section of the report
processing: Stores the record in the database with the id of the record to which it belongs.
Output: None
'''
def createEmail(id, emails):
    now = datetime.now()
    app.logger.info(
        str(now.strftime("%H:%M %Y-%m-%d")) + ' ' + __file__ + ' ' + inspect.stack()[0][3] +' ID: '+str(id) + ' Value: ' + json.dumps(emails))
    conn = sl.connect('logs.db')
    for key, val in emails.items():
        if val == {}:
            continue
        conn.execute("INSERT INTO EMAIL VALUES (?,?,?,?)", (id, val["recipient"], val["frequency"], val["schedule"]))
    conn.commit()

