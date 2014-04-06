from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.proxy import *
import time
from msqlhttp import insert_html
import base64
from yara_scan_links import yara_match
import sys;
sys.setdefaultencoding("utf8")


def selenium (port,url,uid,local_ip,remote_ip):
  local_ip=local_ip
  remote_ip =remote_ip
  #remote_ip ='10.91.152'
  
  server_ip =""
  client_ip=""
  uid =uid
  myProxy = str(local_ip)+":"+str(port)
  print "Fetchning Url:"+str(url)
  proxy = Proxy({
    'proxyType': ProxyType.MANUAL,
    'httpProxy': myProxy,
    'ftpProxy': myProxy,
    'sslProxy': myProxy,
    'noProxy': '' # set this value as desired
    })

  caps = webdriver.DesiredCapabilities.FIREFOX
  proxy.add_to_capabilities(caps)
  fp = webdriver.FirefoxProfile()
  fp.set_preference("browser.download.manager.showWhenStarting", False);
  fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream");
  fp.update_preferences()
  

  driver = webdriver.Remote(
    command_executor='http://'+remote_ip+':4444/wd/hub',
    desired_capabilities=caps,browser_profile=fp)
  print "\nCalling Browser and Url\n"
  
  
  
  try:
    
    driver.get(url)
    #Wait another 15 seconds more after request is compleated
    print 
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
    print e
    pass
  
  try:
    
    print "Getting Screen Shot\n"
    s_filename = "/var/www/sandy/screenshots_links/"+str(uid)+".png"
    driver.get_screenshot_as_file(s_filename)
    time.sleep(5)
    driver.close()
    print "Browser Closed"
  except Exception as e:
    print e
    pass

if __name__ == '__main__':
  selenium()