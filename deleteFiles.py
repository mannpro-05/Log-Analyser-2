import os
import time
os.chdir('modules/downloadReports')

cronTime =int(time.time())
print(cronTime)
for i in os.listdir():
    mTime = os.path.getmtime(i)
    if mTime <= cronTime - 86400:
        os.remove(i)
