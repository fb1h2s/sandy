from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.proxy import *
import time
from msqlhttp import insert_html,binary_found
import base64
from yara_scan_links import yara_match
import sys;
sys.setdefaultencoding("utf8")


def selenium (port,url,uid,remote_ip,local_ip):
  
  uid =uid
  myProxy = str(local_ip)+":"+str(port)
  print "Fetchning Url:"+str(url)
  webdriver.DesiredCapabilities.INTERNETEXPLORER['proxy'] = {
    "httpProxy":myProxy,
    "ftpProxy":myProxy,
    "sslProxy":myProxy,
    "noProxy":None,
    "proxyType":"MANUAL",
    "class":"org.openqa.selenium.Proxy",
    "autodetect":False }
    
  
  
  driver = webdriver.Remote("http://"+str(remote_ip)+":4444/wd/hub", webdriver.DesiredCapabilities.INTERNETEXPLORER)
  print "\nCalling Browser and Url\n"
  try:
    
    driver.get(url)
    #Wait another 15 seconds more after request is compleated
    time.sleep(40)
  except Exception as e:
    print e
    pass
  
  try:
    
    print " Getting Source\n"
    html_source_js = driver.page_source
    print "Scanning for signature\n"
    html_source_js = html_source_js.encode('utf-8')
    yara_results =""
    yara_results = yara_match(html_source_js)
    yara_results = "<br>Dom_Scan"+str(yara_results)
    print yara_results
    
    print "Updating Source to Db\n"
    
    insert_html(uid,html_source_js,yara_results)
    
  except Exception as e:
    
    if "save" in str(e):
      print "Binary Found, updating status"
      binary_found(uid)
    print "Exception in Source:"+str(e)
    pass
  
  try:
    
    print " Getting Screenshot\n"
    s_filename = "/var/www/sandy/screenshots_links/"+str(uid)+".png"
    driver.get_screenshot_as_file(s_filename)
    driver.close()
    print "Browser Closed"
  except Exception as e:
    print "Exception in Screenshot"+str(e)
    pass

if __name__ == '__main__':
  selenium()