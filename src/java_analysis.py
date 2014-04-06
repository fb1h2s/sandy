'''
Input: Path to folder with .java sourc code
Function returns class name and checks if jar is a midlet or applet
'''

import os,re
from msl import update_class

def read_java_code_domain(dir_read):
  print "Directory to scan"+dir_read
  possible_urls = []
  os.chdir(dir_read)
  for files in os.listdir("."):
    #If Applet or midlet found then return values
    #Read each file and look for main class
    full_path = dir_read+"/"+files
    print full_path
    
    try:
      
      java_file = open(full_path,"r")
      data = java_file.read()
      possible_urls = re.findall(r'(https?://[^\s]+)', data) 
      possible_url2 = re.findall(r'(www[^\s]+)', data)

      possible_ips  = re.findall( r'[0-9]+(?:\.[0-9]+){3}', data )
      #Java functions
      possible_java = re.findall('^.exec((.*?)^)',data)
      
      #java strings
      possible_strings=re.findall(r'\"(.+?)\"',data)
      possible_strings = set(possible_strings)
      possible_strings = list(possible_strings)
      return_possible_strings =  '\n'.join(map(str, possible_strings))
      
      
      for pu in possible_url2:
	
	possible_urls.append(pu)
	
      for ip in possible_ips:
	
        possible_urls.append(ip)
        
      for java_functions in possible_java:
	
        possible_urls.append(java_functions)
      
      
        
      print possible_urls
      possible_urls= set(possible_urls)
      possible_urls = list(possible_urls)
      
      
      java_file.close()
	  

    except Exception as e:
      print e
      pass
  return (possible_urls,return_possible_strings)
  

def read_java_code(dir_read):
  
  print "Directory to scan"+dir_read
  afound =0
  mfound =0
  error =3
  class_name = ""
  applet = "applet"
  midlet = "midlet"
  extends = "extends"
  app_type = 0 # 1: Applet 2: Midlet
  os.chdir(dir_read)
  for files in os.listdir("."):
    #If Applet or midlet found then return values
    #Read each file and look for main class
    full_path = dir_read+"/"+files
    print full_path
    
    try:
      
      java_file = open(full_path,"r")
      java_code = java_file.readlines()
      if (java_code):
	
	for line in java_code:
	  
	  if re.search(r"\b" + extends + r"\b", line.lower()) and re.search(r"\b" + midlet + r"\b",line.lower()):
	    #print "found"
	    print "Midlet Class Found: "+line.split()[2]
	    print line
	    class_name=line.split()[2]
	    mfound =2
	    return (mfound,afound,class_name)
	    
	  elif re.search(r"\b" + extends + r"\b", line.lower()) and re.search(r"\b" + applet + r"\b",line.lower()):
	    print line
	    afound =1
	    class_name=line.split()[2]
	    print "Applet Class Found: "+line.split()[2]
	    return (mfound,afound,class_name)
	  
	
	  
    except Exception as e:
      print e
      pass
  
def java_analysis_caller(jar_bin_path,uploaduid):
  class_value= read_java_code(jar_bin_path)
  print class_value
  #return (mfound,afound,class_name)   
  ##Applet type- 0: Unknow 1: Applet 2: Midlet
  if class_value is not None:
    
    if class_value[0] ==2:
      
      print "Midlet Found: "+class_value[2]
      applet_type = 2
      class_name = class_value[2]
      #print class_name
      
    elif class_value[1] ==1:
      print "Applet Found: "+class_value[2]
      applet_type = 1
      class_name = class_value[2]
    else:
      applet_type =0
      class_name = ""
  else:
    class_name =""
    applet_type =3
  
  urls =[]
  strings = []
  urls,strings = read_java_code_domain(jar_bin_path)
  print "The urls:"
  print urls
  print "The string:"
  print strings
  print class_name,applet_type,uploaduid,urls
  update_class(class_name,applet_type,urls,strings,uploaduid)
if __name__ == "__main__":
  
  java_analysis_caller("/var/scan/expscanner/sandbox/sandbox/src/samples/jfiles/decompiled/b7a797fe64365a0059e2ca373d7dc073/",uploaduid=2)
  #read_java_code_domain()