import re

sas = open("test.txt","r")

data = sas.read()
data2 = sas.readlines()
possible_urls = []
possible_urls = re.findall(r'(https?://[^\s]+)', data) 
possible_url2 = re.findall(r'(www[^\s]+)', data)

possible_ips  = re.findall( r'[0-9]+(?:\.[0-9]+){3}', data )
for pu in possible_url2:
   possible_urls.append(pu)
for ip in possible_ips:
   possible_urls.append(ip)




for i in possible_urls:
   print i
