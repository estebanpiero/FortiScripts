# Domain Category Checker
This repository contains a Python script that uses Selenium to automate the process of checking the categories of a list of domains on the FortiGuard Web Filter service.

## Prerequisites
Before you can run the script, you need to have the following installed:

1. Python 3.x
2. Selenium
3. Google Chrome
4. ChromeDriver

## Setup

- Clone the repository:
```bash
git clone https://github.com/yourusername/domain-category-checker.git
cd domain-category-checker
```

- Install the required Python packages:

```
pip install selenium
```

- Download ChromeDriver:

1. Download ChromeDriver from [https://googlechromelabs.github.io/chrome-for-testing]
2. Place the chromedriver.exe file in the appropriate location (update the chrome_driver_path variable in the script if needed).

- Prepare the domains list:

1. Create a file named __Domains.txt__ in the root directory of the repository.
2. Add the domains you want to check, each on a new line.
Usage

## Run the script:

```
python webfiler.py
```

This script will open Google Chrome and navigate to the FortiGuard Web Filter page for each domain in __Domains.txt__. It will then retrieve the category of each domain and save the results to a file named Categories.txt.

## Script Explanation

The script performs the following steps:

- Setup Chrome options and service:

```python
chrome_options = Options()
chrome_options.add_experimental_option('detach', True)   # Prevents Selenium from closing the browser
service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)
```

- Read the domains list:

```python
domains_file = open('Domains.txt', 'r')
domains_list = domains_file.readlines()
```

- Iterate over the domains and fetch categories:

```python
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
```

- Quit the browser:

```python
driver.quit()
```

## Notes

1. Ensure that the chromedriver.exe path is correctly set in the chrome_driver_path variable.
2. The script adds a delay (time.sleep(2)) to allow the page to load properly. You can adjust this delay if needed.
3. The script outputs the results to Categories.txt in JSON format, one entry per line.
