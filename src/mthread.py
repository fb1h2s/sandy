#!/usr/bin/env python
import Queue
import threading
import urllib2
import time
import MySQLdb as mdb
import hashlib
from execute import scanfile,filetype,entropy,jad,retrojad,strings
from hachoir import getmeta
from msl import mssqlmeta
from msl import mssqlscan , error
from msl import mssqljobdone,zipupdate,update_uploads
from attribution import autoattrib,getextension
import logging
import magic
import zipfile
import tempfile
import re
import gnomevfs
import sys
import os,signal
from sets import Set
from yara_scan import yara_match
#integrate cuckoo sandbox .
sys.path.append('/var/scan/expscanner/sandbox/sandbox/cuck/utils/')
global file_type_flag
from csubmit  import submitmain
ms = magic.open(magic.MAGIC_NONE)
#documents = ("Text","Document")
ms.load()

ctid=0

LEVELS = {'debug': logging.DEBUG,
          'info': logging.INFO,
          'warning': logging.WARNING,
          'error': logging.ERROR,
          'critical': logging.CRITICAL}
          
level_name = "debug"
extension =""
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
	      md5hash = hashlib.md5(binary[1]).hexdigest()
	      #Get id of the uploded file
	      uploaduid = binary[0]
	      # For Doing an actual file type detection
	      filedata =  ms.buffer(binary[1])
	      logging.debug('File data  %s ',filedata )
	     
	      #python gnomevfs module 
	      logging.debug('V are here %s %s ',str(binary[0]),md5hash )
	      currentuid = binary[0]
	      binaryfound=0
	      mime_typedb = binary[4]
	      #This cant' be fully trusted and can be tampered at cleint side.
	      logging.debug('Mime String %s  ',mime_typedb )
	      
	      extension = getextension(mime_typedb)
	      logging.debug('Extension is %s ', extension )
	      
	      #print "v are hre "+ str(binary[0]) + " " + md5hash
	      #Pass file type as argnment, make a file type identifier
	      filepath="/tmp/"+md5hash+"."+extension
	      
	      
	      
	      bindata = open(filepath,'w')
	      bindata.write(binary[1])
	      bindata.close()
	      logging.debug( "I created the file" )
	      
	      #logging.debug( "File path: %s and type:%s", filepath,ftype)
	      #filedata = filetype(filepath)
	      #print filedata
	      #Confirm file type checking
	      print "File tye:"+filedata
	      file_type_flag =0
	      #Check based on strng returned by type utlity
	      if "Text" in filedata or "Document" in filedata or "ASCII" in filedata :
	        logging.debug( "I am getting metatdata" ) 
	        try:
		  
		  metadata=getmeta(filepath)
	          print metadata
                
                except Exception as e:
		  logging.debug( "Inside Exception metdatata %s",e ) 
		  metadata =""
		  pass
	        
	        #Process metat data for our Auto-detection algorithm. 
	        if metadata != "":
		  #passing meedata string and upload id
		  print "Am inside Mata data",currentuid
		  autoattrib(metadata,currentuid,extension)
		 
	        else:
		  print "no metadata",metadata
		  metatdata = ""
		
		logging.debug("I started scan")
		#Some time I can get stuck
	        scandata= scanfile(filepath,extension)
	        if 'filename' in scandata:
		  binaryfound =1
		else:
		  binaryfound= 0
		
	        logging.debug( "I am updating results to mysql")
	        #
	        mssqlscan(scandata,uploaduid,md5hash,binaryfound)
	        mssqlmeta(metadata,uploaduid,filedata)
	        #submitmain(filepath)
	        
		  
	      elif 'Zip' in filedata :
		file_type = "application/zip"
		logging.debug( "It's a Zip file\n" )
		try:
		  
		  zipmetadata=getmeta(filepath)
		  print zipmetadata
		  logging.debug( "I got zipmetadata")
		  
		except Exception as e:
		  logging.debug( "Error processing metadata:%s",e)
		  pass
		url_list = []
		# Lets read the Jar files.
		try:
		  
		  handle_file = zipfile.ZipFile(filepath, "r")
		  zipfilelist = handle_file.namelist()
		  
		except Exception as e:
		  logging.debug( "Error unziping:%s",e)
		  # These files would be marked with an error code
		  error(uploaduid)
		  print "Error Code"
		  zipfilelist =[]
		  handle_file =open("error.txt","a+b")
		  handle_file.write(md5hash)
		#create a folder with md5-hash and write files to it with md5 of file
		#save file names in database for corelation.
		#Create/Check Extracted folder
		jar_path = "/var/scan/expscanner/sandbox/sandbox/src/samples/jfiles/extracted/"
		#Create folder with md5has name
		jar_bin_path = "/var/scan/expscanner/sandbox/sandbox/src/samples/jfiles/decompiled/" + md5hash
		logging.debug( "Creating Directory %s", jar_path )
		if not os.path.exists(jar_path):
		  os.makedirs(jar_path)
		  logging.debug( "Extract Directory created")
		#Create folder with md5hash  
		if not os.path.exists(jar_bin_path):
		  os.makedirs(jar_bin_path)
		  logging.debug( "Binaries md5 Directory created")
		#we already have the directory if we reached till here. 
		'''
		try:
		  #exception handling for zipfile modulen
		  handle_file.extractall(jar_path)
		  logging.debug("Files created")
		  #Unsafe to use this method
	        except Exception as e:
		  logging.debug( "Error in Ziplib %s" , e)
		  pass
		'''
		try:
		    #The Zlib has got lot of issues.
		    for name in handle_file.namelist():
		      #data contains each of the unziped file contents
		      #logging.debug( "New file inside Zip" )
		      data = handle_file.read(name)
		      #print the name of the file insie , size and 10 bytes.
		      #print name, len(data),repr(data[:10])
		      print name, len(data)
		      classmd5 = hashlib.md5(data).hexdigest()
		      logging.debug( "Md5 of file %s" , classmd5 )
		      zipfile_path =jar_path+classmd5
		      logging.debug( "File Path to extract %s" , zipfile_path)
		      
		      try:
			
			#Check if file exist or not and write to it with md5hash
			if not os.path.exists(zipfile_path):
			  data_write = open(zipfile_path,"wb")
			  data_write.write(data)
			  data_write.close()
			  
		      except Exception as e:
			logging.debug( "Error %s writing file %s" ,e, zipfile_path)
			pass
		      
		      #Update mysql with MD5, filename and upload_id (uid) of the sample
		      #update_zipfiles(md5,filename,filetype,uid)
		      
		      
		      #Locate Binary 1)Inside zip, 2) Xor encrypted binry 3) Encrypted
		      #Check if file is a binary
		      jarfiltype = ms.buffer(data)
		      print jarfiltype
		      #Locate any Executables 
		      if "executable" in jarfiltype:
			print "Binary Found\n"
			binaryfound = 1
		     
		      #if file type is .dex then jartype =3
		      
		      '''
		      Android Analysis : This portion of the source code would not be released right now 
		      		      if the file is a dex lets convert the file from dex to jar and upload it to sandy again
        Steps:
                      
		      1)write the dex file to the jar directory with md5 as name and .dex extension
		      2) Pass the entire path name to dex2jar function
		      3) In dex2jar append path_name with .dex
		      4) Do dex2jar
		      5) New file would be md5_hash.dex2jar.jar
		      6) Read file and upload it to sandy again
		      '''
		      jartype = 0
		      if "dex" in jarfiltype:
			print "Dex file Found\n"
			jartype = 3
			
			
			
		      #Update to Mysql
		      #update_zipfiles(md5,filename,filetype,uid)
		      zipupdate(classmd5,name,jarfiltype,uploaduid)
		      
		      
		      
		      #Locate URLS 
		      possible_urls = re.findall(r'(https?://[^\s]+)', data) and re.findall(r'(www[^\s]+)', data)
		      for possible_url in possible_urls:
			url_list.append(possible_url)
		      possible_ips = re.findall( r'[0-9]+(?:\.[0-9]+){3}', data )
		      for possible_ip in possible_ips:
			print possible_ip
			url_list.append(possible_ip)
		      

		except Exception as e :
		  logging.debug( "Error in Ziplib %s" , e)
		  pass
		#check java bot signatures and decoders
		jack_bot_found =""
		decrypted_datas = ""
		from java_malware_sig import java_analysis_bot
		try:
		  jack_bot_found, decrypted_datas = java_analysis_bot(handle_file)
		except Exception as e:
		  print "Nothing Found " , e
		  pass
		  
		if len(jack_bot_found) > 5:
		  #print "Decrypted data:", decrypted_datas
		  url_list.append(decrypted_datas)
		print "Ignoring"  
		#exit()
		#list to set and back to list for unique urls      
		url_list= set(url_list)
		url_list = list(url_list)
		print url_list
		#update_uploads(filetype,metadata,binfound)
		update_uploads(file_type,zipmetadata,binaryfound,uploaduid,url_list)
		#exit()  
		
		# Check if mainfest file is inside, neceassaryf or identifying jar files.
		#any("MANIFEST" in s for s in zipfilelist) or 
		if any(".class" in s for s in zipfilelist) :
		  logging.debug( "This is a jar  file" )
		  file_type_flag = 3
		  
		    
		  
		  #iterate through the list of files inside the jar file.
		  #Check if class file 
		  #If class file pass it to retrojad, and thent to jad
		  # Decompiled files goes to /decompiled directory
		  
		  try:
		    
		    for name in handle_file.namelist():
		      #Read each file
		      class_data = handle_file.read(name)
		      #Check if file name is Manifest.txt
		      if "manifest" in name.lower():
			logging.debug( "Meta-class file located so Applet" )
			#print class_data
		      #Compute md5 hash
		      classmd5 = hashlib.md5(class_data).hexdigest()
		      #compute the file location , previous extracted files
		      classmd5_path = "/var/scan/expscanner/sandbox/sandbox/src/samples/jfiles/extracted/" +classmd5
		      logging.debug( "Md5 of file is %s and file path %s " , classmd5, classmd5_path )
		      #Check file type
		      classfiltype = ms.buffer(class_data)
		      logging.debug( "Detecting Class file type using file" )
		      print classfiltype
		      #Locate any Executables 
		      if "class" in classfiltype:
			logging.debug( "%s is a class file %s\n",classmd5, classmd5_path )
			
			
			#Send the file to jadretro and jad for decompilation
			#Check if the file exist.
			if os.path.exists(classmd5_path):
			  
			  logging.debug( "Class file exist at %s\n", classmd5_path )
			  #Jad retro is used to downgrde class file version for jad decompilation.
			  #Running jadretor will change the md5sum of the orginl file.
			  retrojad(classmd5_path)
			  jad(classmd5_path,jar_bin_path)
			  #result would be in #/var/scan/expscanner/sandbox/sandbox/src/samples/jfiles/binaries/decompiled/md5sum.jad
			  logging.debug( "The module returned from decompilers")
			  
		        
		        else:
			  
			  logging.debug( "We could not locate the class %s",classmd5_path )
			  
	              else:
			#include check if file is class file .
			
			logging.debug( "This is not a Class File, so ignoring")
		  
		      
		  
		  except Exception as e:
		    logging.debug( "Exception occured at decompile %s", e )
		    pass
		    
		  try:
		    
		    logging.debug( "Entering Java source code analysis")
		    from java_analysis import java_analysis_caller
		    java_analysis_caller(jar_bin_path,uploaduid)
		  
		  except Exception as e:
		    
		    print e
		    pass
		    
		    
		handle_file.close() 
		  		    		    		  		
	      elif 'class' in filedata :
		file_type = "application/x-java-applet"
		logging.debug( "It's a Class file\n" )
		try:
		  
		  zipmetadata=getmeta(filepath)
		  print zipmetadata
		  logging.debug( "I got Class Metadata")
		  
		except Exception as e:
		  logging.debug( "Error processing metadata:%s",e)
		  pass
		url_list = []
		# Lets read class file and write to disk.
		
		  
		  
		#create a folder with md5-hash and write class to it with md5 of file
		#save file names in database for corelation.
		#Create/Check Extracted folder
		jar_path = "/var/scan/expscanner/sandbox/sandbox/src/samples/jfiles/extracted/"
		#Create folder with md5has name
		jar_bin_path = "/var/scan/expscanner/sandbox/sandbox/src/samples/jfiles/decompiled/" + md5hash
		logging.debug( "Creating Directory %s", jar_path )
		if not os.path.exists(jar_path):
		  os.makedirs(jar_path)
		  logging.debug( "Extract Directory created")
		#Create folder with md5hash  
		if not os.path.exists(jar_bin_path):
		  os.makedirs(jar_bin_path)
		  logging.debug( "Binaries md5 Directory created")
		#we already have the directory if we reached till here. 
		
		try:
		    #The Zlib has got lot of issues.
		    if 1==1:
		      #data contains each of the unziped file contents
		      #logging.debug( "New file inside Zip" )
		      class_file_read = open(filepath,"r")
		      data = class_file_read.read()
		      class_file_read.close()
		      #print the name of the file insie , size and 10 bytes.
		      #print name, len(data),repr(data[:10])
		      #print name, len(data)
		      classmd5 = hashlib.md5(data).hexdigest()
		      logging.debug( "Md5 of file %s" , classmd5 )
		      zipfile_path =jar_path+classmd5
		      logging.debug( "File Path to extract %s" , zipfile_path)
		      
		      try:
			
			#Check if file exist or not and write to it with md5hash
			if not os.path.exists(zipfile_path):
			  data_write = open(zipfile_path,"wb")
			  data_write.write(data)
			  data_write.close()
			  
		      except Exception as e:
			logging.debug( "Error %s writing file %s" ,e, zipfile_path)
			pass
		      
		      
		      
		      #Locate Binary 1)Inside zip, 2) Xor encrypted binry 3) Encrypted
		      #Check if file is a binary
		      jarfiltype = ms.buffer(data)
		      print jarfiltype
		      #Locate any Executables 
		      if "executable" in jarfiltype:
			print "Binary Found\n"
			binaryfound = 1
		      #Update to Mysql
		      #update_zipfiles(md5,filename,filetype,uid)
		      name =""
		      zipupdate(classmd5,name,jarfiltype,uploaduid)
		      
		      
		      
		      #Locate URLS 
		      possible_urls = re.findall(r'(https?://[^\s]+)', data)
		      for possible_url in possible_urls:
			url_list.append(possible_url)
		      
		except Exception as e :
		  logging.debug( "Error in Class file read|write %s" , e)
		  pass
		#list to set and back to list for unique urls      
		url_list= set(url_list)
		url_list = list(url_list)
		print url_list
		#update_uploads(filetype,metadata,binfound)
		update_uploads(file_type,zipmetadata,binaryfound,uploaduid,url_list)
		  
		
		# Check if mainfest file is inside, neceassaryf or identifying jar files.
		#any("MANIFEST" in s for s in zipfilelist) or 
		if "class" in jarfiltype :
		  logging.debug( "This is a class file" )
		  #compute the file location , previous extracted files
		  classmd5_path = "/var/scan/expscanner/sandbox/sandbox/src/samples/jfiles/extracted/" +classmd5
		  logging.debug( "Md5 of file is %s and file path %s " , classmd5, classmd5_path )
		  #Send the file to jadretro and jad for decompilation
		  #Check if the file exist.
		  if os.path.exists(classmd5_path):
		    logging.debug( "Class file exist at %s\n", classmd5_path )
	            #Jad retro is used to downgrde class file version for jad decompilation.
		    #Running jadretor will change the md5sum of the orginl file.
		    retrojad(classmd5_path)
		    jad(classmd5_path,jar_bin_path) # Extracted ,Decompiled
		    #result would be in #/var/scan/expscanner/sandbox/sandbox/src/samples/jfiles/binaries/decompiled/md5sum.jad
	            logging.debug( "The module returned from decompilers")
			  
		        
		  else:
		    
		    logging.debug( "We could not locate the class %s",classmd5_path )
			  
	        else:
			#include check if file is class file .
		  logging.debug( "This is not a Class File, so ignoring")
		  
		
		    
		try:
		  
		  logging.debug( "Entering Java source code analysis")
		  from java_analysis import java_analysis_caller
		  #extract Main Class #Extract urls,Ip
		  java_analysis_caller(jar_bin_path,uploaduid)
		  
		  
		except Exception as e:  
		    print e
		    pass
		    		
	      elif "PDF" in filedata:
		
		#This shit is for pdf, fk y ou adobe.  
		logging.debug( "This is pdf file, am going inside." )
		#from pdf.pdf_scan.MyCode import Main_pdf
		try:
		  
		  #Main_pdf(filepath)
		  #exit()
		  print "Passed"
		except Exception as e:
		  print e
		  pass
		
		  
		
		
	      else:
		logging.debug( "I have no Idea what file type this is\n" )
		
		
		#cretae entropy files
	      logging.debug( "I started entropy" )
	      entropy(filepath,md5hash)
	      #get strings
	      strings_found = ""
	      if file_type_flag!=3:
		strings_found = strings(filepath)
	      logging.debug( "I am done entropy" )
	      logging.info("Uid=%s md5hash= %s", uploaduid,md5hash)
	      if binaryfound == 0:
		'''
		logging.info("Bin Not found %s", str(binaryfound))
		Submit Doc type as identifier
	        ctid = submitmain(filepath)
	        logging.debug( "Submited %s box taskid %s\n",filepath,ctid )
	        print ctid
	      else:
		print "Skiping Dynamic Bin found"
		ctid =0
		#logging.debug( "I am done entropy" )
		'''
	      #Scanning with yara_match
	      yara_results=""
	      yara_results = yara_match(binary[1])
	      print "Yara Signatures matched:",yara_results
	      #exit()
	      #Updating to database
	      mssqljobdone(uploaduid,md5hash,yara_results,strings_found,ctid=0)
	      logging.debug( "Am Done ")

	      #signals to queue job is done
	      self.queue.task_done()
	    except Exception as e :
	      print e
	      pass

start = time.time()

def manytasks(sas):
  try:
    print "am here"
    con = mdb.connect('localhost', 'root', 'password', 'sandyfiles')
    cur = con.cursor()
    cur.execute("select * from uploads where done IS NULL")
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
    manytasks(sas='sas')
