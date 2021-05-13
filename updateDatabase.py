import os
import time
import insertRecords
import sqlite3 as sl
conn = sl.connect('logs.db')

os.chdir('/var/log/safesquid/extended/')


cursor = conn.execute("SELECT * FROM FILEUPDATIONINFO")

currentFile = cursor.fetchone()
cronTime =int(time.time())

currentFileName = int(currentFile[0])
currentFileLine = int(currentFile[1])

newFileName = 0
newFileLine = 0

max = int(os.listdir()[0].split('-')[0])

for i in os.listdir():
    if i == 'extended.log':
        continue
    elif int(i.split('-')[0]) > currentFileName:
        newFileName = int(i.split('-')[0])
        newFileLine = insertRecords.insertNewRecords(i)
    elif int(i.split('-')[0]) == currentFileName:
        currentFileLine = insertRecords.insertModifiedRecordsRecords(i, currentFileLine)

conn.execute("DELETE FROM FILEUPDATIONINFO")
conn.commit()
if newFileName != 0:
    conn.execute("INSERT INTO FILEUPDATIONINFO VALUES (?,?)", (newFileName, newFileLine))
else:
    conn.execute("INSERT INTO FILEUPDATIONINFO VALUES (?,?)",(currentFileName, currentFileLine))
conn.commit()

