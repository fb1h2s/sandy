def parsing (content_length, content):
  
			      #Check if content length is empty
			      if content_length is not None or content_length != 0 :
				print "Content-length is :"+str(content_length)
				print "Body Length is :" + str(len(self.body_file))
				#body_file_type = ms.buffer(self.body_file[:400])
				body_file_type ="buhaha"
				print "File type is "+body_file_type
				try:
				  
				  c_url = self.url.split(" ", 2)[1]
				  if c_url != "":
				    
				    c_file = c_url.split('/')[-1]
				    c_file = "/var/scan/expscanner/sandbox/sandbox/src/samples/dfiles/" +str(c_file)
				  else:
				    
				    c_url="nothing"
				    c_file = "/var/scan/expscanner/sandbox/sandbox/src/samples/dfiles/nothing"
			      
			            
			        except Exception as e:
				  print e
				  pass
				'''
				if body_file_type and "executable" in body_file_type:
				  
				  print "Found Executable Writing Executable to disk"
				  try:
				    
				    #print(b("").join(self.body))
				    print "Writing file\n"
				    data_write = open(c_file,"wb")
				    data_write.write(self.body_file)
				    data_write.close()
				  
				  except Exception as e:
				    print e
				    pass
				    
			        '''
			      
			      else:
				content_length =0
			      break
			      