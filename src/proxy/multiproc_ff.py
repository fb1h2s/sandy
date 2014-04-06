from multiprocessing import Process
import os
import time
from random import randint
from proxy_links import server
from sele_ff import selenium
from msqlhttp import done_links

def start_selenium(port,url,uid,local_ip,remote_ip):
    print "Starting Selenium"
    selenium(port,url,uid,local_ip,remote_ip)

def start_server(rand_port,uid,local_ip):
    print "Starting Server "+str(local_ip)
    server(rand_port,uid,local_ip)

def mprocess(i,uid,url):
  
    try:
      
      local_ip ='192.168.6.10'
      remote_ip ='192.168.6.11'
      
      uid=i
      i =i
      print " Uid is " + str(uid) +"id is :" +str(i)
      # We generate a random port and pass it on to selenium and Proxy
      rand_port = randint(6000,7000)
      procs = []
      #Append process to a list
      procs.append(Process(target=start_server,args=(rand_port,uid,local_ip,)))
      procs.append(Process(target=start_selenium,args=(rand_port,url,uid,local_ip,remote_ip)))
      #python lambda http://www.secnetix.de/olli/Python/lambda_functions.hawk
      map(lambda x: x.start(), procs)
      map(lambda x: x.join(70), procs)
      #Lets let the entire url execute for 60 seconds
      #time.sleep(80)
      print " Updating status to DB"+str(uid)
      done_links(i)
      print "Terminating Proxy|Selenium\n"
     
      map(lambda x: x.terminate(), procs)
      
    except Exception as e:
      print e
      pass

if __name__ == '__main__':
  mprocess('1','1','http://www.gogole.com')