import time,PySQLPool
from threading import Thread

def manytasks(sas):
  connection = PySQLPool.getNewConnection(username='root', password='password', host='localhost', db='sandyfiles')
  

  for i in range(2):
    t = Thread(target=checksamples, args=(i,connection,))
    t.start() 

  

def (i,connection):
  
    print "At thread %d" % i
    query = PySQLPool.getNewQuery(connection)
    query.Query('select * from uploads')
    threadcount = len(query.record)
    print threadcount
    
    
    

