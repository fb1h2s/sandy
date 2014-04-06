from multiprocessing import Process
import os
import time
from random import randint
from proxy import server
from sele_java import selenium
from msqlhttp import done

def start_selenium(port,url,uid):
    print "Starting Selenium"
    selenium(port,url,uid)

def start_server(rand_port,uid):
    print "Starting Server "
    server(rand_port,uid)

def mprocess(i,uid,url):
    try:
      
      uid=uid
      i =i
      print " Uid is " + str(uid) +"id is :" +str(i)
      # We generate a random port and pass it on to selenium and Proxy
      rand_port = randint(8000,9000)
      procs = []
      #Append process to a list
      procs.append(Process(target=start_server,args=(rand_port,uid,)))
      procs.append(Process(target=start_selenium,args=(rand_port,url,uid,)))
      #python lambda http://www.secnetix.de/olli/Python/lambda_functions.hawk
      map(lambda x: x.start(), procs)
      map(lambda x: x.join(70), procs)
      #Lets let the entire url execute for 60 seconds
      #time.sleep(80)
      print " Updating status to DB"+str(uid)
      done(i)
      print "Terminating Proxy|Selenium\n"
     
      map(lambda x: x.terminate(), procs)
      
    except Exception as e:
      print e
      pass

if __name__ == '__main__':
  mprocess()