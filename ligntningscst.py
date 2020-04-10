from selenium import webdriver
# from selenium.webdriver import ActionChains
import time
import os
from ftplib import FTP


# import win32api
# import win32con

def ftp_connect(host, username, password):
    ftp = FTP()
    # ftp.set_debuglevel(2)
    ftp.connect(host, 21)
    ftp.login(username, password)
    print(ftp.getwelcome())
    return ftp


def upload_file(ftp, remotepath, localpath):
    bufsize = 1024
    fp = open(localpath, 'rb')

    ftp.storbinary('STOR ' + remotepath, fp, bufsize)
    ftp.set_debuglevel(0)
    fp.close()


def lightningscst(url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--disable-gpu')
    # browser = webdriver.Chrome(chrome_options=chrome_options, executable_path="./chromedriver")
    browser = webdriver.Chrome(executable_path="./chromedriver")
    browser.maximize_window()
    data = time.strftime('%Y.%m.%d', time.localtime(time.time()))
    datatime = time.strftime('%Y-%m-%d-%H_%M_%S', time.localtime(time.time()))
    # filedirectory = 'E:/PYTHONPROJECT/LIGNTNINGSCREENSHOT/image/' + data
    filedirectory = 'D:/lightningScreenshot/image/' + data
    if not os.path.exists(filedirectory):
        os.makedirs(filedirectory)
    filename = filedirectory + '/' + datatime + '.png'
    try:
        browser.get(url)
        time.sleep(1)
    except:
        text = "获取URL失败\n"
        browser.quit()
        return text
    try:

        # time.sleep(3)
        # browser.execute_script("document.body.app-root.app-lightning-instrument.div.style.zoom='0.5'")
        # tar = browser.find_element_by_id('lightning-box')
        # browser.execute_script("argument[0].scrollIntoView();", tar)
        # ActionChains(browser).move_to_element(tar).perform()
        # browser.find_element_by_id('lightning-box')

        # for i in range(300):
        #     print(i)
        # ActionChains(browser).move_to_element(browser.find_element_by_id('lightning-box')).perform()
        # win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, -400, 0, -1000, 0)
        # browser.find_element_by_link_text("散点图").click()
        # document.querySelector("body > app-root > app-lightning-instrument")
        time.sleep(5)
        browser.get_screenshot_as_file(filename)
        browser.quit()
        if os.path.exists(filename):
            ftpname = '/' + 'lightning' + datatime + '.png'
            try:
                ftp = ftp_connect("172.24.16.40", "sbs", "vaisala")
                upload_file(ftp, ftpname, filename)
                ftp.quit()
            except:
                print("ftperror")
        return filename
    except:
        text = "保存文件失败\n"
        return text
