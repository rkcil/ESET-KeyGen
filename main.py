from selenium.webdriver import Chrome, ChromeOptions, ChromeService
from selenium.webdriver import Firefox, FirefoxOptions, FirefoxService
from selenium.webdriver import Edge, EdgeOptions, EdgeService

import subprocess
import traceback
import platform
import datetime
import argparse
import requests
import zipfile
import tarfile
import shutil
import random
import string

import email
import email.parser
from email import policy

import time
import sys
import os
import re

LOGO = """
███████╗███████╗███████╗████████╗   ██╗  ██╗███████╗██╗   ██╗ ██████╗ ███████╗███╗   ██╗
██╔════╝██╔════╝██╔════╝╚══██╔══╝   ██║ ██╔╝██╔════╝╚██╗ ██╔╝██╔════╝ ██╔════╝████╗  ██║
█████╗  ███████╗█████╗     ██║      █████╔╝ █████╗   ╚████╔╝ ██║  ███╗█████╗  ██╔██╗ ██║
██╔══╝  ╚════██║██╔══╝     ██║      ██╔═██╗ ██╔══╝    ╚██╔╝  ██║   ██║██╔══╝  ██║╚██╗██║   
███████╗███████║███████╗   ██║      ██║  ██╗███████╗   ██║   ╚██████╔╝███████╗██║ ╚████║   
╚══════╝╚══════╝╚══════╝   ╚═╝      ╚═╝  ╚═╝╚══════╝   ╚═╝    ╚═════╝ ╚══════╝╚═╝  ╚═══╝                                                                      
                                                Project Version: v1.4.7.1
                                                Project Devs: rzc0d3r, AdityaGarg8, k0re,
                                                              Fasjeit, alejanpa17, Ischunddu,
                                                              soladify, AngryBonk, Xoncia
"""
DEFAULT_MAX_ITER = 30
DEFAULT_DELAY = 1
GET_EBCN = 'document.getElementsByClassName'
GET_EBID = 'document.getElementById'
GET_EBTN = 'document.getElementByTagName'
GET_EBAV = 'getElementByAttrValue'
CLICK_WITH_BOOL = 'clickWithBool'
PARSE_10MINUTEMAIL_INBOX = 'parse_10minutemail_inbox()'
DEFINE_GET_EBAV_FUNCTION = """
function getElementByAttrValue(tagName, attrName, attrValue) {
    for (let element of document.getElementsByTagName(tagName)) {
        if(element.getAttribute(attrName) === attrValue)
            return element } }"""
DEFINE_CLICK_WITH_BOOL_FUNCTION = """
function clickWithBool(object) {
    try {
        object.click()
        return true }
    catch {
        return false } }"""
DEFINE_PARSE_10MINUTEMAIL_INBOX_FUNCTION = """function parse_10minutemail_inbox() {
    updatemailbox()
    let mails = Array.from(document.getElementsByTagName('tr')).slice(1)
    let inbox = []
    for(let i=0; i < mails.length; i++) {
        let id = mails[i].children[0].children[0].href
        let from = mails[i].children[0].innerText
        let subject = mails[i].children[1].innerText
        inbox.push([id, from, subject]) }
    return inbox }"""
PARSE_GUERRILLAMAIL_INBOX = """
var email_list = document.getElementById('email_list').children
var inbox = []
for(var i=0; i < email_list.length-1; i++) {
    var mail = email_list[i].children
    var from = mail[1].innerText
    var subject = mail[2].innerText
    var mail_id = mail[0].children[0].value
    inbox.push([mail_id, from, subject])
}
return inbox
"""
GET_GUERRILLAMAIL_DOMAINS = """
var domains_options = document.getElementById('gm-host-select').options
var domains = [] 
for(var i=0; i < domains_options.length-1; i++) {
    domains.push(domains_options[i].value)
}
return domains
"""

from colorama import Fore, Style, init

init()

class LoggerType:
    def __init__(self, sborder, eborder, title, color, fill_text):
        self.sborder = sborder
        self.eborder = eborder
        self.title = title
        self.color = color
        self.fill_text = fill_text

    @property
    def data(self):
        return self.sborder + self.color + self.title + Style.RESET_ALL + self.eborder

ERROR = LoggerType('[ ', ' ]', 'FAILED', Fore.RED, True)
OK = LoggerType('[   ', '   ]', 'OK', Fore.GREEN, False)
INFO = LoggerType('[  ', '  ]', 'INFO', Fore.LIGHTBLACK_EX, True)
DEVINFO = LoggerType('[ ', ' ]', 'DEBUG', Fore.CYAN, True)

def console_log(text='', logger_type=None, fill_text=None):
    if isinstance(logger_type, LoggerType):
        ni = 0
        for i in range(0, len(text)):
            if text[i] != '\n':
                ni = i
                break
            print()
        if logger_type.fill_text and fill_text is None:
            fill_text = True
        if logger_type.fill_text and fill_text:
            print(logger_type.data + ' ' + logger_type.color + text[ni:] + Style.RESET_ALL)
        else:
            print(logger_type.data + ' ' + text[ni:])
    else:
        print(text)

class SecEmailAPI(object):
    def __init__(self):
        self.__login = None
        self.__domain = None
        self.email = None
        self.__api = 'https://www.1secmail.com/api/v1/'
        
    def init(self):
        url = f'{self.__api}?action=genRandomMailbox&count=1'
        try:
            r = requests.get(url)
        except:
            raise RuntimeError('SecEmailAPI: API access error!')
        if r.status_code != 200:
            raise RuntimeError('SecEmailAPI: API access error!')
        self.__login, self.__domain = str(r.content, 'utf-8')[2:-2].split('@')
        self.email = self.__login+'@'+self.__domain
    
    def login(self, login, domain):
        self.__login = login
        self.__domain = domain
    
    def read_email(self):
        url = f'{self.__api}?action=getMessages&login={self.__login}&domain={self.__domain}'
        try:
            r = requests.get(url)
        except:
            raise RuntimeError('SecEmailAPI: API access error!')
        if r.status_code != 200:
            raise RuntimeError('SecEmailAPI: API access error!')
        return r.json()
    
    def get_message(self, message_id):
        url = f'{self.__api}?action=readMessage&login={self.__login}&domain={self.__domain}&id={message_id}'
        try:
            r = requests.get(url)
        except:
            raise RuntimeError('SecEmailAPI: API access error!')
        if r.status_code != 200:
            raise RuntimeError('SecEmailAPI: API access error!')
        return r.json()

class DeveloperMailAPI(object):
    def __init__(self):
        self.email = ''
        self.email_name = ''
        self.headers = {}
        self.api_url = 'https://www.developermail.com/api/v1'
    
    def init(self):
        r = requests.put(f'{self.api_url}/mailbox')
        self.email_name, token = list(r.json()['result'].values())
        self.email = self.email_name+'@developermail.com'
        self.headers = {'X-MailboxToken': token}

    def __parse_message(self, raw_message_body):
        message_bytes = raw_message_body.encode('utf-8')
        msg = email.parser.BytesParser(policy=policy.default).parsebytes(message_bytes)
        message_subject = msg['subject']
        message_from = msg['from']
        message_body = str(msg.get_payload(decode=True).decode(msg.get_content_charset())) # decoding MIME-Type to html
        return {'subject':message_subject, 'from':message_from, 'body':message_body}

    def get_messages(self):
        # get message IDs
        r = requests.get(
            f'{self.api_url}/mailbox/{self.email_name}',
            headers=self.headers
        )
        message_ids = r.json()['result']
        if message_ids == []:
            return None
        # parse messages
        messages = []
        for message_id in message_ids:
            r = requests.get(f'{self.api_url}/mailbox/{self.email_name}/messages/{message_id}', headers=self.headers)
            raw_message_body = r.json()['result']
            messages.append(self.__parse_message(raw_message_body))
        if messages == []:
            messages = None
        return messages

