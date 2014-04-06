sandy
=====

Static and Dynamic exploit analysis framework. 


This is the backend code powering [Sandy] at exploit-analysis.com. Hence there would be lot of hard coded path names and no centrilized config files.   It would take a bit of time for me to beautify this code.The Front end php data viewer is not included with code.

Requirements:

Ubuntu/Linux Os



To Run:

1) Create Database sandyfiles from sandyfiles.sql.
2) Replace all mysql configurations with your username,password,and database filename.
3) Run Sandy Java Analysis ,
    
    cd src
    python mthread.py
   
   Or to schedule every few secs.
   
    cd src
   
    python samples/run.py 
   

  
