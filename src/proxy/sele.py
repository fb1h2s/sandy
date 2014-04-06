from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.proxy import *
import time


def selenium (port,url,uid):
  server_ip =""
  client_ip=""
  uid =uid
  myProxy = "192.168.6.10:"+str(port)
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
    command_executor='http://192.168.6.12:4444/wd/hub',
    desired_capabilities=caps,browser_profile=fp)
  print "\nCalling Browser and Url\n"
  try:
    
    driver.get(url)
    #Wait another 15 seconds more after request is compleated
    #time.sleep(30)
  except Exception as e:
    print e
    pass
  
  try:
   
    s_filename = "/var/www/sandy/screenshots/"+str(uid)+".png"
    driver.get_screenshot_as_file(s_filename)
  except Exception as e:
    print e
    pass
  try:
    
    time.sleep(20)
    driver.close()
    print "Browser Closed"
  except Exception as e:
    print e
    pass

if __name__ == '__main__':
  selenium()