"""
    BYPASS reCaptcha By YouTube Channel: NIKO TECH
    Captcha + Others By github@Mybdye 2022.03.24
"""
import os
import sys
import platform
import time
import random
import urllib
import requests
import undetected_chromedriver as uc
uc.TARGET_VERSION = 105

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

audioToTextDelay = 10
delayTime = 2
audioFile = "\\payload.mp3"
urlLogin = 'https://hax.co.id/login'
urlExtendRenew = 'https://hax.co.id/vps-renew/'
SpeechToTextURL = 'https://speech-to-text-demo.ng.bluemix.net/'

# secret
USERNAME = os.environ['USERNAME']
PASSWORD = os.environ['PASSWORD']
try:
    BARKKEY = os.environ['BARKKEY']
    barkKey = 1
except:
    print('No BarkKey')
    barkKey = 0

def delay():
    time.sleep(random.randint(3, 4))

def audioToText(audioFile):
    driver.execute_script('''window.open("","_blank")''')
    driver.switch_to.window(driver.window_handles[1])
    driver.get(SpeechToTextURL)

    delay()
    audioInput = driver.find_element(By.XPATH, '//*[@id="root"]/div/input')
    audioInput.send_keys(audioFile)

    time.sleep(audioToTextDelay)

    text = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[7]/div/div/div/span')
    while text is None:
        text = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[7]/div/div/div/span')

    result = text.text

    driver.close()
    driver.switch_to.window(driver.window_handles[0])

    return result

def reCAPTCHA():
    g_recaptcha = driver.find_elements(By.CLASS_NAME, 'g-recaptcha')[0]
    outerIframe = g_recaptcha.find_element(By.TAG_NAME, 'iframe')
    outerIframe.click()

    iframes = driver.find_elements(By.TAG_NAME, 'iframe')
    audioBtnFound = False
    audioBtnIndex = -1

    for index in range(len(iframes)):
        driver.switch_to.default_content()
        iframe = driver.find_elements(By.TAG_NAME, 'iframe')[index]
        driver.switch_to.frame(iframe)
        driver.implicitly_wait(delayTime)
        try:
            audioBtn = driver.find_element(By.ID, "recaptcha-audio-button")
            audioBtn.click()
            audioBtnFound = True
            audioBtnIndex = index
            break
        except Exception as e:
            pass

    if audioBtnFound:
        try:
            while True:
                # get the mp3 audio file
                src = driver.find_element(By.ID, "audio-source").get_attribute("src")
                print("[INFO] Audio src: %s" % src)

                # download the mp3 audio file from the source
                urllib.request.urlretrieve(src, os.getcwd() + audioFile)

                # Speech To Text Conversion
                key = audioToText(os.getcwd() + audioFile)
                print("[INFO] Recaptcha Key: %s" % key)

                driver.switch_to.default_content()
                iframe = driver.find_elements(By.TAG_NAME, 'iframe')[audioBtnIndex]
                driver.switch_to.frame(iframe)

                # key in results and submit
                inputField = driver.find_element(By.ID, "audio-response")
                inputField.send_keys(key)
                delay()
                inputField.send_keys(Keys.ENTER)
                delay()
                delay()

                err = driver.find_elements(By.CLASS_NAME, 'rc-audiochallenge-error-message')[0]
                if err.text == "" or err.value_of_css_property('display') == 'none':
                    print("[INFO] Success!")
                    driver.switch_to.default_content()
                    break

        except Exception as e:
            print(e)
            barkPush('[INFO] Possibly blocked by google. Change IP,Use Proxy method for requests')
            sys.exit("[INFO] Possibly blocked by google. Change IP,Use Proxy method for requests")
    else:
        # sys.exit("[INFO] Audio Play Button not found! In Very rare cases!")
        print('reCAPTCHA not found!')
    print('reCAPTCHA done')

def CAPTCHA():
    # 获取 captcha 图片链接
    number1 = int(driver.find_element(By.XPATH, '//*[@id="form-submit"]/div[2]/div[1]/img[1]').get_attribute('src').split('-')[1][0])
    caculateMethod = driver.find_element(By.XPATH, '//*[@id="form-submit"]/div[2]/div[1]').text[0]
    number2 = int(driver.find_element(By.XPATH, '//*[@id="form-submit"]/div[2]/div[1]/img[2]').get_attribute('src').split('-')[1][0])
    print('Method', caculateMethod)
    if caculateMethod == '+':
        captcha_result = number1 + number2
    elif caculateMethod == '-':
        captcha_result = number1 - number2
    elif caculateMethod == 'X':
        captcha_result = number1 * number2
    elif caculateMethod == '/':
        captcha_result = number1 / number2
    return captcha_result

def barkPush(body):
    if barkKey == 1:
        # bark push
        barkUrl = 'https://api.day.app/' + BARKKEY
        title = 'HaxExtend'
        requests.get(url=f'{barkUrl}/{title}/{body}?isArchive=1')
        print('bark push Done! Body:', body)
    elif barkKey == 0:
        print('No barkKey, Body is:', body)

