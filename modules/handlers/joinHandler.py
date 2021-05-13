from datetime import datetime
import inspect
import time
from modules import app
join_handler = {
    "APPLICATION_SIGNATURES" : "A.APPLICATION_SIGNATURES",
    "CACHECODE" : "CODE.CACHECODE",
    "CATEGORIES" : "CAT.CATEGORIES",
    "CLIENT_IP" : "IP.CLIENT_IP",
    "DOWNLOAD_CONTENT" : "D.DOWNLOAD_CONTENT",
    "FILTER_NAME" : "FNAME.FILTER_NAME",
    "FILTER_REASON" : "FREASON.FILTER_REASON",
    "HTTP_REFERER" : "H.HTTP_REFERER",
    "METHOD" : "M.METHOD",
    "REQUEST_PROFILES" : "R.REQUEST_PROFILES",
    "UPLOAD_CONTENT" : "UP.UPLOAD_CONTENT",
    "URL" : "U.URL",
    "USERAGENT" : "UA.USERAGENT",
    "USERNAME" : "UN.USERNAME",
    "USER_GROUPS" : "UG.USER_GROUPS",
    "STATUS" : "F.STATUS",
    "UPLOAD" : "F.UPLOAD",
    "DOWNLOAD" : "F.DOWNLOAD",
    "DATE_TIME" : "F.DATE_TIME"
}
exception = ['STATUS','UPLOAD','DOWNLOAD', 'DATE_TIME']

'''
input: Asked Fields in the query.
processing: It creates a join sql query to reduce the querying time and data retrival time from the database. With the
help of hte join_handler and exception variables it creates the join query. If it there in the exception then those values
are hardcoded in the final_logs.
Output: Returns the sql query.
'''
def createInnerJoinQuery(fields):
    now = datetime.now()
    app.logger.info(
        str(now.strftime("%H:%M %Y-%m-%d")) + ' ' + __file__ + ' ' + inspect.stack()[0][3] + ' Fields: ' + ','.join(fields))
    columns = []
    joinArr = []

    for i in fields:
        columns.append(join_handler[i])
        if i in exception:
            continue
        keyword = join_handler[i].split('.')[0]
        joinArr.append("INNER JOIN "+i+" "+keyword+" ON F."+i+" = " + keyword+".ID")

    columns = ','.join(columns)
    joinStr = ' '.join(joinArr)
    if "DATE_TIME" not in fields:
        return "SELECT DISTINCT COUNT(*) AS ROWCOUNT," + columns + "  FROM FINAL_LOG AS F " + joinStr, " GROUP BY "+ columns + " ORDER BY ROWCOUNT DESC"
    return "SELECT DISTINCT "+columns+" FROM FINAL_LOG AS F "+joinStr, " ORDER BY F.DATE_TIME DESC"

