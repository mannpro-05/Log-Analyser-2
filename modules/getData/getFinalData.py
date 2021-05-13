from modules import epochTImeConversions
from datetime import datetime
import inspect
from modules import app
import time
exception = ['STATUS','UPLOAD','DOWNLOAD', 'DATE_TIME']

'''
input: queried data from the final logs and the FIELDS from from the database.
processing: Iterates evey all the data line by line. Converts the datetime from epoch to human readable form if it is there 
in the fields. The row data gets stored in the output array (FinalData). Columns array is also created.
Output: Sends the finalData and columns generated.
'''
def getAllData(data,fields):
    now = datetime.now()
    app.logger.info(
        str(now.strftime("%H:%M %Y-%m-%d")) + ' ' + __file__ + ' ' + inspect.stack()[0][3] + ' Size: '+ str(len(data)) +' Fields: ' + ','.join(fields))
    columns = []
    finalData = []
    start = time.time()
    if "DATE_TIME" in fields:
        index = fields.index("DATE_TIME")
        for row in data:
            row = list(row)
            row[index] = epochTImeConversions.epotchToDateTime(row[index])
            finalData.append(row)
    else:
        for row in data:
            row = list(row)
            finalData.append(row)
    end = time.time()
    print("Time taken to create the final human readable form of final data",end-start)
    for i in fields:
        columns.append({"title":i})
    return finalData, columns

