

#!/usr/bin/python
# -*- coding: utf-8 -*-

import _mysql
import sys
#sys.setdefaultencoding("utf8")
import MySQLdb
def mssqlmeta(meta,uid,fileinfo):
  try:
    
    con = None
    fileinfo = _mysql.escape_string(str(fileinfo))
    meta= _mysql.escape_string(str(meta))
    try:
      con = _mysql.connect('localhost', 'root' ,'password', 'sandyfiles')
     
      uid =uid    
      con.query("UPDATE `sandyfiles`.`uploads` SET `metascan` = '"+meta+"',`fileinfo` = '"+fileinfo+"'   WHERE `uploads`.`uploadid` ="+str(uid))
      
      result = con.use_result()
      
      ##print result.fetch_row()[0]
      
    except _mysql.Error, e:
      
      print "Error %d: %s" % (e.args[0], e.args[1])
      pass

    finally:
      if con:
	con.close()
  except Exception:
    pass
    '''
    `attribid` `attrib` `time`
     INSERT INTO attribute (attrib_au,time )
VALUES (, NOW())
ON DUPLICATE KEY UPDATE time = NOW()
    '''

#insert auto atribution insert
def autoattribinsert(uid,author,title,credate,moddate,attribid,mime):
  
  print uid,author,title,credate,moddate,attribid,mime
  try:
    
    con = None
    uid =uid
    attribid= attribid
    author = _mysql.escape_string(str(author))
    title  = _mysql.escape_string(str(title))
    credate = _mysql.escape_string(str(credate))
    moddate = _mysql.escape_string(str(moddate))
    
    try:
      
      con = _mysql.connect('localhost', 'root' ,'password', 'sandyfiles')
      
      uid =uid
      #filetype
      con.query("UPDATE `sandyfiles`.`uploads` SET `title` = '"+title+"',`author` = '"+author+"',`creadate` = '"+credate+"' ,`attribid` = '"+str(attribid)+"',`filetype` = '"+mime+"' WHERE `uploads`.`uploadid` ="+str(uid))
      #print "UPDATE `sandyfiles`.`uploads` SET `title` = '"+title+"',`author` = '"+author+"',`creadate` = '"+credate+"',`moddate` = '"+moddate+"'  WHERE `uploads`.`uploadid` ="+str(uid)
      result = con.use_result()
      
      print result.fetch_row()[0]
      
    except _mysql.Error, e:
      
      print "Error %d: %s" % (e.args[0], e.args[1])
      pass

    finally:
      if con:
	con.close()
  except Exception:
    pass


def insertattribinsert(author):
  
  print "Am in attrib insert"
  try:
    
    con = None
    
    author = _mysql.escape_string(str(author))
    
    
    try:
      Con = MySQLdb.Connect(host="127.0.0.1", port=3306, user="root", passwd="password", db="sandyfiles")
      Cursor = Con.cursor()
      sql= "INSERT IGNORE INTO sandyfiles.attribute (attrib_au,time) VALUES ('"+author+"', NOW()) ON DUPLICATE KEY UPDATE time = NOW()"
      print sql
      Cursor.execute(sql)
      attribid= Cursor.lastrowid
      print attribid
      Cursor.close()
      Con.commit()
      Con.close()
      return attribid
      
      
    except _mysql.Error, e:
      
      print "Error %d: %s" % (e.args[0], e.args[1])
      pass

    finally:
      if con:
	con.close()
  except Exception as e:
    print e
    pass

      
      
def mssqlscan(scandata,suid,md5hash,binaryfound):
  con = None
  scandata= _mysql.escape_string(str(scandata))
  scandata =scandata[300:]
  try:
    con = _mysql.connect('localhost', 'root' ,'password', 'sandyfiles')
    #just for fun assigning it here
    suid =suid
    md5hash=md5hash
    con.query("UPDATE `sandyfiles`.`uploads` SET `sigscan` = '"+scandata+"',done='1',binaryfound='"+str(binaryfound)+"' ,md5='"+str(md5hash)+"' WHERE `uploads`.`uploadid` ="+str(suid))
    result = con.use_result()
    
    
    ##print result.fetch_row()[0]
    
  except _mysql.Error, e:
     
    print "Error %d: %s" % (e.args[0], e.args[1])
    pass

  finally:
    if con:
      con.close()   

def error(suid):
  con = None
  #done =2 error code
  try:
    con = _mysql.connect('localhost', 'root' ,'password', 'sandyfiles')
    #just for fun assigning it here
    suid =suid
    con.query("UPDATE `sandyfiles`.`uploads` SET done='2' WHERE `uploads`.`uploadid` ="+str(suid))
    result = con.use_result()
    
    
    ##print result.fetch_row()[0]
    
  except _mysql.Error, e:
     
    print "Error %d: %s" % (e.args[0], e.args[1])
    pass

  finally:
    if con:
      con.close()   

