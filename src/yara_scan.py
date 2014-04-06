import yara

rules = yara.compile(filepaths={

	'JavaExploit':'/var/scan/expscanner/sandbox/sandbox/yara-ctypes/yara/rules/java/exploit.yar',
	'InternetExplorer':'/var/scan/expscanner/sandbox/sandbox/yara-ctypes/yara/rules/ie/exploit.yar',
	'ClamAv':'/var/scan/expscanner/sandbox/sandbox/yara-ctypes/yara/rules/clam_av/clam_av.yar',
	'test':'/var/scan/expscanner/sandbox/sandbox/yara-ctypes/yara/rules/clam_av/test.yar'
})



def yara_match(scan_file):
  
  matches = rules.match(data=scan_file)
  return matches
  
    
    
if __name__ == "__main__":
  fo = open("test1.txt", "r+")
  scan_file = fo.read();
  matches =""
  matches=yara_match(scan_file)
  print matches
