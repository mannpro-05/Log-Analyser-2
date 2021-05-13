import sqlite3 as sl



def deleteReport(title, userid):
    conn = sl.connect('logs.db')
    cursor = conn.execute("SELECT ID FROM RECORDS_LIST WHERE TITLE = ? AND USERID = ?", (title, userid))
    id = cursor.fetchone()
    if id == None:
        return {"message":"Record with title: " + title + " was created by someone else. You do not have permission to delete this record!."}
    conn.execute("DELETE FROM RECORDS_LIST WHERE TITLE = ?", (title,))
    conn.execute("DELETE FROM EMAIL WHERE ID = ?", (id[0],))
    conn.execute("DELETE FROM FILTERS WHERE ID = ?", (id[0],))
    conn.commit()
    return {"message":"Record with title: " + title + " has been deleted successfully!"}