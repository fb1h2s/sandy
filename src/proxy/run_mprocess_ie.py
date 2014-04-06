import sched, time,sys
#append the path of mthread
sys.path.append('/var/scan/expscanner/sandbox/sandbox/src/')
import multiproc_links_ie
import MySQLdb as mdb
from pysph import revert

s = sched.scheduler(time.time, time.sleep)
def main(sc): 
    print "Main()"
    con = mdb.connect('localhost', 'root', 'password', 'sandyfiles')
    cur = con.cursor()
    cur.execute("select id,url from links where sucess='0' and browser='2' limit 1")
    bindatas = cur.fetchall()
    querange=  len(bindatas)
    if querange > 0:
      
      print "passing",bindatas[0][0],bindatas[0][1]
      multiproc_links_ie.mprocess(bindatas[0][0],bindatas[0][1]) #id,url
      revert("[datastore1] WindowsXPRahul2/WindowsXPRahul.vmx")
    
    
    sc.enter(3, 1, main, (sc,))
s.enter(3, 1, main, (s,))
s.run()


