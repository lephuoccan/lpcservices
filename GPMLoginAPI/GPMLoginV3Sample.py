import time
from GPMLoginAPI import GPMLoginAPI
# python3 -m pip install --upgrade pip
# python3 -m pip
# pip install selenium
from selenium.webdriver.chrome import service
from selenium.webdriver.chrome.options import Options

from UndetectChromeDriver import UndetectChromeDriver

api = GPMLoginAPI('http://127.0.0.1:19995') # Alert: copy url api on GPM Login App

#  Print list off profiles in GPMLogin -------------------------
print('PROFILES ----------------------------')
profiles = api.GetProfiles()
profiles = profiles['data']
if(profiles != None):
    for profile in profiles:
        id = profile['id']
        name = profile['name']
        print(f"Id: {id} | Name: {name}")


print('START PROFILE ------------------')
startedResult = api.Start("7a3b131f-4229-4233-ba0f-f74dc5db5fd9");#, addinationArgs='--proxy-server="1.2.3.4:55"')
if(startedResult != None):
    status = bool(startedResult['success'])
    if(status):
        startedResult = startedResult['data']
        browserLocation = str(startedResult["browser_location"])
        seleniumRemoteDebugAddress = str(startedResult["remote_debugging_address"])
        gpmDriverPath = str(startedResult["driver_path"])
        # Init selenium
        options = Options()
        options.debugger_address = seleniumRemoteDebugAddress
        myService  = service.Service(gpmDriverPath)
        driver = UndetectChromeDriver(service = myService, options=options)
        driver.GetByGpm("https://fingerprint.com/products/bot-detection/")
        time.sleep(100)
        driver.close()
        driver.quit()


print('ALL DONE, PRESS ENTER TO EXIT')
input() # pause