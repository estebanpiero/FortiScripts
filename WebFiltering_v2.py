import time
import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

chrome_driver_path = 'D:\Developers\chrome\chromedriver.exe'
chrome_options = Options()
chrome_options.add_experimental_option('detach',True)   #Avoids Selenium to close the browser
driver = webdriver.Chrome(executable_path=chrome_driver_path,chrome_options=chrome_options)

domains_file = open('Domains.txt','r')
domains_list = domains_file.readlines()

for domain in domains_list:
    driver.get('https://www.fortiguard.com/webfilter')
    #time.sleep(5)
    search = driver.find_element(By.NAME,'url')
    
    search.send_keys(domain)
    search.send_keys(Keys.ENTER)
    time.sleep(2)
    category_response = driver.find_element(By.CLASS_NAME, value='info_title').text
    
    #print('---------------------')

    result = category_response[10:]
    domain = {
        'Domain' : domain[:-1],
        'Category' : result
    }

    with open(f'Categories.txt','a') as outputs:
        json.dump(domain, outputs)
        outputs.write('\n')

    print(domain)

