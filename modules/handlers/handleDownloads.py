import sqlite3 as sl
import csv
import xlsxwriter
from modules.handlers import queryingHandler, pdfCreator
from datetime import datetime
import inspect
from modules import app
import time

'''
input: Id of the record and the filetype in which the report is to be exported.
processing: It gets the filtered data form the database and using that data creates the output file that the user wants.
Output: Sends the name of the file.
'''
def createDownloadFile(title="", id=0, fileType=".csv", pythonFileName=""):
    now = datetime.now()
    app.logger.info(
        str(now.strftime("%H:%M %Y-%m-%d")) + ' ' + __file__ + ' ' + inspect.stack()[0][3] + ' ID: ' + str(title) + ' FileType: ' + fileType)
    conn = sl.connect('logs.db')
    if pythonFileName == "cronjob":
        cursor = conn.execute("SELECT * FROM RECORDS_LIST WHERE ID = ?",(id,))
    else:
        cursor = conn.execute("SELECT * FROM RECORDS_LIST WHERE TITLE = ?",(title,))
    value = cursor.fetchone()
    finalData = queryingHandler.queryCreater(value[0])
    start = time.time()
    if fileType == 'csv':
        file = open('modules/downloadReports/'+ value[1] +'.csv','w',newline='')
        writer = csv.writer(file)
        rows = ["ID",value[0]],["Record-Name",value[1]],["Description", value[2]]
        writer.writerows(rows)
        temp=value[3].split(',')
        if "DATE_TIME" not in temp:
            temp.insert(0,'NUMBER OF HITS')
            writer.writerow(temp)
        else:
            writer.writerow(temp)
        if finalData == []:
            writer.writerow(["The Data which you asked for is not there in the dataBase.\
             Please apply other filters and try again!!!"])
        else:
            writer.writerows(finalData)
        file.close()
        end = time.time()
        print('Time taken to create the CSV file:', end-start)
        return value[1]+'.csv'
    elif fileType == 'xlsx':
        workbook = xlsxwriter.Workbook('modules/downloadReports/'+ value[1] +'.xlsx')
        worksheet = workbook.add_worksheet()
        worksheet.write_row(0, 0,["Record-Id",value[0]])
        worksheet.write_row(1, 0, ["Title", value[1]])
        worksheet.write_row(2, 0, ["Description", value[2]])
        temp = value[3].split(',')
        if "DATE_TIME" not in temp:
            temp.insert(0,'NUMBER OF HITS')
            worksheet.write_row(3, 0, temp)
        else:
            worksheet.write_row(3, 0, temp)
        row=4
        if finalData == []:
            worksheet.write_row(4, 0, ["The Data which you asked for is not there in the dataBase.\
             Please apply other filters and try again!!!"])
            workbook.close()
            end = time.time()
            print('Time taken to create the XLSX file:', end - start)
        else:
            for i in finalData:
                worksheet.write_row(row, 0, i)
                row+=1
            workbook.close()
            end = time.time()
            print('Time taken to create the XLSX file:', end - start)
        return value[1]+'.xlsx'
    elif fileType == 'pdf':
        pdfCreator.createPDF(finalData, value[3].split(","))
        return 'report.pdf'
