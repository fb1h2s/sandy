import yara

matches      = dict()
rules = yara.compile(filepaths={

	"Exploits":"/var/scan/expscanner/sandbox/sandbox/yara-ctypes/yara/rules/browser/exploits.yar",
	"Exploit-kits":"/var/scan/expscanner/sandbox/sandbox/yara-ctypes/yara/rules/browser/exploit_kits.yar",
	"Java_Script":"/var/scan/expscanner/sandbox/sandbox/yara-ctypes/yara/rules/jsunpack/jsunpack.yar",
	"Exploits-ie":"/var/scan/expscanner/sandbox/sandbox/yara-ctypes/yara/rules/ie/exploit.yar",
	"Exploits-js":"/var/scan/expscanner/sandbox/sandbox/yara-ctypes/yara/rules/jsclassifier.yar",
	"Exploits-url":"/var/scan/expscanner/sandbox/sandbox/yara-ctypes/yara/rules/urlclassifier.yar"
})



def yara_match(scan_file):
  yara_rules =[]
  matches = rules.match(data=scan_file)
  ##matches = str(matches)
  keys = matches.keys()
  for keys in matches:
    each_value = matches[keys]
    for each in each_value:
      match = keys+":"+each["rule"]
      #print match
      yara_rules.append(match)
  
  return yara_rules 
    
if __name__ == "__main__":
  fo = open("test1.txt", "r+")
  scan_file = fo.read();
  match = yara_match(scan_file)
  print match
  