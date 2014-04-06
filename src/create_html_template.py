"""

Read data jar|class filed from database
Write to disk
"""
#!/usr/bin/env python
import Queue
import threading
import urllib2
import time
import MySQLdb as mdb
import hashlib
from msl import mssqlmeta,urlgen
import logging
import os
import _mysql

from sets import Set

ip_adress_sandy = "192.168.5.5"
ctid=0
ip ="http://"+ip_adress_sandy+"/sandy/exploits/"

LEVELS = {'debug': logging.DEBUG,
          'info': logging.INFO,
          'warning': logging.WARNING,
          'error': logging.ERROR,
          'critical': logging.CRITICAL}
          
level_name = "debug"
extension ="jar"

template_head = '''<html>
<head>
<b>Exploit Yo</b>
</head>

<body bgcolor="#E6E6FA">

<APPLET archive="'''

template_head_class = '''<html>
<head>
<b>Exploit Yo</b>
</head>

<body>

<APPLET code="'''

#<PARAM name="java_version" value="1.6+">
template_foot = ''' width="300" height="300">
    
</APPLET>


<body bgcolor="#E6E6FA">
</html>
'''

"""
<applet code = 'appletComponentArch.DynamicTreeApplet' 
    archive = 'DynamicTreeDemo.jar'
    width = 300
    height = 300>
    <param name="permissions" value="sandbox" />
</applet>
"""

#level_name = sys.argv[1]
level = LEVELS.get(level_name, logging.NOTSET)
logging.basicConfig(level=level)          


class BinaryGrab(threading.Thread):
    """Threaded Url Grab"""
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
    
    def run(self):
        while True:
	  
            #grabs binary from queue
            try:
	      
	      binary = self.queue.get()
	      #Get md5 hash
	      md5hash = binary[8]
	      #Get id of the uploded file
	      uploaduid = binary[0]
	      # For Doing an actual file type detection
	     
	      #python gnomevfs module 
	      logging.debug('V are here %s %s ',str(binary[0]),md5hash )
	      currentuid = binary[0]
	      binaryfound=0
	      mime_typedb = binary[4]
	      class_name = binary[19]
	      jar_path = "/var/www/sandy/exploits/"+md5hash
	      
	      
	      if not os.path.exists(jar_path):
		os.makedirs(jar_path)
		logging.debug( "Exploit Directory created")

	      logging.debug( "File Type:%s",mime_typedb)
	      #print "v are hre "+ str(binary[0]) + " " + md5hash
	      #Pass file type as argnment, make a file type identifier
	      file_data=jar_path+"/"+class_name+"."+extension
	      class_data = jar_path+"/"+class_name+".class"
	      mclass_file = class_name+".class"
	      logging.debug( "Exploit Url:%s",mclass_file)
	      
	      try:
		
	        con = mdb.connect('localhost', 'root', 'password', 'sandyfiles')
	        cur = con.cursor()
	        mclass_file = _mysql.escape_string(str(mclass_file))
	        sql= "SELECT fname FROM `zipfiles` WHERE fname like '%"+mclass_file+"%' and uid="+str(binary[0])
	        print sql
	        if cur.execute(sql):
		  
	          class_sql_name = cur.fetchone()[0]
	          print " Inside IF, this is not printed on error"
	          code = class_sql_name
	          print code
	          
	        else:
		  print "Inside else"
		  code = mclass_file
		  print code
		  
		  
	      except Exception as e:
		print "Error in DB" +str(e)
		pass
	      logging.debug( "Done DB operation" )
	      logging.debug( "The Code main class is %s", code )
	      
	      
	      if "zip" in mime_typedb:
		file_to_write = file_data
		print ".jar file"
	      if "java-applet" in mime_typedb:
		file_to_write = class_data
		print ".class file"
		
	      bindata = open(file_to_write,'w')
	      bindata.write(binary[1])
	      bindata.close()
	      logging.debug( "I created jar file %s",file_to_write )
	      
	      html_template = template_head+class_name+".jar"+"\" code=\""+code+"\" "+template_foot
	      html_template_class = template_head_class+code+"\" "+ template_foot
	      #print html_template
	      file_html=jar_path+"/exploit.html"
	      
	      url =ip+md5hash+"/exploit.html"
	      logging.debug( "Exploit Url:%s",url)
	      
	      if "zip" in mime_typedb:
		html_to_write = html_template
		print " Jar template written"
	      if "java-applet" in mime_typedb:
		html_to_write = html_template_class
		print "Class template written"
		
	      
	      html_data = open(file_html,'w')
	      html_data.write(html_to_write)
	      html_data.close()
	      logging.debug( "I created jar file" )
	      
	      urlgen(uploaduid,url)
	      logging.debug( "Updating data| Status to Db" )
	      logging.debug( "Am Done ")

	      #signals to queue job is done
	      self.queue.task_done()
	    except Exception as e :
	      print e
	      pass

start = time.time()

def create_html_d(sas):
  try:
    print "am here"
    con = mdb.connect('localhost', 'root', 'password', 'sandyfiles')
    cur = con.cursor()
    cur.execute("select * from uploads where jar_main_class IS NOT NULL AND jar_type ='1' AND urlgen='0' and jar_main_class <> ''")
    bindatas = cur.fetchall()
    querange=  len(bindatas)
    print querange
    cur.close()
    con.close()
    binaries = []
    #if querange > 0:
    queue = Queue.Queue()  
    for stuffs in bindatas:
      
      logging.debug( "Appending bin stuffs\n" )
      #Putting jobs in quer
      binaries.append(stuffs)
        
    #spawn a pool of threads, and pass them queue instance 
    #for i in range(int(querange)/2): total by 2
    if querange > 0:
      
      for i in range(2):
	
	t = BinaryGrab(queue)
        t.setDaemon(True)
        t.start()

    #populate queue with data
      for binary in binaries:
	
        logging.debug( "Putting stuffs in Queu\n" )
        #invoke the que
        queue.put(binary)
        
	
        #wait on the queue until everything has been processed
        queue.join()
  except Exception as e:
    print e
    pass

    
if __name__ == "__main__":
    create_html_d(sas='sas')