class Hi2inAPI(object):
    def __init__(self, driver: Chrome):
        self.driver = driver
        self.email = None
        self.window_handle = None
    
    def init(self):
        #self.driver.execute_script('window.open("https://hi2.in/#/", "_blank")')
        #if args['try_auto_cloudflare']:
        #    console_log(f'Attempting to pass cloudflare captcha automatically...', INFO)
        #    time.sleep(8)
        #else:
        #    console_log(f'{Fore.CYAN}Solve the cloudflare captcha on the page manually!!!{Fore.RESET}', INFO, False)
        #    input(f'[  {Fore.YELLOW}INPT{Fore.RESET}  ] {Fore.CYAN}Press Enter when you see the hi2in page...{Fore.RESET}')
        #self.driver.switch_to.window(self.driver.window_handles[0])
        #self.driver.close()
        #self.driver.switch_to.window(self.driver.window_handles[0])
        self.driver.get("https://hi2.in/#/")
        self.window_handle = self.driver.current_window_handle
        #if args['try_auto_cloudflare']:
        #    try:
        #        self.driver.execute_script(f'{GET_EBCN}("mailtext mailtextfix")[0]')
        #        console_log('Successfully passed сloudflare captcha in automatic mode!!!', OK)
        #    except:
        #        console_log('Failed to pass сloudflare captcha in automatic mode!!!', ERROR)
        #        time.sleep(3) # exit-delay
        #        sys.exit(-1)
        SharedTools.untilConditionExecute(
            self.driver,
            f'return ({GET_EBCN}("mailtext mailtextfix")[0] !== null && {GET_EBCN}("mailtext mailtextfix")[0].value !== "")'
        )
        self.email = self.driver.execute_script(f'return {GET_EBCN}("mailtext mailtextfix")[0].value')
        # change domain to @telegmail.com
        if self.email.find('@telegmail.com') == -1:
            while True:
                self.email = self.driver.execute_script(f'return {GET_EBCN}("mailtext mailtextfix")[0].value')
                if self.email.find('@telegmail.com') != -1:
                    break
                self.driver.execute_script(f"{GET_EBCN}('genbutton')[0].click()")
                time.sleep(1.5)
    
    def open_inbox(self):
        self.driver.switch_to.window(self.window_handle)

class TenMinuteMailAPI(object):
    def __init__(self, driver: Chrome):
        self.driver = driver
        self.email = None
        self.window_handle = None
    
    def init(self):     
        self.driver.get('https://10minutemail.net/new.html?lang=en')
        self.window_handle = self.driver.current_window_handle
        SharedTools.untilConditionExecute(self.driver, f'return {GET_EBID}("fe_text") != null')
        self.email = self.driver.execute_script(f'return {GET_EBID}("fe_text").value')
    
    def parse_inbox(self):
        self.driver.switch_to.window(self.window_handle)
        self.driver.get('https://10minutemail.net/?lang=en')
        inbox = self.driver.execute_script('\n'.join([DEFINE_PARSE_10MINUTEMAIL_INBOX_FUNCTION, 'return '+PARSE_10MINUTEMAIL_INBOX]))
        return inbox

    def open_mail(self, id):
        self.driver.switch_to.window(self.window_handle)
        self.driver.get(id)

class GuerRillaMailAPI(object):
    def __init__(self, driver: Chrome):
        self.driver = driver
        self.email = None
        self.window_handle = None

    def init(self):     
        self.driver.get('https://www.guerrillamail.com/')
        self.window_handle = self.driver.current_window_handle
        SharedTools.untilConditionExecute(self.driver, f'return {GET_EBID}("email-widget") != null')
        self.email = self.driver.execute_script(f'return {GET_EBID}("email-widget").innerText')
        # change to random available domain
        self.email = self.email.split('@')[0]+'@'+random.choice(self.driver.execute_script(GET_GUERRILLAMAIL_DOMAINS))
    
    def parse_inbox(self):
        self.driver.switch_to.window(self.window_handle)
        self.driver.get('https://www.guerrillamail.com/')
        inbox = self.driver.execute_script(PARSE_GUERRILLAMAIL_INBOX)
        return inbox

    def open_mail(self, id):
        self.driver.switch_to.window(self.window_handle)
        self.driver.get(f'https://www.guerrillamail.com/inbox?mail_id={id}')

class TempMailAPI(object):
    def __init__(self, driver=None):
        self.driver = driver
        self.token = ""
        self.email = ""
        self.window_handle = None

    def init(self):
        self.driver.execute_script('window.open("https://temp-mail.org", "_blank")')
        if args['try_auto_cloudflare']:
            console_log(f'Attempting to pass cloudflare captcha automatically...', INFO)
            time.sleep(8)
        else:
            console_log(f'{Fore.CYAN}Solve the cloudflare captcha on the page manually!!!{Fore.RESET}', INFO, False)
            input(f'[  {Fore.YELLOW}INPT{Fore.RESET}  ] {Fore.CYAN}Press Enter when you see the TempMail page...{Fore.RESET}')
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.window_handle = self.driver.current_window_handle
        if args['try_auto_cloudflare']:
            try:
                self.driver.execute_script(f"return {GET_EBID}('mail').value")
                console_log('Successfully passed сloudflare captcha in automatic mode!!!', OK)
            except:
                console_log('Failed to pass сloudflare captcha in automatic mode!!!', ERROR)
                time.sleep(3) # exit-delay
                sys.exit(-1)
        for _ in range(DEFAULT_MAX_ITER):
            self.email = self.driver.execute_script(f"return {GET_EBID}('mail').value")
            if self.email == '':
                raise RuntimeError('TempMailAPI: Your IP is blocked, try again later or try use VPN!')
            elif self.email.find('@') != -1:
                break
            time.sleep(DEFAULT_DELAY)
    
    def auth(self):
        if self.token != "":
            return True
        self.driver.switch_to.window(self.window_handle)
        for _ in range(DEFAULT_MAX_ITER):
            try:
                self.token = self.driver.get_cookie('token')['value']
                return True
            except:
                time.sleep(1)
        raise RuntimeError('TempMailAPI: Error during authorization!')

    def get_messages(self):
        try:
            self.driver.switch_to.window(self.window_handle)
            return self.driver.execute_script(f"""
                var req = new XMLHttpRequest()
                req.open("GET", "https://web2.temp-mail.org/messages", false)
                req.setRequestHeader("Authorization", "Bearer {self.token}")
                req.send(null)
                return JSON.parse(req.response)
            """)["messages"]
        except Exception as E:
            return None

    def get_message(self, message_id):
        try:
            self.driver.switch_to.window(self.window_handle)
            return self.driver.execute_script(f"""
                var req = new XMLHttpRequest()
                req.open("GET", "https://web2.temp-mail.org/messages/{message_id}", false)
                req.setRequestHeader("Authorization", "Bearer {self.token}")
                req.send(null)
                return JSON.parse(req.response)
            """)
        except:
            return None

