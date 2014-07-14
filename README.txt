sandy
=====

Static and Dynamic exploit analysis framework. 

http://www.garage4hackers.com/entry.php?b=2532

This is the backend code powering [Sandy] at exploit-analysis.com. Hence there would be lot of hard coded path names and no centrilized config files.   It would take a bit of time for me to beautify this code.The Front end php data viewer is not included with code.

Requirements:

Ubuntu/Linux Os
And way too many things :( . I will update soon. 



To Run:

1) Create Database sandyfiles from sandyfiles.sql.
2) Replace all mysql configurations with your username,password,and database filename.
3) Run Sandy Java Analysis ,
    
    
    Starting Sandy After restart:

Make sure network is up so that the Vmsphere server has an ubuntu machine and 2 windows machine that can communicate to each other. 

Make sure DNS is set:

#cat /etc/resolv.conf

If no DNS set add a DSN server

#vi /etc/resolv.conf

nameserver 8.8.8.8
nameserver 4.4.2.2


Starting Sandy Processors: 

cd /var/scan/expscanner/sandbox/sandbox/src/

nohup python samples/run.py &
nohup python proxy/run_mprocess_ff.py &
nohup python proxy/run_mprocess_ie.py &
nohup python proxy/run_mprocess.py &


Confirm the Jobs are running:

/var/scan/expscanner/sandbox/sandbox/src# jobs -l
[1]  17613 Running                 nohup python samples/run.py &
[2]  28140 Running                 nohup python proxy/run_mprocess_ff.py &
[3]- 28143 Running                 nohup python proxy/run_mprocess_ie.py &
[4]+ 28146 Exit 1                  nohup python proxy/run_mprocess.py


What each Jobs do: 

#python samples/run.py — > This should start the Module for processing Jar files 

#python proxy/run_mprocess_ff.py  —> This start the job for processing url , that are to be processed using firefox [by default] 

#python proxy/run_mprocess_ie.py  —> This starts the Jobs for processing urls, that are to be processed using Internet Explorer [optional choice ] 


#python proxy/run_mprocess.py  —> This start the jobs for processing urls for dynamic analysis for jar files. 



That should be it:

   

  
