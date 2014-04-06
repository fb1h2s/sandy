# -*- coding: cp1252 -*-
# <PythonProxy.py>
#
#Copyright (c) <2009> <Fábio Domingues - fnds3000 in gmail.com>
#
#Permission is hereby granted, free of charge, to any person
#obtaining a copy of this software and associated documentation
#files (the "Software"), to deal in the Software without
#restriction, including without limitation the rights to use,
#copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the
#Software is furnished to do so, subject to the following
#conditions:
#
#The above copyright notice and this permission notice shall be
#included in all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
#OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
#NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
#HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
#WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
#OTHER DEALINGS IN THE SOFTWARE.

"""\

"""

import socket, thread, select
try:
    from http_parser.parser import HttpParser
except ImportError:
    from http_parser.pyparser import HttpParser
from http_parser.util import b
import magic
import os
from msqlhttp import update_traffic_link,binary_found,insert_html
from yara_scan_links import yara_match
import zlib


ms = magic.open(magic.MAGIC_NONE)
ms.load()


__version__ = '0.1.0 Draft 1'
BUFLEN = 8337
VERSION = 'Python Proxy/'+__version__
HTTPVER = 'HTTP/1.1'

class ConnectionHandler:
    def __init__(self, connection, address, timeout):
        self.body_file =""
        self.p = HttpParser()
	self.body = []
	self.request_url = ""
	self.response_header = []
	self.header_done = False
        self.url =""
        self.controller = []
        self.controller_ip = []
        self.client = connection
        self.client_buffer = ''
        self.timeout = timeout
        self.method, self.path, self.protocol = self.get_base_header()
        if self.method=='CONNECT':
            self.method_CONNECT()
        elif self.method in ('OPTIONS', 'GET', 'HEAD', 'POST', 'PUT',
                             'DELETE', 'TRACE'):
            self.method_others()
        self.client.close()
        self.target.close()
        #clear
        #print self.controller , self.controller_ip

    def get_base_header(self):
        while 1:
            self.client_buffer += self.client.recv(BUFLEN)
            end = self.client_buffer.find('\n')
            if end!=-1:
                break
        #We dont wann those google.com urls.        
        if not "127.0.0.1" in self.client_buffer[:end]:
	  
	  #Insert Url into database here
          self.url = '%s'%self.client_buffer[:end]
          
          
        data = (self.client_buffer[:end+1]).split()
        self.client_buffer = self.client_buffer[end+1:]
        #print data
        return data

    def method_CONNECT(self):
        self._connect_target(self.path)
        self.client.send(HTTPVER+' 200 Connection established\n'+
                         'Proxy-agent: %s\n\n'%VERSION)
        self.client_buffer = ''
        self._read_write()        

    def method_others(self):
        self.path = self.path[7:]
        i = self.path.find('/')
        host = self.path[:i]        
        path = self.path[i:]
        self._connect_target(host)
        self.target.send('%s %s %s\n'%(self.method, path, self.protocol)+
                         self.client_buffer)
        self.client_buffer = ''
        self._read_write()

    def _connect_target(self, host):
        i = host.find(':')
        if i!=-1:
            port = int(host[i+1:])
            host = host[:i]
            #print host
        else:
            port = 80
        try:
	  
	  
          (soc_family, _, _, _, address) = socket.getaddrinfo(host, port)[0]
          self.target = socket.socket(soc_family)
          self.target.connect(address)
          
        except Exception as e:
	  address =host
	  print "Error Connecting to:"+str(address)
	  connect_ip = "Error Connecting to:"+str(address)
	  update_traffic_link(urlid,connect_ip,"Unable to Connect","Nil","")
	  # insert to db here
        #Concat data to string
        self.request_url = str(host)+" | "+str(address)+" | "+str(self.url) #debug
        #print self.request_url


    def _read_write(self):
        
        time_out_max = self.timeout/3
        socs = [self.client, self.target]
        count = 0
        while 1:
            count += 1
            (recv, _, error) = select.select(socs, [], socs, 3)
            if error:
                break
            if recv:
                for in_ in recv:
		    try:
		      
		      #print " Receving Data "
                      data = in_.recv(10000)
                    except Exception as e:
		      print e
		      pass
		    
                    if in_ is self.client:
                        out = self.target
                    else:
                        out = self.client
                    try:
		      
		      
		      if data:
			  #column 25
			  #Dig here to analysis the traffic
			  #print data
			  try:
			    #Lets parse the data using http_parser modules
			    
			    recved = len(data)
			    #
			    #print "We received so far "+ str(recved)
			    nparsed = self.p.execute(data, recved)
			    assert nparsed == recved
			    # Check 
			    if self.p.is_headers_complete() and not self.header_done:
			      
			      #Header is an ordered dictionary 
			      header_s = self.p.get_headers()
			      
			     
			      # Lets beautify it and print it.
			      for header, value in header_s.items():
				
				#Print Response
				# Connection : close format
				res_header = header+": "+value
				self.response_header.append(res_header)
			      
			        self.header_done = True
			        #Put header to Database.
			        
			   
			    #Check if the boday is partial, if then append the body
			    if self.p.is_partial_body():
			      
			      self.body.append(self.p.recv_body())
			      #print "appending body" +self.p.recv_body()
			      #Append data body recived to a list
			      #print self.body
			      
			    # If the parsing of current request is compleated 
			    if self.p.is_message_complete():
			      
			      try:
				
				try:
				  
				  content_length = self.p.get_headers()['content-length']
			        
			        except Exception as e:
				  print "Exception in Body retrive-sub"+str(e)
				  content_length = 0
				  pass
				  
			        self.body_file = "".join(self.body)
			        body_file_type = ms.buffer(self.body_file[:1024])
			        signature_scan = ""
			        html_source =""
			        html_body=""
			        html_body = self.body_file
			        if "gzip" in body_file_type:
				  try:
				    
				    print " Decoding GZIp html\n"
				    html_body = zlib.decompress(html_body, 16+zlib.MAX_WBITS)
				    #print "source"+str(html_body)
				  except Exception as e:
				    print "Error gzip decoding:"+str(e)
				    
				  
			        
			        print urlid 
			        signature_scan_body = yara_match(html_body)
			        signature_scan_request = yara_match(self.request_url)
			        signature_scan_response =""
			        self_response = ""
			        try:
				  #This is a list convert to string and do the check
				  print self.response_header
				  self_response = ''.join(self.response_header)
				  if "Content-Disposition:" in self_response and "attachment;" in  self_response:
				    signature_scan_response = "Forced-file-download"
				    print " Signatured matched in response"
				    
				except Exception as e:
				  print e,"Error in header_match"
			        signature_scan = str(signature_scan_body) +""+str(signature_scan_request)+""+signature_scan_response
  
			        #print self.request_url
			        #print self.response_header
			        #print body_file_type
			        
			        
			        if len(signature_scan) > 6:
				  try:
				    
				    print " Signatured found and Updating\n"
				    body_file_type = "Signature_Matched: "+signature_scan+" ing "+body_file_type
				    insert_html(urlid,html_body,signature_scan)
				    html_source = html_body
				  
				  except Exception as e:
				    print "Error in Traffic Signature"+str(e)
				  
				print " Trffic Updated\n"
			        update_traffic_link(urlid,self.request_url,self.response_header,body_file_type,html_source)
				  
			        if "executable" in body_file_type:
				  print "\nExecutable found\n"
				  binary_found(urlid)
				  
				  
			      except Exception as e:
				print "Exception in Body retrive"+str(e)
				content_length = 0
				pass
			      
			      
			  except Exception as e:
			    print e
			    pass

			  #if filetype in traffice == jar,class , pdf,flash, execute
			  #save those files
			  
			  
			  out.send(data)
			  count = 0
		      
	
	            except Exception as e:
		      print e
		      pass
            if count == time_out_max:
                break

def server(port,uid,host):
    
    try:
      
      #Selenium Server Configuration
      print "Proxy at "+str(host)+":"+str(port)
      global urlid
      urlid = uid
      host=""+str(host)
      IPv6=False
      timeout=50
      handler=ConnectionHandler
      
      
      if IPv6==True:
	  soc_type=socket.AF_INET6
      else:
	  soc_type=socket.AF_INET
      try:
	
        soc = socket.socket(soc_type)
        soc.bind((host, port))
        #Lets print the current server config
        print "Serving on %s:%d."%(host, port)#debug
        soc.listen(0)
      except Exception as e:
	print "Exception at proxy " +str(e)
	pass
      
      while 1:
	  thread.start_new_thread(handler, soc.accept()+(timeout,))
    except Exception as e:
      print e
      pass

if __name__ == '__main__':
    server(1222,'1','10.91.1.148')
