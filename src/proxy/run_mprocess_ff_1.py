import sched, time,sys
#append the path of mthread
sys.path.append('/var/scan/expscanner/sandbox/sandbox/src/')
import multiproc_ff
import MySQLdb as mdb
from msqlhttp import in_use

s = sched.scheduler(time.time, time.sleep)
def main(sc): 
    print "Main()"
    con = mdb.connect('localhost', 'root', 'password', 'sandyfiles')
    cur = con.cursor()
    cur.execute("select id,uid,url from links where browser='1' and sucess='0' limit 1")
    bindatas = cur.fetchall()
    querange=  len(bindatas)
    if querange > 0:
      
      print "passing",bindatas[0][0],bindatas[0][1],bindatas[0][2]
      in_use(bindatas[0][0])
      multiproc_ff.mprocess(bindatas[0][0],bindatas[0][1],bindatas[0][2]) #id,uid,url
      
    
    sc.enter(6, 1, main, (sc,))
s.enter(6, 1, main, (s,))
s.run()


