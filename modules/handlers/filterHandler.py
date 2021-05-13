import sqlite3 as sl
from datetime import datetime
import inspect
from modules import app
import json
from modules import epochTImeConversions
'''
input: ID of the record and the FILTERS section of the report
processing: Stores the record in the database with the id of the record to which it belongs.
Output: None
'''
def createFIlter(id, filters, sDate, sTime, eDate, eTime):
    conn = sl.connect('logs.db')
    now = datetime.now()
    app.logger.info(
        str(now.strftime("%H:%M %Y-%m-%d")) + ' ' + __file__ + ' ' + inspect.stack()[0][3] + ' ID: ' + str(id) + ' Value: ' + json.dumps(filters))
    if sDate != "" and eDate == "":
        time = epochTImeConversions.dateTimeToEpotchFilter(sDate, sTime)
        conn.execute("INSERT INTO FILTERS VALUES (?,?,?,?)", (id, "DATE_TIME",">",str(time)))
    elif sDate == "" and eDate != "":
        time = epochTImeConversions.dateTimeToEpotchFilter(eDate, eTime)
        conn.execute("INSERT INTO FILTERS VALUES (?,?,?,?)", (id, "DATE_TIME","<",str(time)))
    elif sDate == "" and eDate == "":
        pass
    else:
        stime = epochTImeConversions.dateTimeToEpotchFilter(sDate, sTime)
        etime = epochTImeConversions.dateTimeToEpotchFilter(eDate, eTime)
        conn.execute("INSERT INTO FILTERS VALUES (?,?,?,?)", (id, "DATE_TIME", "between", str(stime)+','+str(etime)))

    for key,val in filters.items():
        if val == {}:
            continue
        conn.execute("INSERT INTO FILTERS VALUES (?,?,?,?)", (id, val["targetColumn"],val["condition"], val["value"]))
    conn.commit()