class CustomEmailAPI(object):
    def __init__(self):
        self.email = None

class SharedTools(object):
    def untilConditionExecute(driver_obj, js: str, delay=DEFAULT_DELAY, max_iter=DEFAULT_MAX_ITER, positive_result=True, raise_exception_if_failed=True, return_js_result=False):
        driver_obj.execute_script(f'window.{GET_EBAV} = {DEFINE_GET_EBAV_FUNCTION}')
        driver_obj.execute_script(f'window.{CLICK_WITH_BOOL} = {DEFINE_CLICK_WITH_BOOL_FUNCTION}')
        pre_js = [
            DEFINE_GET_EBAV_FUNCTION,
            DEFINE_CLICK_WITH_BOOL_FUNCTION
        ]
        js = '\n'.join(pre_js+[js])
        for _ in range(max_iter):
            try:
                result = driver_obj.execute_script(js)
                if return_js_result and result is not None:
                    return result
                elif result == positive_result:
                    return True
            except Exception as E:
                pass
            time.sleep(delay)
        if raise_exception_if_failed:
            raise RuntimeError('untilConditionExecute: the code did not return the desired value! TRY VPN!')

    def createPassword(length, only_numbers=False):
        if only_numbers:
            return [random.choice(string.digits) for _ in range(length)]
        return ''.join(['Xx0$']+[random.choice(string.ascii_letters) for _ in range(length)])

    def initSeleniumWebDriver(browser_name: str, webdriver_path = None, browser_path = '', headless=True):
        if os.name == 'posix': # For Linux
            if sys.platform.startswith('linux'):
                console_log(f'Initializing {browser_name}-webdriver for Linux', INFO)
            elif sys.platform == "darwin":
                console_log(f'Initializing {browser_name}-webdriver for macOS', INFO)
        elif os.name == 'nt':
            console_log(f'Initializing {browser_name}-webdriver for Windows', INFO)
        driver_options = None
        driver = None
        if browser_name.lower() == 'chrome':
            driver_options = ChromeOptions()
            driver_options.binary_location = browser_path
            driver_options.add_experimental_option('excludeSwitches', ['enable-logging'])
            driver_options.add_argument("--log-level=3")
            driver_options.add_argument("--lang=en-US")
            if headless:
                driver_options.add_argument('--headless')
            if os.name == 'posix': # For Linux
                driver_options.add_argument('--no-sandbox')
                driver_options.add_argument('--disable-dev-shm-usage')
            try:
                driver = Chrome(options=driver_options, service=ChromeService(executable_path=webdriver_path))
            except Exception as E:
                if traceback.format_exc().find('only supports') != -1: # Fix for downloaded chrome update
                    console_log('Downloaded Google Chrome update is detected! Using new chrome executable file!', INFO)
                    browser_path = traceback.format_exc().split('path')[-1].split('Stacktrace')[0].strip()
                    if 'new_chrome.exe' in os.listdir(browser_path[:-10]):
                        browser_path = browser_path[:-10]+'new_chrome.exe'
                        driver_options.binary_location = browser_path
                        driver = Chrome(options=driver_options, service=ChromeService(executable_path=webdriver_path))
                else:
                  raise E
        elif browser_name.lower() == 'firefox':
            driver_options = FirefoxOptions()
            driver_options.binary_location = browser_path
            driver_options.set_preference('intl.accept_languages', 'en-US')
            if headless:
                driver_options.add_argument('--headless')
            if os.name == 'posix': # For Linux
                driver_options.add_argument('--no-sandbox')
                driver_options.add_argument("--disable-dev-shm-usage")
            driver = Firefox(options=driver_options, service=FirefoxService(executable_path=webdriver_path))
        elif browser_name.lower() == 'edge':
            driver_options = EdgeOptions()
            driver_options.use_chromium = True
            driver_options.binary_location = browser_path
            driver_options.add_experimental_option('excludeSwitches', ['enable-logging'])
            driver_options.add_argument("--log-level=3")
            driver_options.add_argument("--lang=en-US")
            if headless:
                driver_options.add_argument('--headless')
            if os.name == 'posix': # For Linux
                driver_options.add_argument('--no-sandbox')
                driver_options.add_argument('--disable-dev-shm-usage')
            driver = Edge(options=driver_options, service=EdgeService(executable_path=webdriver_path))
        #driver.set_window_position(0, 0)
        #driver.set_window_size(640, 640)
        return driver

    def parseToken(email_obj, driver=None, eset_business=False, delay=DEFAULT_DELAY, max_iter=DEFAULT_MAX_ITER):
        activated_href = None
        if args['custom_email_api']:
            while True:
                activated_href = input(f'\n[  {Fore.YELLOW}INPT{Fore.RESET}  ] {Fore.CYAN}Enter the link to activate your account, it will come to the email address you provide: {Fore.RESET}').strip()
                if activated_href is not None:
                    match = re.search(r'token=[a-zA-Z\d:/-]*', activated_href)
                    if match is not None:
                        token = match.group()[6:]
                        if len(token) == 36:
                            return token
                console_log('Incorrect link syntax', ERROR)
        for _ in range(max_iter):
            if args['email_api'] == '1secmail':
                json = email_obj.read_email()
                if json != []:
                    message = json[-1]
                    if eset_business and message['subject'].find('activation') != -1:
                        activated_href = email_obj.get_message(message['id'])['body']
                    elif message['from'].find('product.eset.com') != -1:
                        activated_href = email_obj.get_message(message['id'])['body']
            elif args['email_api'] == 'developermail':
                messages = email_obj.get_messages()
                if messages is not None:
                    message = messages[-1]
                    if eset_business and message['subject'].find('activation') != -1:
                        activated_href = message['body']
                    elif message['from'].find('product.eset.com') != -1:
                        activated_href = message['body']
            elif args['email_api'] == 'hi2in':
                email_obj.open_inbox()
                try:
                    if eset_business:
                        activated_href = driver.find_element('xpath', "//a[starts-with(@href, 'https://eba.eset.com')]").get_attribute('href')
                    else:
                        activated_href = driver.find_element('xpath', "//a[starts-with(@href, 'https://login.eset.com')]").get_attribute('href')
                except:
                    pass
            elif args['email_api'] in ['10minutemail', 'guerrillamail']:
                inbox = email_obj.parse_inbox()
                for mail in inbox:
                    mail_id, mail_from, mail_subject = mail
                    if mail_from.find('product.eset.com') != -1 or mail_subject.find('activation') != -1:
                        email_obj.open_mail(mail_id)
                        try:
                            if eset_business:
                                activated_href = driver.find_element('xpath', "//a[starts-with(@href, 'https://eba.eset.com')]").get_attribute('href') 
                            else:
                                activated_href = driver.find_element('xpath', "//a[starts-with(@href, 'https://login.eset.com')]").get_attribute('href')
                        except:
                            pass
            elif args['email_api'] == 'tempmail':
                email_obj.auth()
                messages = email_obj.get_messages()
                try:
                    for message in messages:
                        if message["from"].find("product.eset.com") != -1 or message["subject"].find("activation") != -1:
                            activated_href = email_obj.get_message(message["_id"])["bodyHtml"]
                except:
                    pass
            if activated_href is not None:
                match = re.search(r'token=[a-zA-Z\d:/-]*', activated_href)
                if match is not None:
                    token = match.group()[6:]
                    return token
            time.sleep(delay)
        raise RuntimeError('Token retrieval error!!!')

