import sqlite3 as sl

def getActivity():
    conn = sl.connect('logs.db')
    cursor = conn.execute("SELECT * FROM ACTIVITY")
    return cursor.fetchall()