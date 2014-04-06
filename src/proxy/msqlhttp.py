import _mysql
import sys
import MySQLdb
import sys;
reload(sys);
sys.setdefaultencoding("utf8")
sys.path.append('/var/scan/expscanner/sandbox/sandbox/src/')
'''
update_traffic(urlid=1,self.request_url,self.response_header)

Tbale: traffic
column:
`traffic_id``urlid``request``response` , filetype


'''
def update_traffic(urlid,request,response,filetype):
  
  print "Am inside Traffic Update"
  try:
    
    con = None
    
    request = _mysql.escape_string(str(request))
    response = _mysql.escape_string(str(response))
    filetype = _mysql.escape_string(str(filetype))
    
    
    try:
      Con = MySQLdb.Connect(host="127.0.0.1", port=3306, user="root", passwd="password", db="sandyfiles")
      Cursor = Con.cursor()
      sql= "INSERT IGNORE INTO sandyfiles.traffic (urlid,request,response,filetype) VALUES ('"+str(urlid)+"','"+str(request)+"','"+str(response)+"','"+str(filetype)+"' )"
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
def insert_html(urlid,html,yara_results):
  
  print "Am inside update yara + counter"
  try:
    
    con = None
    html = html.encode('base64','strict')
    html = _mysql.escape_string(html)
    yara_results = _mysql.escape_string(yara_results)
    inf_status=4
    #CONCAT( field, ' this is appended' )
    
    try:
      Con = MySQLdb.Connect(host="127.0.0.1", port=3306, user="root", passwd="password", db="sandyfiles")
      Cursor = Con.cursor()
      sql= "UPDATE `sandyfiles`.`links` SET infection_status=infection_status+1 , sigscan=CONCAT(sigscan,'"+str(yara_results)+"') WHERE `links`.`id` ="+str(urlid)
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

def update_traffic_link(urlid,request,response,filetype,html_source):
  
  print "Am inside Traffic Update"
  try:
    
    con = None
    
    #replace < with space to prevent xss
    request = request.replace("<"," ")
    request = request.replace(">"," ")
    response = str(response)
    response = response.replace("<"," ")
    response = response.replace(">"," ")
    request = _mysql.escape_string(str(request))
    response = _mysql.escape_string(str(response))
    filetype = _mysql.escape_string(str(filetype))
    try:
      html_source = html_source.decode('utf8')
    except Exception as e:
      print "utf8 decoding failed inside tupdate",e
      html_source = html_source
    html_source = _mysql.escape_string(str(html_source))
    
    
    try:
      Con = MySQLdb.Connect(host="127.0.0.1", port=3306, user="root", passwd="password", db="sandyfiles")
      Cursor = Con.cursor()
      sql= "INSERT IGNORE INTO sandyfiles.traffic_links (urlid,request,response,filetype,html_source) VALUES ('"+str(urlid)+"','"+str(request)+"','"+str(response)+"','"+str(filetype)+"' ,'"+str(html_source)+"')"
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

def done(suid):
  con = None
  #done =2 error code
  try:
    con = _mysql.connect('localhost', 'root' ,'password', 'sandyfiles')
    #just for fun assigning it here
    suid =suid
    con.query("UPDATE `sandyfiles`.`urls` SET sucess='1' WHERE `urls`.`id` ="+str(suid))
    result = con.use_result()
    
    
    ##print result.fetch_row()[0]
    
  except _mysql.Error, e:
     
    print "Error %d: %s" % (e.args[0], e.args[1])
    pass

  finally:
    if con:
      con.close()  
      
def binary_found(suid):
  con = None
  #done =2 error code
  try:
    con = _mysql.connect('localhost', 'root' ,'password', 'sandyfiles')
    #just for fun assigning it here
    suid =suid
    print "Updating Binary found"
    con.query("UPDATE `sandyfiles`.`links` SET binary_found='1' WHERE `links`.`id` ="+str(suid))
    result = con.use_result()
    
    ##print result.fetch_row()[0]
    
  except _mysql.Error, e:
     
    print "Error %d: %s" % (e.args[0], e.args[1])
    pass

  finally:
    if con:
      con.close()   

def done_links(suid):
  con = None
  #done =2 error code
  try:
    con = _mysql.connect('localhost', 'root' ,'password', 'sandyfiles')
    #just for fun assigning it here
    suid =suid
    con.query("UPDATE `sandyfiles`.`links` SET sucess='1' WHERE `links`.`id` ="+str(suid))
    result = con.use_result()
    
    
    ##print result.fetch_row()[0]
    
  except _mysql.Error, e:
     
    print "Error %d: %s" % (e.args[0], e.args[1])
    pass

  finally:
    if con:
      con.close()   

def in_use(suid):
  con = None
  #done =2 error code
  try:
    con = _mysql.connect('localhost', 'root' ,'password', 'sandyfiles')
    #just for fun assigning it here
    suid =suid
    con.query("UPDATE `sandyfiles`.`links` SET sucess='3' WHERE `links`.`id` ="+str(suid))
    result = con.use_result()
    
    
    ##print result.fetch_row()[0]
    
  except _mysql.Error, e:
     
    print "Error %d: %s" % (e.args[0], e.args[1])
    pass

  finally:
    if con:
      con.close()   