class WebDriverInstaller(object):
    def __init__(self, for_firefox=False):
        self.platform = ['', []] # [OC name, [webdriver architectures]]
        if sys.platform.startswith('win'):
            self.platform[0] = 'win'
            if sys.maxsize > 2**32:
                self.platform[1] = ['win64', 'win32']
            else:
                self.platform[1] = ['win32']
        elif sys.platform.startswith('linux'):
            self.platform[0] = 'linux'
            if sys.maxsize > 2**32:
                self.platform[1].append('linux64')
            else:
                self.platform[1].append('linux32')
        elif sys.platform == "darwin":
            self.platform[0] = 'mac'
            if for_firefox:
                self.platform[1] = ['macos']
            elif platform.processor() == "arm":
                self.platform[1] = ['mac-arm64', 'mac_arm64', 'mac64_m1']
            elif platform.processor() == "i386":
                self.platform[1] = ['mac64', 'mac-x64']
        if self.platform[0] == '' or self.platform[1] == []:
            raise RuntimeError('WebDriverInstaller: impossible to define the system!')
    
    def get_chrome_version(self):
        if self.platform[0] == "linux":
            path = None
            for executable in ("google-chrome", "google-chrome-stable", "google-chrome-beta", "google-chrome-dev", "chromium-browser", "chromium"):
                path = shutil.which(executable)
                if path is not None:
                    with subprocess.Popen([path, "--version"], stdout=subprocess.PIPE) as proc:
                        chrome_version = proc.stdout.read().decode("utf-8").replace("Chromium", "").replace("Google Chrome", "").strip().split()[0]
        elif self.platform[0] == "mac":
            process = subprocess.Popen(["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "--version"], stdout=subprocess.PIPE)
            chrome_version = process.communicate()[0].decode("UTF-8").replace("Google Chrome", "").strip()
        elif self.platform[0] == "win":
            paths = [
                "C:\\Program Files\\Google\\Chrome\\Application\\",
                "C:\\Program Files (x86)\\Google\\Chrome\\Application\\",
                os.environ.get('LOCALAPPDATA')+"\\Google\\Chrome\\Application\\"
            ]
            for path in paths:
                try:
                    with open(path+'chrome.VisualElementsManifest.xml', 'r') as f:
                        for line in f.readlines():
                            line = line.strip()
                            if line.startswith('Square150x150Logo'):
                                chrome_version = line.split('=')[1].split('\\')[0][1:] 
                                break
                except:
                    pass
        if chrome_version is not None:
            chrome_version = [chrome_version]+chrome_version.split('.') # [full, major, _, minor, micro]
        else:
            raise RuntimeError('WebDriverInstaller: Google Chrome is not detected installed on your device!')
        return chrome_version

    def get_chromedriver_download_url(self, chrome_major_version=None):
        if chrome_major_version is None:
            chrome_major_version = self.get_chrome_version()[1]
        if int(chrome_major_version) >= 115: # for new drivers ( [115.0.0000.0, ...] )
            drivers_data = requests.get('https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json')
            drivers_data = drivers_data.json()['versions'][::-1] # start with the latest version
            for driver_data in drivers_data:
                driver_version = driver_data['version']
                driver_major_version = driver_version.split('.')[0] # major, _, minor, micro
                if driver_major_version == chrome_major_version: # return latest driver version for current major chrome version
                    for driver_url in driver_data['downloads'].get('chromedriver', None):
                            if driver_url['platform'] in self.platform[1]:
                                return driver_url['url']
        else: # for old drivers ( [..., 115.0.0000.0) )
            latest_old_driver_version = requests.get('https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{0}'.format(chrome_major_version))
            if latest_old_driver_version.status_code != 200:
                raise RuntimeError('WebDriverInstaller: the required chrome-webdriver was not found!')
            latest_old_driver_version = latest_old_driver_version.text
            driver_url = 'https://chromedriver.storage.googleapis.com/{0}/chromedriver_'.format(latest_old_driver_version)
            for arch in self.platform[1]:
                current_driver_url = driver_url+arch+'.zip'
                driver_size = requests.head(current_driver_url).headers.get('x-goog-stored-content-length', None)
                if driver_size is not None and int(driver_size) > 1024**2:
                    return current_driver_url
            raise RuntimeError('WebDriverInstaller: the required chrome-webdriver was not found!')
    
    def get_latest_geckodriver_download_url(self, only_version=False):
        r = requests.get("https://api.github.com/repos/mozilla/geckodriver/releases/latest")
        r_json = r.json()
        # note for: r_json['assets'][::-1]
        # in the initialization of WebDriverInstaller for 64bit is also suitable for 32bit, but
        # in the list of assets first go 32bit and it comes out that for 64bit gives a 32bit release, turning the list fixes it
        if only_version:
            return r_json['name']
        for asset in r_json['assets'][::-1]:
            if asset['name'].find('asc') == -1: # ignoring GPG Keys
                asset_arch = asset['name'].split('-', 2)[-1].split('.')[0] # package architecture parsing; geckodriver-v0.34.0-win32.zip -> ['geckodriver', 'v0.34.0', 'win32.zip'] -> ['win32', 'zip'] -> win32
                if asset_arch in self.platform[1]:
                    return asset['browser_download_url']

    def download_webdriver(self, path='.', url=None, edge=False, firefox=False):
        file_extension = '.zip'
        if url is None:
            if edge:
                url = self.get_edgedriver_download_url()
            elif firefox:
                url = self.get_latest_geckodriver_download_url()
            else:
                url = self.get_chromedriver_download_url()
        if url.find('.tar.gz') != -1:
            file_extension = '.tar.gz'
        # downloading
        zip_path = path.replace('\\', '/')+'/data'+file_extension
        f = open(zip_path, 'wb')
        f.write(requests.get(url).content)
        f.close()
        if edge:
            webdriver_name = 'msedgedriver' # macOS, linux
        elif firefox:
            webdriver_name = 'geckodriver' # macOS, linux
        else:
            webdriver_name = 'chromedriver' # macOS, linux
        if self.platform[0].startswith('win'): # windows
            webdriver_name += '.exe'
        # extracting
        if file_extension == '.zip':
            with zipfile.ZipFile(zip_path, 'r') as zip:
                webdriver_zip_path = ''
                if not edge and not firefox: # Google Chrome
                    if len(zip.namelist()[0].split('/')) > 1: # for new Google Chrome webdriver zip format 
                        webdriver_zip_path = zip.namelist()[0].split('/')[0]+'/'
                with open(path+'/'+webdriver_name, 'wb') as f: # for Google Chrome and Microsoft Edge
                    f.write(zip.read(webdriver_zip_path+webdriver_name))
        elif file_extension == '.tar.gz':
            tar = tarfile.open(zip_path)
            tar.extractall()
            tar.close()
        try:
            os.remove(zip_path)
        except:
            pass
        return True
    
    def get_edge_version(self): # Only for windows
        edge_version = None
        paths = [
            'C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe',
            'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe'
        ]
        for path in paths:
            if not os.path.exists(path):
                continue
            f = open(path, 'rb')
            for line in f.readlines()[::-1]:
                if line.find(b'" version="') != -1:
                    # <assemblyIdentity type="win32" name="124.0.2478.80" version="124.0.2478.80" language="*"/> ->
                    # ['<assemblyIdentity type="win32" name="124.0.2478.80" version', '="124.0.2478.80" language="*"/>'] ->
                    # ="124.0.2478.80" language="*"/> -> ['="', '124.0.2478.80', '" language="*"/>']
                    # 124.0.2478.80
                    edge_version = str(line).split('version')[-1].split('"')[1]
                    edge_version = [edge_version]+edge_version.split('.')
                    break
            f.close()
        if edge_version is None:
            raise RuntimeError('WebDriverInstaller: Microsoft Edge is not detected installed on your device!')
        return edge_version

    def get_edgedriver_download_url(self, edge_version=None):
        archs = self.platform[1]
        if edge_version is None:
            edge_version = self.get_edge_version()
        driver_url = 'https://msedgedriver.azureedge.net/{0}/edgedriver_'.format(edge_version[0])
        if requests.head(driver_url+'win32.zip').status_code != 200:
            console_log('Webdriver with identical version as the browser is not detected!!!', ERROR)
            console_log('Script runs an advanced search for a suitable webdriver...', INFO)
            for i in range(0, 150):
                tmp_edge_version = edge_version
                tmp_edge_version[-1] = str(i)
                tmp_edge_version = '.'.join(tmp_edge_version[1:])
                if requests.head(f'https://msedgedriver.azureedge.net/{tmp_edge_version}/edgedriver_win32.zip').status_code == 200:
                    # console_log('Another suitable version has been found!', OK)
                    driver_url = 'https://msedgedriver.azureedge.net/{0}/edgedriver_'.format(tmp_edge_version)
                    break
        for arch in archs:
            current_driver_url = driver_url+arch+'.zip'
            driver_size = requests.head(current_driver_url).headers.get('Content-Length', None)
            if driver_size is not None and int(driver_size) > 1024**2:
                return current_driver_url
        raise RuntimeError('WebDriverInstaller: the required edge-webdriver was not found!')
            
    def webdriver_installer_menu(self, edge=False, firefox=False): # auto updating or installing webdrivers
        if edge:
            browser_name = 'Microsoft Edge'
        elif firefox:
            browser_name = 'Mozilla Firefox'
        else:
            browser_name = 'Google Chrome'
        console_log('-- WebDriver Auto-Installer --\n'.format(browser_name))
        if edge:
            browser_version = self.get_edge_version()
        elif firefox:
            browser_version = ['Ignored', 'Ignored']
        else:
            browser_version = self.get_chrome_version()
        current_webdriver_version = None
        if edge:
            webdriver_name = 'msedgedriver'
        elif firefox:
            webdriver_name = 'geckodriver'
        else:
            webdriver_name = 'chromedriver'
        if self.platform[0] == 'win':
            webdriver_name += '.exe'
        webdriver_path = None
        if os.path.exists(webdriver_name):
            os.chmod(webdriver_name, 0o777)
            out = subprocess.check_output([os.path.join(os.getcwd(), webdriver_name), "--version"], stderr=subprocess.PIPE)
            if out is not None:
                if edge:
                    current_webdriver_version = out.decode("utf-8").split(' ')[3]
                else: 
                    current_webdriver_version = out.decode("utf-8").split(' ')[1]
        console_log('{0} version: {1}'.format(browser_name, browser_version[0]), INFO, False)
        console_log('{0} webdriver version: {1}'.format(browser_name, current_webdriver_version), INFO, False)
        if firefox:
            latest_geckodriver_version = self.get_latest_geckodriver_download_url(True)
            if current_webdriver_version == latest_geckodriver_version:
                console_log('The webdriver has already been updated to the latest version!\n', OK)
                return os.path.join(os.getcwd(), webdriver_name)
            elif current_webdriver_version is not None:
                console_log(f'Updating the webdriver from {current_webdriver_version} to {latest_geckodriver_version} version...', INFO)
        if current_webdriver_version is None:
            console_log('{0} webdriver not detected, download attempt...'.format(browser_name), INFO)
        elif current_webdriver_version.split('.')[0] != browser_version[1] and not firefox: # major version match
            console_log('{0} webdriver version doesn\'t match version of the installed {1}, trying to update...'.format(browser_name, browser_name), ERROR)
        if (current_webdriver_version is None or current_webdriver_version.split('.')[0] != browser_version[1]) or firefox:
            if edge:
                driver_url = self.get_edgedriver_download_url()
            elif firefox:
                driver_url = self.get_latest_geckodriver_download_url()
            else:
                driver_url = self.get_chromedriver_download_url()
            if driver_url is not None:
                console_log('\nFound a suitable version for your system!', OK)
                console_log('Downloading...', INFO)
                if self.download_webdriver('.', driver_url, edge, firefox):
                    console_log('{0} webdriver was successfully downloaded and unzipped!\n'.format(browser_name), OK)
                    webdriver_path = os.path.join(os.getcwd(), webdriver_name)
                else:
                    console_log('Error downloading or unpacking!\n', ERROR)
        else:
            console_log('The webdriver has already been updated to the browser version!\n', OK)
            webdriver_path = os.path.join(os.getcwd(), webdriver_name)
        return webdriver_path

class EsetRegister(object):
    def __init__(self, registered_email_obj: SecEmailAPI, eset_password: str, driver: Chrome):
        self.email_obj = registered_email_obj
        self.eset_password = eset_password
        self.driver = driver
        self.window_handle = None

    def createAccount(self):
        exec_js = self.driver.execute_script
        uCE = SharedTools.untilConditionExecute

        console_log('\n[EMAIL] Register page loading...', INFO)
        if args['email_api'] in ['hi2in', '10minutemail', 'tempmail', 'guerrillamail']:
            self.driver.switch_to.new_window('EsetRegister')
            self.window_handle = self.driver.current_window_handle
        self.driver.get('https://login.eset.com/Register')
        uCE(self.driver, f"return {GET_EBID}('email') != null")
        console_log('[EMAIL] Register page is loaded!', OK)

        console_log('\nBypassing cookies...', INFO)
        if uCE(self.driver, f"return {CLICK_WITH_BOOL}({GET_EBAV}('button', 'id', 'cc-accept'))", max_iter=10, raise_exception_if_failed=False):
            console_log('Cookies successfully bypassed!', OK)
            time.sleep(1.5) # Once pressed, you have to wait a little while. If code do not do this, the site does not count the acceptance of cookies
        else:
            console_log("Cookies were not bypassed (it doesn't affect the algorithm, I think :D)", ERROR)

        exec_js(f"return {GET_EBID}('email')").send_keys(self.email_obj.email)
        uCE(self.driver, f"return {CLICK_WITH_BOOL}({DEFINE_GET_EBAV_FUNCTION}('button', 'data-label', 'register-continue-button'))")

        console_log('\n[PASSWD] Register page loading...', INFO)
        uCE(self.driver, f"return typeof {GET_EBAV}('button', 'data-label', 'register-create-account-button') === 'object'")
        console_log('[PASSWD] Register page is loaded!', OK)
        exec_js(f"return {GET_EBID}('password')").send_keys(self.eset_password)
        # Select Ukraine country
        if exec_js(f"return {GET_EBCN}('select__single-value ltr-1dimb5e-singleValue')[0]").text != 'Ukraine':
            exec_js(f"return {GET_EBID}('country-select-control')").click()
            for country in exec_js(f"return {GET_EBCN}('select__option ltr-gaqfzi-option')"):
                if country.text == 'Ukraine':
                    country.click()
                    break
        uCE(self.driver, f"return {CLICK_WITH_BOOL}({DEFINE_GET_EBAV_FUNCTION}('button', 'data-label', 'register-create-account-button'))")

        for _ in range(DEFAULT_MAX_ITER):
            title = exec_js('return document.title')
            if title == 'Service not available':
                raise RuntimeError('\nESET temporarily blocked your IP, try again later!!! TRY VPN!!!')
            url = exec_js('return document.URL')
            if url == 'https://home.eset.com/':
                return True
            time.sleep(DEFAULT_DELAY)
        raise RuntimeError('\nESET temporarily blocked your IP, try again later!!! TRY VPN!!!')

    def confirmAccount(self):
        uCE = SharedTools.untilConditionExecute
        #uCE(self.driver, f'return {CLICK_WITH_BOOL}({GET_EBAV}("ion-button", "data-r", "account-verification-email-modal-resend-email-btn"))') # accelerating the receipt of an eset token
        
        if args['custom_email_api']:
            token = SharedTools.parseToken(self.email_obj, max_iter=100, delay=3)
        else:
            console_log(f'\n[{args["email_api"]}] ESET-Token interception...', INFO)
            if args['email_api'] in ['hi2in', '10minutemail', 'tempmail', 'guerrillamail']:
                token = SharedTools.parseToken(self.email_obj, self.driver, max_iter=100, delay=3)
                self.driver.switch_to.window(self.window_handle)
            else:
                token = SharedTools.parseToken(self.email_obj, max_iter=100, delay=3) # 1secmail, developermail
        console_log(f'ESET-Token: {token}', OK)
        console_log('\nAccount confirmation is in progress...', INFO)
        self.driver.get(f'https://login.eset.com/link/confirmregistration?token={token}')
        uCE(self.driver, 'return document.title === "ESET HOME"')
        uCE(self.driver, f'return {GET_EBCN}("verification-email_p").length === 0')
        console_log('Account successfully confirmed!', OK)
        return True

    def returnDriver(self):
        return self.driver

class EsetKeygen(object):
    def __init__(self, registered_email_obj: SecEmailAPI, driver: Chrome):
        self.email_obj = registered_email_obj
        self.driver = driver

    def sendRequestForKey(self):
        exec_js = self.driver.execute_script
        uCE = SharedTools.untilConditionExecute
        
        console_log('\nRequest sending...', INFO)
        self.driver.get('https://home.eset.com/subscriptions')
        uCE(self.driver, f"return {CLICK_WITH_BOOL}({GET_EBAV}('button', 'data-label', 'licenseAssociateHeaderAddNewBtn'))") # V2
        
        console_log('Waiting for permission to request...', INFO)
        uCE(self.driver, f"return {CLICK_WITH_BOOL}({GET_EBAV}('button', 'data-label', 'license-fork-slide-trial-license-card-button'))")
        console_log('Access to the request was open!', OK)
        try:
            uCE(self.driver, f"return {CLICK_WITH_BOOL}({GET_EBAV}('ion-button', 'robot', 'license-fork-slide-continue-button'))")
        except:
            raise RuntimeError('Access to the request is denied, try again later!')
        console_log('\nPlatforms loading...', INFO)
        uCE(self.driver, f"return {CLICK_WITH_BOOL}({GET_EBAV}('button', 'data-label', 'device-protect-os-card-Windows-button'))")
        console_log('Windows platform is selected!', OK)
        uCE(self.driver, f"return {CLICK_WITH_BOOL}({GET_EBAV}('ion-button', 'robot', 'device-protect-choose-platform-continue-btn'))")

        console_log('\nSending a request for a license...', INFO)
        uCE(self.driver, f"return typeof {GET_EBAV}('ion-input', 'robot', 'device-protect-get-installer-email-input') === 'object'")
        exec_js(f"{GET_EBAV}('ion-input', 'robot', 'device-protect-get-installer-email-input').value = '{self.email_obj.email}'")
        exec_js(f"{GET_EBAV}('ion-button', 'robot', 'device-protect-get-installer-send-email-btn').click()")
        console_log('Request successfully sent!', OK)

    def getLicenseData(self):
        exec_js = self.driver.execute_script
        uCE = SharedTools.untilConditionExecute
        console_log('\nLicense uploads...', INFO)
        if platform.release() == '7' and webdriver_installer.platform[0] == 'win': # old browser versions
            for _ in range(DEFAULT_MAX_ITER):
                self.driver.get('https://home.eset.com/subscriptions') # refresh page
                try:
                    exec_js(f"{DEFINE_GET_EBAV_FUNCTION}\n{GET_EBAV}('button', 'data-label', 'license-list-open-detail-page-btn').click()")
                    break
                except:
                    time.sleep(3)
        else: # new browser versions
            self.driver.get('https://home.eset.com/subscriptions')
            uCE(self.driver, f"return {CLICK_WITH_BOOL}({GET_EBAV}('button', 'data-label', 'license-list-open-detail-page-btn'))")
        if self.driver.current_url.find('detail') != -1:
            console_log(f'License ID: {self.driver.current_url[-11:]}', OK)
        uCE(self.driver, f"return typeof {GET_EBAV}('div', 'class', 'LicenseDetailInfo') === 'object'")
        license_name = exec_js(f"return {GET_EBAV}('div', 'data-r', 'license-detail-product-name').innerText")
        license_out_date = exec_js(f"return {GET_EBAV}('div', 'data-r', 'license-detail-license-model-additional-info').innerText")
        license_key = exec_js(f"return {GET_EBAV}('div', 'data-r', 'license-detail-license-key').innerText")
        console_log('\nInformation successfully received!', OK)
        return license_name, license_key, license_out_date

class EsetBusinessRegister(object):
    def __init__(self, registered_email_obj: SecEmailAPI, eset_password: str, driver: Chrome):
        self.email_obj = registered_email_obj
        self.driver = driver
        self.eset_password = eset_password
        self.window_handle = None

    def createAccount(self):
        exec_js = self.driver.execute_script
        uCE = SharedTools.untilConditionExecute
        # STEP 0
        console_log('\nLoading EBA-ESET Page...', INFO)
        if args['email_api'] in ['hi2in', '10minutemail', 'tempmail', 'guerrillamail']:
            self.driver.switch_to.new_window('EsetBusinessRegister')
            self.window_handle = self.driver.current_window_handle
        self.driver.get('https://eba.eset.com/Account/Register?culture=en-US')
        uCE(self.driver, f'return {GET_EBID}("register-email") !== null')
        console_log('Successfully!', OK)
        time.sleep(1)

        # STEP 1
        console_log('\nData filling...', INFO)
        exec_js(f'return {GET_EBID}("register-email")').send_keys(self.email_obj.email)
        exec_js(f'return {GET_EBID}("register-password")').send_keys(self.eset_password)
        exec_js(f'return {GET_EBID}("register-confirm-password")').send_keys(self.eset_password)
        exec_js(f'return {GET_EBID}("register-continue-1")').click()
        time.sleep(2)

        # STEP 2
        uCE(self.driver, f'return {GET_EBID}("register-first-name") !== null')
        exec_js(f'return {GET_EBID}("register-first-name")').send_keys(SharedTools.createPassword(10))
        exec_js(f'return {GET_EBID}("register-last-name")').send_keys(SharedTools.createPassword(10))
        exec_js(f'return {GET_EBID}("register-phone")').send_keys(SharedTools.createPassword(12, True))
        exec_js(f'return {GET_EBID}("register-continue-2")').click()
        time.sleep(2)

        # STEP 3
        uCE(self.driver, f'return {GET_EBID}("register-company-name") !== null')
        exec_js(f'return {GET_EBID}("register-company-name")').send_keys(SharedTools.createPassword(10))
        exec_js(f'{GET_EBID}("register-country").value = "227: 230"') # Ukraine
        exec_js(f'return {GET_EBID}("register-continue-3")').click()
        console_log('Successfully!', OK)
        time.sleep(1)

        # STEP 4
        uCE(self.driver, f'return {GET_EBID}("register-back-4") !== null')
        console_log(f'\n{Fore.CYAN}Solve the captcha on the page manually!!!{Fore.RESET}', INFO, False)
        while True: # captcha
            try:
                mtcaptcha_solved_token = exec_js(f'return {GET_EBCN}("mtcaptcha-verifiedtoken")[0].value')
                if mtcaptcha_solved_token != '':
                    break
            except Exception as E:
                pass
            time.sleep(1)
        exec_js(f'{GET_EBID}("isAgreedToTerms").click()')
        exec_js(f'return {GET_EBID}("register-back-4")').click()
        for _ in range(DEFAULT_MAX_ITER):
            if exec_js(f'return {GET_EBID}("registration-error") !== null'):
                raise RuntimeError('\nESET temporarily blocked your IP, try again later!!! TRY VPN!!!')
            if exec_js(f'return {GET_EBID}("registration-success") !== null'):
                console_log('Successfully!', OK)
                return True
            time.sleep(1.5)
        raise RuntimeError('\nESET temporarily blocked your IP, try again later!!! TRY VPN!!!')

    def confirmAccount(self):
        if args['custom_email_api']:
            token = SharedTools.parseToken(self.email_obj, max_iter=100, delay=3)
        else:
            console_log(f'\n[{args["email_api"]}] EBA-ESET-Token interception...', INFO)
            if args['email_api'] in ['hi2in', '10minutemail', 'tempmail', 'guerrillamail']:
                token = SharedTools.parseToken(self.email_obj, self.driver, True, max_iter=100, delay=3)
                self.driver.switch_to.window(self.window_handle)
            else:
                token = SharedTools.parseToken(self.email_obj, eset_business=True, max_iter=100, delay=3) # 1secmail, developermail
        console_log(f'EBA-ESET-Token: {token}', OK)
        console_log('\nAccount confirmation is in progress...', INFO)
        self.driver.get(f'https://eba.eset.com/Account/InitActivation?token={token}')
        SharedTools.untilConditionExecute(self.driver, f'return {GET_EBID}("username") !== null')
        console_log('Account successfully confirmed!', OK)

class EsetBusinessKeygen(object):
    def __init__(self, registered_email_obj: SecEmailAPI, eset_password: str, driver: Chrome):
        self.email_obj = registered_email_obj
        self.eset_password = eset_password
        self.driver = driver

    def sendRequestForKey(self):
        exec_js = self.driver.execute_script
        uCE = SharedTools.untilConditionExecute

        # Log in
        console_log('\nLogging in to the created account...', INFO)
        exec_js(f'return {GET_EBID}("username")').send_keys(self.email_obj.email)
        exec_js(f'return {GET_EBID}("password")').send_keys(self.eset_password)
        exec_js(f'return {GET_EBID}("btn-login").click()')
        
        # Start free trial
        uCE(self.driver, f'return {GET_EBID}("dashboard-create-eca-trial") !== null', delay=2)
        console_log('Successfully!', OK)
        console_log('\nSending a request for a get license...', INFO)
        exec_js(f'{GET_EBID}("dashboard-create-eca-trial").click()')
        uCE(self.driver, f'return {GET_EBID}("add-license-key-Agree-edtd-terms") !== null')
        exec_js(f'{GET_EBID}("add-license-key-Agree-edtd-terms").click()')
        exec_js(f'{GET_EBID}("edtd-eula-continue").click()')
        uCE(self.driver, f'return {GET_EBID}("btn-eca-eula-accept") !== null')
        console_log('Request successfully sent!', OK)
    
    def getLicenseData(self):
        exec_js = self.driver.execute_script
        uCE = SharedTools.untilConditionExecute

        console_log('\nLicense uploads...', INFO)
        self.driver.get('https://eba.eset.com/ba/licenses')
        for _ in range(DEFAULT_MAX_ITER):
            try:
                license_full_tag = self.driver.find_element('xpath', '//span[starts-with(@id, "license-list-license")]').get_attribute('id')
                break
            except:
                pass
            time.sleep(DEFAULT_DELAY)
        if license_full_tag is not None:     
            license_full_tag = license_full_tag[21:-1].split('-') # license-list-license-3B3-B8J-VA3-2017 -> [3B3, B8J, VA3, 2017]
            license_tag = '-'.join(license_full_tag[0:3]) # 3B3-B8J-VA3
            license_year = license_full_tag[-1] # 2017
            self.driver.get(f'https://eba.eset.com/ba/licenses/license/{license_tag}/{license_year}/overview')
            uCE(self.driver, f'return {GET_EBID}("specific-license-overview-license-key") !== null')
            console_log('License is uploaded!', OK)     
            console_log('\nGetting information from the license...', INFO)
            license_name = 'ESET Endpoint Security + ESET Server Security - Universal License'
            license_key = exec_js(f'return {GET_EBID}("specific-license-overview-license-key").innerText').strip()
            license_out_date = exec_js(f'return {GET_EBID}("specific-license-overview-expiration-date").innerText').strip()
            console_log('Information successfully received!', OK)
            return license_name, license_key, license_out_date
        else:
            raise RuntimeError('Error!')

if __name__ == '__main__':
    print(LOGO)
    args_parser = argparse.ArgumentParser()
    # Required
    ## Browsers
    args_browsers = args_parser.add_mutually_exclusive_group(required=True)
    args_browsers.add_argument('--chrome', action='store_true', help='Launching the project via Google Chrome browser')
    args_browsers.add_argument('--firefox', action='store_true', help='Launching the project via Mozilla Firefox browser')
    args_browsers.add_argument('--edge', action='store_true', help='Launching the project via Microsoft Edge browser')
    ## Modes of operation
    args_modes = args_parser.add_mutually_exclusive_group(required=True)
    args_modes.add_argument('--key', action='store_true', help='Generating an ESET-HOME license key (example as AGNV-XA2V-EA89-U546-UVJP)')
    args_modes.add_argument('--account', action='store_true', help='Generating an ESET HOME Account (To activate the free trial version)')
    args_modes.add_argument('--business-account', action='store_true', help='Generating an ESET BUSINESS Account (To huge businesses) - Requires manual captcha input!!!')
    args_modes.add_argument('--business-key', action='store_true', help='Generating an ESET BUSINESS Account and creating a universal license key for ESET products (1 key - 75 devices) - Requires manual captcha input!!!')
    args_modes.add_argument('--only-update', action='store_true', help='Updates/installs webdrivers and browsers without generating account and license key')
    # Optional
    args_parser.add_argument('--skip-webdriver-menu', action='store_true', help='Skips installation/upgrade webdrivers through the my custom wrapper (The built-in selenium-manager will be used)')
    args_parser.add_argument('--no-headless', action='store_true', help='Shows the browser at runtime (The browser is hidden by default, but on Windows 7 this option is enabled by itself)')
    args_parser.add_argument('--custom-browser-location', type=str, default='', help='Set path to the custom browser (to the binary file, useful when using non-standard releases, for example, Firefox Developer Edition)')
    args_parser.add_argument('--email-api', choices=['1secmail', 'hi2in', '10minutemail', 'tempmail', 'guerrillamail', 'developermail'], default='developermail', help='Specify which api to use for mail')
    args_parser.add_argument('--custom-email-api', action='store_true', help='Allows you to manually specify any email, and all work will go through it. But you will also have to manually read inbox and do what is described in the documentation for this argument')
    args_parser.add_argument('--try-auto-cloudflare',action='store_true', help='Removes the prompt for the user to press Enter when solving cloudflare captcha. In some cases it may go through automatically, which will give the opportunity to use tempmail in automatic mode!')
    try:
        try:
            args = vars(args_parser.parse_args())
        except:
            time.sleep(3)
            sys.exit(-1)
        
        # initialization and configuration of everything necessary for work
        webdriver_installer = WebDriverInstaller()
        # changing input arguments for special cases
        if platform.release() == '7' and webdriver_installer.platform[0] == 'win': # fix for Windows 7
            args['no_headless'] = True
        elif args['business_account'] or args['business_key'] or args['email_api'] in ['tempmail']:
            args['no_headless'] = True
        
        driver = None
        webdriver_path = None
        browser_name = 'chrome'
        if args['firefox']:
            browser_name = 'firefox'
        if args['edge']:
            browser_name = 'edge'
        if not args['skip_webdriver_menu']: # updating or installing webdriver
            webdriver_path = webdriver_installer.webdriver_installer_menu(args['edge'], args['firefox'])
            if webdriver_path is not None:
                os.chmod(webdriver_path, 0o777)
        if not args['only_update']:
            driver = SharedTools.initSeleniumWebDriver(browser_name, webdriver_path, args['custom_browser_location'], (not args['no_headless']))
        else:
            sys.exit(0)

        # main part of the programd
        if not args['custom_email_api']:
            console_log(f'\n[{args["email_api"]}] Mail registration...', INFO)
            if args['email_api'] == '10minutemail':
                email_obj = TenMinuteMailAPI(driver)
            elif args['email_api'] == 'hi2in':
                email_obj = Hi2inAPI(driver)
            elif args['email_api'] == 'tempmail':
                email_obj = TempMailAPI(driver)
            elif args['email_api'] == 'guerrillamail':
                email_obj = GuerRillaMailAPI(driver)
            elif args['email_api'] == 'developermail':
                email_obj = DeveloperMailAPI()
            elif args['email_api'] == '1secmail':
                email_obj = SecEmailAPI()
            email_obj.init()
            console_log('Mail registration completed successfully!', OK)
        else:
            email_obj = CustomEmailAPI()
            while True:
                email = input(f'\n[  {Fore.YELLOW}INPT{Fore.RESET}  ] {Fore.CYAN}Enter the email address you have access to: {Fore.RESET}').strip()
                try:
                    matched_email = re.match(r"[-a-z0-9+]+@[a-z]+\.[a-z]{2,3}", email).group()
                    if matched_email == email:
                        email_obj.email = matched_email
                        console_log('Mail has the correct syntax!', OK)
                        break
                    else:
                        raise RuntimeError
                except:
                    console_log('Invalid email syntax!!!', ERROR)
        eset_password = SharedTools.createPassword(10)
        
        # standart generator
        if args['account'] or args['key']:
            EsetReg = EsetRegister(email_obj, eset_password, driver)
            EsetReg.createAccount()
            EsetReg.confirmAccount()
            output_line = '\n'.join([
                    '',
                    '----------------------------------',
                    f'Account Email: {email_obj.email}',
                    f'Account Password: {eset_password}',
                    '----------------------------------',
                    ''
            ])        
            output_filename = 'ESET ACCOUNTS.txt'
            if args['key']:
                output_filename = 'ESET KEYS.txt'
                EsetKeyG = EsetKeygen(email_obj, driver)
                EsetKeyG.sendRequestForKey()
                license_name, license_key, license_out_date = EsetKeyG.getLicenseData()
                output_line = '\n'.join([
                    '',
                    '----------------------------------',
                    f'Account Email: {email_obj.email}',
                    f'Account Password: {eset_password}',
                    '',
                    f'License Name: {license_name}',
                    f'License Key: {license_key}',
                    f'License Out Date: {license_out_date}',
                    '----------------------------------',
                    ''
                ])
                
        # new generator
        elif args['business_account'] or args['business_key']:
            EsetBusinessReg = EsetBusinessRegister(email_obj, eset_password, driver)
            EsetBusinessReg.createAccount()
            EsetBusinessReg.confirmAccount()
            output_line = '\n'.join([
                    '',
                    '----------------------------------',
                    f'Business Account Email: {email_obj.email}',
                    f'Business Account Password: {eset_password}',
                    '----------------------------------',
                    ''
            ])    
            output_filename = 'ESET ACCOUNTS.txt'
            if args['business_key']:
                output_filename = 'ESET KEYS.txt'
                EsetBusinessKeyG = EsetBusinessKeygen(email_obj, eset_password, driver)
                EsetBusinessKeyG.sendRequestForKey()
                license_name, license_key, license_out_date = EsetBusinessKeyG.getLicenseData()
                output_line = '\n'.join([
                    '',
                    '----------------------------------',
                    f'Business Account Email: {email_obj.email}',
                    f'Business Account Password: {eset_password}',
                    '',
                    f'License Name: {license_name}',
                    f'License Key: {license_key}',
                    f'License Out Date: {license_out_date}',
                    '----------------------------------',
                    ''
                ])        
        # end
        console_log(output_line)
        date = datetime.datetime.now()
        f = open(f"{str(date.day)}.{str(date.month)}.{str(date.year)} - "+output_filename, 'a')
        f.write(output_line)
        f.close()
        driver.quit()
    
    except Exception as E:
        traceback_string = traceback.format_exc()
        if str(type(E)).find('selenium') and traceback_string.find('Stacktrace:') != -1: # disabling stacktrace output
            traceback_string = traceback_string.split('Stacktrace:', 1)[0]
        console_log(traceback_string, ERROR)
        time.sleep(3) # exit-delay
