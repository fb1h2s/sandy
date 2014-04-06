import shlex, subprocess

def scanfile(filepath,extension):
  
  try:
    
    if "rtf" in extension:
      binarypath ="/var/scan/expscanner/RTFScan.exe"
    else:
      binarypath ="/var/scan/expscanner/scan.exe"
      
    #subprocess.Popen('wine "Hello world!"', shell=True)
    
    process= subprocess.Popen(['wine',binarypath,filepath,'scan','brute'], shell=False, stdout=subprocess.PIPE)
    output,error = process.communicate()
    process.stdout.close()
    return output
  except Exception:
    
    pass

def entropy(filepath,pngfile):
  
  try:
        
    #subprocess.Popen('wine "Hello world!"', shell=True)
    pngfile = pngfile+".png"
    print "I am inside entropy\n"
    binarypath ="/var/scan/others/png"
    pngoutputdir ="/var/www/sandy/entropy/"+pngfile
    filepathlen = len(filepath)
    process= subprocess.Popen([binarypath,filepath,pngoutputdir], shell=False, stdout=subprocess.PIPE)
    output,error = process.communicate()
    process.stdout.close()
    print output
    return
    
  except Exception: 
    pass    
      
def strings(filepath):
  
  try:
        
    #subprocess.Popen('wine "Hello world!"', shell=True)
    print "I am inside Strings\n"
    binarypath ="/usr/bin/strings"
    process= subprocess.Popen([binarypath,filepath], shell=False, stdout=subprocess.PIPE)
    output,error = process.communicate()
    process.stdout.close()
    print output
    return output
    
  except Exception: 
    pass


def dex2jar(filepath):
  
  try:
        
    #subprocess.Popen('wine "Hello world!"', shell=True)
    print "I am inside dex2jar\n"
    binarypath ="/bin/sh"
    d2jar ="/var/scan/others/dex2jar/dex2jar.sh"
    process= subprocess.Popen([binarypath,d2jar,filepath], shell=False, stdout=subprocess.PIPE)
    output,error = process.communicate()
    process.stdout.close()
    print output
    return output
    
  except Exception: 
    pass  

def filetype(filepath):
  
  try:
        
    #subprocess.Popen('wine "Hello world!"', shell=True)
    print "I am inside filetype\n"
    binarypath ="/usr/bin/file"
    filepathlen = len(filepath)
    process= subprocess.Popen([binarypath,filepath], shell=False, stdout=subprocess.PIPE)
    output,error = process.communicate()
    process.stdout.close()
    print output
    return output[filepathlen+1:]
  except Exception: 
    pass    
    
def retrojad(filepath):
  
  try:
        
    #subprocess.Popen('wine "Hello world!"', shell=True)
    print "I am inside retrojad\n"
    binarypath ="/var/scan/others/jadretro"
    #jadretro filename.class
    process= subprocess.Popen([binarypath,filepath], shell=False, stdout=subprocess.PIPE)
    output,error = process.communicate()
    process.stdout.close()
    print output
    #return output[filepathlen+1:]
  except Exception: 
    pass
  
def jad(filepath,folder):
  
  try:
        
    #subprocess.Popen('wine "Hello world!"', shell=True)
    print "I am inside jad\n"
    binarypath ="/var/scan/others/jad"
    #jad -d converted XXX.class
    process= subprocess.Popen([binarypath,"-s",".java","-o","-d",folder,filepath], shell=False, stdout=subprocess.PIPE)
    output,error = process.communicate()
    process.stdout.close()
    print output
    #return output[filepathlen+1:]
  except Exception: 
    pass  
  