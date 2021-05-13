import sqlite3 as sl
import json

exceprion = ['URL','HTTP_REFERER','STATUS','DOWNLOAD','UPLOAD']

def getData(column):
    conn = sl.connect('logs.db')
    if column in exceprion:
        return json.dumps([])
    cursor = conn.execute("SELECT * FROM %s"%(column))
    columnRecords = []
    for i in cursor.fetchall():
        columnRecords.append({
            "id" : i[0],
            "name" : i[1]
        })
    return json.dumps(columnRecords)