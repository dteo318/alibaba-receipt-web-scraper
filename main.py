from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
import json
import os
import shutil

# Global Constants
options = webdriver.ChromeOptions()
settings = {
       "recentDestinations": [{
            "id": "Save as PDF",
            "origin": "local",
            "account": "",
        }],
        "selectedDestinationId": "Save as PDF",
        "version": 2
    }
prefs = {'printing.print_preview_sticky_settings.appState': json.dumps(settings)}
options.add_experimental_option('prefs', prefs)
options.add_argument('--kiosk-printing')
options.add_argument("--window-size=1600x1000")

# Chromedriver is for v86 of Chrome
# Download applicable selenium chromedriver 
CHROMEDRIVER_PATH = "./drivers/chromedriver" # --- EDIT HERE IF CHANGING ENVIRONMENT
browser = webdriver.Chrome(chrome_options=options, executable_path=CHROMEDRIVER_PATH) 
browser.implicitly_wait(60)
current_pages = 0

# Global Variables 
website = "https://www.1688.com/index.html"
username = None # --- Enter username here
password = None # --- Enter password here
# Intended download directory to store files in 
download_files_directory = "/Users/dteo183/Documents/Python/Projects/alibaba-receipt-web-scraper/Files" # --- EDIT HERE IF CHANGING ENVIRONMENT
# The standard downloads directory that Chrome downloads to 
standard_downloads_directory = "/Users/dteo183/Downloads/" # --- EDIT HERE IF CHANGING ENVIRONMENT
starting_page = 1 # --- CHANGE THE PAGE TO START DOWNLOADING RECEIPTS FROM
num_pages = starting_page + 5 # --- CHANGE THE NUMBER OF PAGES TO DOWNLOAD


# # Opening website main-page
browser.get(website)
close_popup_main = browser.find_element_by_class_name("identity-close-icon")
close_popup_main.click()

# Going to login page
my_space = browser.find_element_by_link_text("我的阿里")
my_space_hover = ActionChains(browser).move_to_element(my_space)
my_space_hover.perform()
items_sold = browser.find_element_by_link_text("已买到货品")
items_sold.click()

# Logging in
# Will have to bypass 2FA manually first since it requires OTP SMS
browser.switch_to.window(browser.window_handles[-1])
WebDriverWait(browser, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,'//*[@id="loginchina"]/iframe')))
WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="fm-login-id"]'))).send_keys(username)
browser.find_element_by_id("fm-login-password").send_keys(password)
time.sleep(7)
browser.find_element_by_xpath('//*[@id="login-form"]/div[4]/button').click()

# Finding page to download
time.sleep(3)
browser.switch_to_frame(0)
receipts_from_3months_ago = browser.find_element_by_xpath('//*[@id="new-content"]/div[3]/div/div/div/ul/li[2]/a')
receipts_from_3months_ago.click()
time.sleep(7)

# Navigating to the starting page
while current_pages < starting_page:
    next_page = browser.find_element_by_link_text("下一页")
    next_page.click()
    time.sleep(3)
    current_pages += 1

# Downloading elements
while current_pages < num_pages:
    receipts_to_download = browser.find_elements_by_class_name("bannerOrderDetail")
    filename = None
    for receipt in receipts_to_download:
        receipt.click()
        browser.switch_to.window(browser.window_handles[-1])
        try:
            WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'offer-title')))
            title = browser.find_elements_by_class_name('offer-title')[0].text
            filename = title
            browser.find_element_by_link_text('打印订单详情').click()
            time.sleep(3)
            browser.switch_to.window(browser.window_handles[-1])
            browser.execute_script('window.print();')
            browser.close()
            browser.switch_to.window(browser.window_handles[-1])
            browser.close()
            browser.switch_to.window(browser.window_handles[-1])
            time.sleep(5)
        except:
            browser.close()
            browser.switch_to.window(browser.window_handles[-1])
            receipt.click()
            browser.switch_to.window(browser.window_handles[-1])
            WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'offer-title')))
            title = browser.find_elements_by_class_name('offer-title')[0].text
            filename = title
            browser.find_element_by_link_text('打印订单详情').click()
            time.sleep(3)
            browser.switch_to.window(browser.window_handles[-1])
            browser.execute_script('window.print();')
            browser.close()
            browser.switch_to.window(browser.window_handles[-1])
            browser.close()
            browser.switch_to.window(browser.window_handles[-1])
            time.sleep(5)
        print(filename)
        # Reformatting filename 
        if '/' in filename:
            filename = filename.replace('/', '_', filename.count('/'))
        file_name = max([standard_downloads_directory + f for f in os.listdir(standard_downloads_directory)],key=os.path.getctime)
        count = 0
        # Moving file from standard download directory to intended downloads directory
        for f in os.listdir(download_files_directory):
            if f.startswith(title):
                count += 1
        if count == 0:
            shutil.move(file_name,os.path.join(download_files_directory, "{}.pdf".format(filename)))
        else:
            shutil.move(file_name,os.path.join(download_files_directory, "{} ({}).pdf".format(filename, count)))
    next_page = browser.find_element_by_link_text("下一页")
    next_page.click()
    time.sleep(3)
    current_pages += 1

print("~~~~~~~~~~~~~~~~~~~~~~DONE!~~~~~~~~~~~~~~~~~~~~~~~")
time.sleep(3)
browser.quit()
