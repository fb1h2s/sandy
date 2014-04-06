import re,logging
from msl import autoattribinsert,insertattribinsert


def getextension(mime_typedb):
  mime_string = mime_typedb
  if "application/msword" in mime_string:
    logging.debug( "File is: doc")
    return "doc"
  
  elif "ms-excel" in mime_string:
    logging.debug( "File is: xls")
    return "xls"
  elif "rtf" in mime_string:
    logging.debug( "File is: rtf")
    return "rtf"
  else:
    logging.debug( "File is: unknown")
    return ""

def getfiletype(mime_typedb):
  mime_string = mime_typedb
  if "doc" in mime_string:
    logging.debug( "File is: doc")
    return "application/msword"
  
  elif "xls" in mime_string:
    logging.debug( "File is: xls")
    return "application/ms-excel"
  
  elif "rtf" in mime_string:
    logging.debug( "File is: rtf")
    return "application/rtf"
  
  else:
    logging.debug( "File is: unknown")
    return ""    

def autoattrib(metadata,uid,extension):
  
   #print type(metadata),metadata[1]
  re_author =re.compile("Author: (.*?)'")
  re_cdata = re.compile("Creation date: (.*?)'")
  re_lmod  = re.compile("Last modification: (.*?)'")
  re_title = re.compile("Title: (.*?)'") 
  re_mime =re.compile("MIME type: (.*?)'")
  smetadata = "'".join(metadata)
  #smetadata = smetatdata.encode('utf-8')
  #print smetadata

  try:
    
    #re for getting data form metadata
    if re_author.search(smetadata):
      author_name = re_author.search(smetadata)
      author= author_name.group(1)
    else:
      author = ""
    
    
    if re_title.search(smetadata):
      doc_title = re_title.search(smetadata)
      title=  doc_title.group(1)
    else:
      title = ""
    if re_cdata.search(smetadata):
      creation_date = re_cdata.search(smetadata)
      credate = creation_date.group(1)
    else:
      credate = ""
    if re_lmod.search(smetadata):
      modification_date = re_lmod.search(smetadata)
      moddate = modification_date.group(1)
    else:
      moddate = ""
    if re_mime.search(smetadata):
      mime_data = re_mime.search(smetadata)
      mime =   mime_data.group(1)
      
    else:
      mime = getfiletype(extension) 
    
    #logging.info( "%s \n %s \n %s %s\n",author_name.group(1),doc_title.group(1),creation_date.group(1),modification_date.group(1)  )
    #print author_name.group(1),doc_title.group(1),creation_date.group(1),modification_date.group(1)
    # Pass the data to insert autoattrib
    uid = uid
    
    attribid = insertattribinsert(author)
    print "Am ouside insert"
    print uid,author,title,credate,moddate,attribid,mime
    autoattribinsert(uid,author,title,credate,moddate,attribid,mime)
    
  except Exception as e:
    print e