def urlgen(suid,url):
  con = None
  #done =2 error code
  try:
    con = _mysql.connect('localhost', 'root' ,'password', 'sandyfiles')
    #just for fun assigning it here
    suid =suid
    con.query("UPDATE `sandyfiles`.`uploads` SET urlgen='1' WHERE `uploads`.`uploadid` ="+str(suid))
    result = con.use_result()
    sql= "INSERT INTO sandyfiles.urls (url,uid) VALUES ('"+str(url)+"','"+str(suid)+"' )"
    con.query(sql)
    result2 = con.use_result()
    print result2
    
    ##print result.fetch_row()[0]
    
  except _mysql.Error, e:
     
    print "Error %d: %s" % (e.args[0], e.args[1])
    pass

  finally:
    if con:
      con.close()   
      
def mssqljobdone(suid,md5hash,yara_results,strings,ctid):
  con = None
  strings = _mysql.escape_string(str(strings))
  #scandata =scandata[300:]
  try:
    con = _mysql.connect('localhost', 'root' ,'password', 'sandyfiles')
    #just for fun assigning it here
    suid =suid
    md5hash=md5hash
    ctid=ctid
    yara_results = _mysql.escape_string(str(yara_results))
    
    con.query("UPDATE `sandyfiles`.`uploads` SET done='1', ctid='"+str(ctid)+"', sigscan2='"+str(yara_results)+"' , strings=CONCAT(strings,'"+str(strings)+"'),md5='"+str(md5hash)+"' WHERE `uploads`.`uploadid` ="+str(suid))
    result = con.use_result()
    print "Update done"
    
    print result.fetch_row()[0]
    
  except _mysql.Error, e:
     
    print "Error %d: %s" % (e.args[0], e.args[1])
    pass
    return

  finally:
    if con:
      con.close()
      return

def update_uploads(file_type,zipmetadata,binaryfound,uploaduid,urls):
  con = None
  file_type = _mysql.escape_string(str(file_type))
  zipmetadata= _mysql.escape_string(str(zipmetadata))
  urls= _mysql.escape_string(str(urls))

  try:
    con = _mysql.connect('localhost', 'root' ,'password', 'sandyfiles')
    #just for fun assigning it here

    
    con.query("UPDATE `sandyfiles`.`uploads` SET filetype='"+str(file_type)+"', metascan='"+str(zipmetadata)	+"' ,binaryfound='"+str(binaryfound)+"' , urls='"+str(urls)+"' WHERE `uploads`.`uploadid` ="+str(uploaduid))
    result = con.use_result()
    print "Update done"
    
    print result.fetch_row()[0]
    
  except _mysql.Error, e:
     
    print "Error %d: %s" % (e.args[0], e.args[1])
    pass
    return

  finally:
    if con:
      con.close()
      return
    

def update_class(class_name,class_type,urls,strings,uploaduid):
  con = None
  class_name = _mysql.escape_string(str(class_name))
  urls = _mysql.escape_string(str(urls))
  strings = _mysql.escape_string(str(strings))
  class_type= _mysql.escape_string(str(class_type))
  #jar_type	jar_main_class
  try:
    con = _mysql.connect('localhost', 'root' ,'password', 'sandyfiles')
    #just for fun assigning it here
    #Escape urls _mysql.escape_string(str(classmd5))
    #UPDATE Table SET Field=CONCAT(Field,'your extra html');
    con.query("UPDATE `sandyfiles`.`uploads` SET urls=CONCAT(urls,'"+str(urls)+"'),strings=CONCAT(strings,'"+str(strings)+"'), jar_type='"+str(class_type)+"', jar_main_class='"+str(class_name)+"' WHERE `uploads`.`uploadid` ="+str(uploaduid))
    result = con.use_result()
    print "Update done"
    
    print result.fetch_row()[0]
    
  except _mysql.Error, e:
     
    print "Error %d: %s" % (e.args[0], e.args[1])
    pass
    return

  finally:
    if con:
      con.close()
      return    
  

def zipupdate(classmd5,name,jarfiltype,uploaduid):
  
  print "Am inside Zipupdate"
  try:
    
    con = None
    
    classmd5 = _mysql.escape_string(str(classmd5))
    name = _mysql.escape_string(str(name))
    jarfiltype = _mysql.escape_string(str(jarfiltype))
    
    
    try:
      Con = MySQLdb.Connect(host="127.0.0.1", port=3306, user="root", passwd="password", db="sandyfiles")
      Cursor = Con.cursor()
      sql= "INSERT INTO sandyfiles.zipfiles (fname,md5,uid,filetype) VALUES ('"+str(name)+"','"+str(classmd5)+"','"+str(uploaduid)+"','"+str(jarfiltype)+"' )"
      print sql
      Cursor.execute(sql)
      attribid= Cursor.lastrowid
      print attribid
      Cursor.close()
      Con.commit()
      Con.close()
      
      
    except _mysql.Error, e:
      
      print "Error %d: %s" % (e.args[0], e.args[1])
      pass

    finally:
      if con:
	con.close()
  except Exception as e:
    print e
    pass


      
if __name__ == "__main__":
  mssqlmeta()