def diffPlatformDriverPath():
    sysstr = platform.system()
    if sysstr == "Windows":
        path = os.getcwd()+"\\chromedriver.exe"
    elif sysstr == "Linux":
        path = os.getcwd()+"/chromedriver"
    else:
        path = os.getcwd()+"/chromedriver"
    print("path: ", path)
    return path


# def jumpCF():
#     flag = True
#
#     ##
#     # scraper = cloudscraper.create_scraper()  # returns a CloudScraper instance
#     # # Or: scraper = cloudscraper.CloudScraper()  # CloudScraper inherits from requests.Session
#     # sc = scraper.get(urlLogin)
#     # print(sc.text)  # => "<!DOCTYPE html><html><head>..."
#
#     try:
#         print("start jumpCF")
#         driver.find_elements(By.CLASS_NAME, "cf-browser-verification")[0]
#     except Exception as e:
#         print("Exception jumpCF")
#         flag = False
#     if flag is True:
#         print("while jumpCF")
#         # print(driver.find_elements(By.TAG_NAME, "body")[0].text)
#         time.sleep(10)
#         jumpCF()
#     else:
#         print("end jumpCF")


'''
    selenium.webdriver更换成undetected_chromedriver，从而跳过cloudflare ddos check
'''
def init():
    try:
        # show my public ip
        # ip = requests.get('https://checkip.amazonaws.com').text.strip()
        # print("[My Public IP]", ip)

        # create chrome driver
        # Options = webdriver.ChromeOptions()
        options = uc.ChromeOptions()
        # 浏览器不提供可视化界面
        # options.add_argument('--headless')
        # 隐私模式启动
        options.add_argument('--incognito')
        # options.add_argument('--disable-infobars')
        # options.add_argument('--no-sandbox')
        # options.add_argument('--disable-gpu')
        # options.add_argument('--disable-dev-shm-usage')

        # driver = webdriver.Chrome(executable_path=diffPlatformDriverPath(), options=Options)
        driver_chrome = uc.Chrome(version_main=105,options=options)
        # driver = uc.Chrome()
        delay()
        # go to website which have recaptcha protection
        driver_chrome.get(urlLogin)

        # all_es = driver.find_elements(By.XPATH, '//*')
        # print("[ALL_elements] ", all_es)

        # jumpCF()

        # print(driver.find_elements(By.TAG_NAME, "body")[0].text)
        return driver_chrome

    except Exception as e:
        print(e)
        # sys.exit("[-] Please update the chromedriver in the webdriver folder according to your chrome version:https://chromedriver.chromium.org/downloads")


# main
if __name__ == '__main__':
    driver = init()
    # WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframeCssSelector")))
    # driver.switch_to.default_content()
    time.sleep(20)
    print('fill username')
    driver.find_element(By.XPATH, '//*[@id="text"]').send_keys(USERNAME)
    print('fill password')
    driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(PASSWORD)
    delay()

    # reCAPTCHA
    print('do reCAPTCHA')
    reCAPTCHA()
    time.sleep(20)

    # login
    print('click login')
    driver.find_element(By.NAME, 'login').click()
    time.sleep(20)

    # Extend VPS link |
    # 此处click不知道为什么不跳转界面，所以导致报错：找不到web_address元素————————等待路过的大佬指点迷津！！
    # 所以click干脆换成driver.get(url)的方式了
    print('click Extend VPS')
    # WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.LINK_TEXT, 'Extend VPS Expiration'))).click()
    # driver.find_element(By.LINK_TEXT, 'Extend VPS').click()
    driver.get(urlExtendRenew)
    # print("URL: "+driver.current_url)
    # while "vps-renew" not in driver.current_url:
    #     print("URL: "+driver.current_url)
    #     time.sleep(5)
    time.sleep(20)
    driver.switch_to.default_content()

    # input web address
    print('fill web address')
    # print(driver.find_elements(By.TAG_NAME, "body")[0].text)
    driver.find_element(By.XPATH, '//*[@id="web_address"]').send_keys('hax.co.id')
    # captcha
    print('do CAPTCHA')
    driver.find_element(By.XPATH, '//*[@id="captcha"]').send_keys(CAPTCHA())
    # agreement check
    print('click agreement')
    driver.find_element(By.NAME, 'agreement').click()

    ## reCAPTCHA again
    # print('do reCAPTCHA')
    # reCAPTCHA()
    # time.sleep(10)

    # submit_button (Renew VPS)
    print('click Renew VPS')
    driver.find_element(By.NAME, 'submit_button').click()
    time.sleep(20)
    # driver.switch_to.default_content()

    print('copy text')
    # body = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="response"]/div'))).text
    body = driver.find_element(By.XPATH, '//*[@id="response"]/div').text
    # print('textBody:', body)
    delay()
    print('bark push')
    barkPush(body)
    delay()
    driver.quit()
