import sqlite3 as sl
import time
start = time.time()
conn = sl.connect('logs.db')
def createTable():
    conn.execute('''
    CREATE TABLE CLIENT_IP
    (
    ID INT,
    CLIENT_IP FLOAT 
    );
    ''')
    conn.execute('''
    CREATE TABLE USERNAME
    (
    ID INT,
    USERNAME VARCHAR
    );
    ''')
    conn.execute('''
    CREATE TABLE METHOD
    (
    ID  INT,
    METHOD  VARCHAR 
    );
    ''')
    conn.execute('''
    CREATE TABLE URL
    (
    ID INT,
    URL VARCHAR 
    );
    ''')
    conn.execute('''
    CREATE TABLE HTTP_REFERER
    (
    ID  INT ,
    HTTP_REFERER VARCHAR 
    );
    ''')
    conn.execute('''
    CREATE TABLE USERAGENT
    (
    ID  INT ,
    USERAGENT VARCHAR 
    );
    ''')
    conn.execute('''
    CREATE TABLE FILTER_NAME
    (
    ID  INT ,
    FILTER_NAME VARCHAR 
    );
    ''')
    conn.execute('''
    CREATE TABLE FILTER_REASON
    (
    ID  INT ,
    FILTER_REASON VARCHAR 
    );
    ''')
    conn.execute('''
    CREATE TABLE CACHECODE
    (
    ID INT,
    CACHECODE VARCHAR 
    );
    ''')
    conn.execute('''
    CREATE TABLE USER_GROUPS
    (
    ID INT,
    USER_GROUPS VARCHAR 
    );
    ''')
    conn.execute('''
        CREATE TABLE REQUEST_PROFILES
        (
        ID INT,
        REQUEST_PROFILES VARCHAR 
        );
    ''')

    conn.execute('''
        CREATE TABLE APPLICATION_SIGNATURES
        (
        ID  INT,
        APPLICATION_SIGNATURES VARCHAR 
        );
    ''')
    conn.execute('''
        CREATE TABLE CATEGORIES
        (
        ID  INT,
        CATEGORIES VARCHAR 
        );
    ''')
    conn.execute('''
        CREATE TABLE UPLOAD_CONTENT
        (
        ID  INT,
        UPLOAD_CONTENT VARCHAR 
        );
    ''')
    conn.execute('''
        CREATE TABLE DOWNLOAD_CONTENT
        (
        ID  INT,
        DOWNLOAD_CONTENT VARCHAR 
        );
    ''')
    conn.execute('''
        CREATE TABLE FILTERS(
            ID INT,
            COLUMN VARCHAR,
            CONDITION VARCAHR,
            VALUE VARCHAR
        )
    ''')
    conn.execute('''CREATE TABLE EMAIL (
            ID INT,
            RECIPIENT TEXT,
            FREQUENCY TEXT,
            SCHEDULE TEXT
            );''')
    conn.execute('''
                       CREATE TABLE RECORDS_LIST 
                       (
                           ID INTEGER PRIMARY KEY AUTOINCREMENT,
                           TITLE VARCHAR UNIQUE,
                           DESCRIPTION VARCHAR ,
                           COLUMNS VARCHAR,
                           USERID INTEGER 
                       );
                   ''')
    conn.execute('''

                       CREATE TABLE INSERT_TIME
                       (
                            FILE_NAME VARCHAR ,
                           TIME_VAL INT
                       );
                   ''')
    conn.execute('''
        CREATE TABLE FINAL_LOG 
        (
            DATE_TIME DATE,
            STATUS INT,
            UPLOAD INT,
            DOWNLOAD INT,
            CLIENT_IP VARCHAR,
            USERNAME VARCHAR,
            METHOD VARCHAR,
            URL VARCHAR,
            HTTP_REFERER VARCHAR,
            USERAGENT VARCHAR,
            FILTER_NAME VARCHAR,
            FILTER_REASON VARCHAR,
            CACHECODE VARCHAR,
            USER_GROUPS VARCHAR,
            REQUEST_PROFILES VARCHAR,
            APPLICATION_SIGNATURES VARCHAR,
            CATEGORIES VARCHAR,
            UPLOAD_CONTENT VARCHAR,
            DOWNLOAD_CONTENT VARCHAR
            );
        ''')
    conn.execute('''
    CREATE TABLE ACTIVITY (
        DATE_TIME DATE_TIME,
        USERNAME TEXT,
        ACTION TEXT,
        PAGENAME TEXT
    );
    ''')
    conn.execute('''
        CREATE TABLE FILEUPDATIONINFO (
            FILENAME TEXT,
            LINENUMBER INT
        );
        ''')


try:
    createTable()
    print('table created successfully')
except:
    print('s')