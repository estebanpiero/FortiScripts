Domain Category Checker
This repository contains a Python script that uses Selenium to automate the process of checking the categories of a list of domains on the FortiGuard Web Filter service.

Prerequisites
Before you can run the script, you need to have the following installed:

Python 3.x
Selenium
Google Chrome
ChromeDriver
Setup
Clone the repository:

bash
Copy code
git clone https://github.com/yourusername/domain-category-checker.git
cd domain-category-checker
Install the required Python packages:

bash
Copy code
pip install selenium
Download ChromeDriver:

Download ChromeDriver from here.
Place the chromedriver.exe file in the appropriate location (update the chrome_driver_path variable in the script if needed).
Prepare the domains list:

Create a file named Domains.txt in the root directory of the repository.
Add the domains you want to check, each on a new line.
Usage
Run the script:

bash
Copy code
python domain_category_checker.py
This script will open Google Chrome and navigate to the FortiGuard Web Filter page for each domain in Domains.txt. It will then retrieve the category of each domain and save the results to a file named Categories.txt.

Script Explanation
The script performs the following steps:

Setup Chrome options and service:

python
Copy code
chrome_options = Options()
chrome_options.add_experimental_option('detach', True)   # Prevents Selenium from closing the browser
service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)
Read the domains list:

python
Copy code
domains_file = open('Domains.txt', 'r')
domains_list = domains_file.readlines()
Iterate over the domains and fetch categories:

python
Copy code
for domain in domains_list:
    driver.get('https://www.fortiguard.com/webfilter')
    search = driver.find_element(By.NAME, 'url')
    search.send_keys(domain)
    search.send_keys(Keys.ENTER)
    time.sleep(2)
    category_response = driver.find_element(By.CLASS_NAME, value='info_title').text

    result = category_response[10:]
    domain_info = {
        'Domain': domain.strip(),
        'Category': result
    }

    with open('Categories.txt', 'a') as outputs:
        json.dump(domain_info, outputs)
        outputs.write('\n')
Quit the browser:

python
Copy code
driver.quit()
Notes
Ensure that the chromedriver.exe path is correctly set in the chrome_driver_path variable.
The script adds a delay (time.sleep(2)) to allow the page to load properly. You can adjust this delay if needed.
The script outputs the results to Categories.txt in JSON format, one entry per line.
License
This project is licensed under the MIT License - see the LICENSE file for details.

Feel free to modify this README to better suit your needs.
