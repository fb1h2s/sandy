from multiprocessing import Process
import os
import time
from random import randint
from proxy_links import server
from sele_ie import selenium
from msqlhttp import done_links

def start_selenium(port,url,uid,remoteip,localip):
    print "Starting Selenium"
    selenium(port,url,uid,remoteip,localip)

def start_server(rand_port,uid,localip):
    print "Starting Server "
    server(rand_port,uid,localip)

def mprocess(i,url):
    try:
      
      localip="192.168.6.10"
      remoteip="192.168.6.12"
      uid=i
      i =i
      print " Uid is " + str(uid) +" id is :" +str(i)
      # We generate a random port and pass it on to selenium and Proxy
      rand_port = randint(8000,9000)
      procs = []
      #Append process to a list
      procs.append(Process(target=start_server,args=(rand_port,uid,localip,)))
      procs.append(Process(target=start_selenium,args=(rand_port,url,uid,remoteip,localip,)))
      #python lambda http://www.secnetix.de/olli/Python/lambda_functions.hawk
      map(lambda x: x.start(), procs)
      map(lambda x: x.join(80), procs)
      #Lets let the entire url execute for 60 seconds
      #time.sleep(80)
      print " Updating status to DB"+str(uid)
      done_links(i)
      #done(i)
      print "Terminating Proxy|Selenium\n"
     
      map(lambda x: x.terminate(), procs)
      
    except Exception as e:
      print e
      pass

if __name__ == '__main__':
  mprocess()