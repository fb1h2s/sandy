import sched, time,sys
#append the path of mthread
sys.path.append('/var/scan/expscanner/sandbox/sandbox/src/')
import mthread
from timeout import timeout
import create_html_template 

s = sched.scheduler(time.time, time.sleep)

@timeout(30)
def main(sc): 
    print "Main()"
    mthread.manytasks(sas="sas")
    create_html_template.create_html_d(sas='Urlgen')
    
    sc.enter(2, 1, main, (sc,))
s.enter(2, 1, main, (s,))
s.run()


