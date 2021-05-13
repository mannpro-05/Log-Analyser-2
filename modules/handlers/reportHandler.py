import sqlite3 as sl
from modules import app
from datetime import datetime
import inspect
from modules import epochTImeConversions
'''
input: title, description, fields from the records.
processing: inserts the records into the database.
Output: Id of the newly created record 
'''
exceprion = ['URL','HTTP_REFERER','STATUS','DOWNLOAD','UPLOAD']
def createReport(title, description, fields, userid):
    now = datetime.now()
    app.logger.info(
        str(now.strftime("%H:%M %Y-%m-%d")) + ' ' + __file__ + ' ' + inspect.stack()[0][3] + ' ' + title + \
        ' ' + description + ' '+','.join(fields))
    conn = sl.connect('logs.db')
    try:
        conn.execute("INSERT INTO RECORDS_LIST (TITLE, DESCRIPTION, COLUMNS, USERID) VALUES(?,?,?,?)",
                 (title, description, fields, userid))
    except Exception as e:
        print(e)
        return {'message':'The '+ title + ' already exists!!. Please change the value.', 'type':'error'}
    conn.commit()
    cursor = conn.execute("SELECT ID FROM RECORDS_LIST WHERE TITLE = ?", (title,))
    id = cursor.fetchone()[0]
    return id

'''
input: Id the records.
processing: creates json format object for the multiple emails and records.
Output: filter, email of the record associated to the id passed in the parameter to json format.
'''
def getEmailFilters(id):
    now = datetime.now()
    app.logger.info(
        str(now.strftime("%H:%M %Y-%m-%d")) + ' ' + __file__ + ' ' + inspect.stack()[0][3] + ' ' + str(id))
    filter = {}
    email = {}
    counter = 1
    conn = sl.connect('logs.db')
    cursor = conn.execute("SELECT * FROM FILTERS WHERE ID = ?", (id,))
    filters = cursor.fetchall()
    cursor = conn.execute("SELECT * FROM EMAIL WHERE ID = ?", (id,))
    emails = cursor.fetchall()
    for i in filters:
        if i[1] in exceprion:
            filter[str(counter)] = {
                    "targetColumn": i[1],
                    "condition": i[2],
                    "value" : i[3]
            }
        elif i[1] == "DATE_TIME":
            temp = []
            for j in i[3].split(','):
                temp.append(epochTImeConversions.epotchToDateTime(int(j)))
                filter[str(counter)] = {
                    "targetColumn": i[1],
                    "condition": i[2],
                    "value": ' AND '.join(temp)
                }
        else:
            temp = []
            for j in i[3].split(','):
                cursor = conn.execute("SELECT %s FROM %s WHERE ID = ?"%(i[1],i[1]), (j,))
                temp.append(cursor.fetchone()[0])
            filter[str(counter)] = {
                "targetColumn": i[1],
                "condition": i[2],
                "value": ' OR '.join(temp)
            }
        counter+=1
    counter = 1
    for data in emails:
        email[str(counter)] = {
            "recipient": data[1],
            "frequency": data[2],
            "schedule": data[3]
        }
        counter+=1
    return filter, email

'''
input: NONE
processing: creates HTML Table format string for the all the records and it contains all the details regarding the report.
Output:	Return HTML Table format value of all the reports.
'''

def getReport():
    now = datetime.now()
    app.logger.info(
        str(now.strftime("%H:%M %Y-%m-%d")) + ' ' + __file__ + ' ' + inspect.stack()[0][3] + ' ')
    finalData = []
    conn = sl.connect('logs.db')
    cursor = conn.execute("SELECT * FROM RECORDS_LIST GROUP BY TITLE")
    records = cursor.fetchall()

    count = 1
    for i in records:
        filters, email = getEmailFilters(i[0])
        finalData.append({
            "title": i[1],
            "description": i[2],
            "fields": i[3],
            "email": email,
            "filters": filters
        })
        count += 1
    return finalData, ["Title", "Description", "Fields", "Email", "Filters", "Actions"]

def getReportHTML():
    now = datetime.now()
    app.logger.info(
        str(now.strftime("%H:%M %Y-%m-%d")) + ' ' + __file__ + ' ' + inspect.stack()[0][3] + ' ' + str(id))
    reportsTableColumns = ["ID", "Title", "Description", "Fields", "Email", "Filters", "Actions"]
    actionCell = '''<td class = 'reportActions'>
        <div class="downloadDropdown">
            <button onclick="dropdownControl(this)" class="dropdownbutton">Download</button>
            <div class="dropdown-content">
                <button onclick="downloadReport(this,'xlsx')" name="DownloadXLS">Excel</button>
                <button onclick="downloadReport(this,'csv')" name="DownloadCSV">CSV</button>
                <button onclick="downloadReport(this,'pdf')" name="DownloadPDF">PDF</button>
            </div>
        </div>
        <button onclick="deleteReport(this)" name="Delete">Delete</button>
    </td>'''

    output = '<thead><tr class="bg-info">'
    for i in reportsTableColumns:
        output += "<th>" + i + "</th>"
    output += '</tr></thead><tbody>'

    conn = sl.connect('logs.db')
    cursor = conn.execute("SELECT * FROM RECORDS_LIST")
    records = cursor.fetchall()

    for i in records:
        print(i)
        # Adding Simple Columns
        row = "<tr>"
        row += "<td class='reportID'>" + str(i[0]) + "</td>"
        row += "<td class='reportTitle'>" + i[1] + "</td>"
        row += "<td class='reportDescription'>" + i[2] + "</td>"
        row += "<td class='reportFields'><ol>"
        for j in i[3].split(','):
            row += "<li>" + j + "</li>"
        row += "</ol></td>"

        row += "<td class='reportEmails'><ol>"

        filters, email = getEmailFilters(i[0])

        for key, val in email.items():
            print(key, val)
            row += "<li><ul>"
            row += "<li>" + email[key]["recipient"] + "</li><li>" + email[key]["frequency"] + "</li><li>" + \
                   email[key]["schedule"] + "</li>"
            row += "</ul></li>"
        row += "</ol></td>"

        row += "<td class='reportFilters'><ol>"
        for key, val in filters.items():
            row += "<li>" + filters[key]["targetColumn"] + " " + filters[key]["condition"] + " " + filters[key][
                "value"] + "</li>"
        row += "</ol></td>"

        row += actionCell

        row += "</tr>"
        output += row
    print(output)
    return output
