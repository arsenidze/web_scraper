from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import traceback
import datetime
import csv

options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)
wait = WebDriverWait(driver, 5)

LOGIN_URL = 'https://www.aihitdata.com/login?next=https%3A//www.aihitdata.com/'

EMAIL_FIELD_ID = 'email'
EMAIL = 'arsenidze@ukr.net'
PASSWORD_FIELD_ID = 'password'
PASSWORD = 'aihit_4321'
# title = The Company Database | aiHit
LOGIN_BUTTON_ID = 'submit'

COOKIE_BUTTON_XPATH = '''//p[@class='cc_message']/preceding::a[1]'''

COMPANY_FIELD_ID = 'company'
COMPANY_DOMAIN = 'mortgage'

LOCATION_FIELD_ID = 'location'
COMPANY_LOCATION = 'US'

FILTERS_DROPDOWN_ID = 'filtersIcon'
ACTIVATE_CHECKBOXES_IDS = ['hasWebsite', 'hasEmail', 'hasPhone', 'hasAddress']

SEARCH_BUTTON_XPATH = '''//button[contains(@class, 'btn btn-info btn-block')][text()='Search']'''

COMPANIES_LINKS =	'''//p[@class='text-muted'][text()[contains(.,'results')]]/parent::div/child::div[contains(@class, 'panel panel-default')]/div[contains(@class, 'panel-body')]/div/a'''

COMPANY_INFO_ELEMENTS = list(map(lambda x: {'xpath': f'''//i[contains(@class, '{x[0]}')]/parent::*''', 'type': x[1]}, \
  [('icon-sm icon-home', 'website'), ('icon-sm icon-email', 'email'), ('icon-sm icon-phone', 'phone'), ('icon-sm icon-map-marker', 'address')]))


OUTPUT_FILEPATH = f'./results/{COMPANY_DOMAIN}_companies'

def generate_filename(basename, ext = 'csv'):
  suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
  filename = "_".join([basename, suffix]) # e.g. 'mylogfile_120508_171442'
  filename += '.' + ext
  return filename


def find_element(by, locator):
  try:
    element = driver.find_element(by, locator)
  except:
    return None
  return element


def input_element(by, locator, text):
  element = wait.until(ec.visibility_of_element_located((by, locator)))
  element.send_keys(text)


def click_element(by, locator):
  element = wait.until(ec.element_to_be_clickable((by, locator)))
  element.click()


def login():
  driver.get(LOGIN_URL)
  input_element(By.ID, EMAIL_FIELD_ID, EMAIL)
  input_element(By.ID, PASSWORD_FIELD_ID, PASSWORD)
  click_element(By.ID, LOGIN_BUTTON_ID)


def remove_specific_cookie_popup():
  element = wait.until(ec.element_to_be_clickable((By.XPATH, COOKIE_BUTTON_XPATH)))
  driver.execute_script("arguments[0].click();", element) # https://stackoverflow.com/a/58378714


def search_mortgage_companies():
  input_element(By.ID, COMPANY_FIELD_ID, COMPANY_DOMAIN)
  input_element(By.ID, LOCATION_FIELD_ID, COMPANY_LOCATION)
  click_element(By.ID, FILTERS_DROPDOWN_ID)

  for checkbox_id in ACTIVATE_CHECKBOXES_IDS:
    click_element(By.ID, checkbox_id)

  click_element(By.XPATH, SEARCH_BUTTON_XPATH)


def get_infos_from_companies():
  infos = []
  links = driver.find_elements_by_xpath(COMPANIES_LINKS)
  links_hrefs = [link.get_attribute('href') for link in links]
  for l_href in links_hrefs:
    driver.get(l_href)
    info = get_info_from_one_company()
    infos.append(info)
    driver.back()
  return infos


def get_info_from_one_company():
  info = {}
  for elem in COMPANY_INFO_ELEMENTS:
    element = find_element(By.XPATH, elem['xpath'])
    info[elem['type']] = element.text if element else ''
  return info


def save_infos_to_csv_file(infos, filename = generate_filename(OUTPUT_FILEPATH)):
  if not infos:
    return 
  with open(filename, 'w') as csvfile: 
    writer = csv.DictWriter(csvfile, fieldnames = infos[0].keys()) 
    writer.writeheader() 
    writer.writerows(infos) 


def tasks():
  login()
  remove_specific_cookie_popup()
  search_mortgage_companies()
  infos = get_infos_from_companies()
  save_infos_to_csv_file(infos)


if __name__ == "__main__":
  try:
    tasks()
  except Exception:
    print(traceback.print_exc())
  finally:
    driver.close()
    driver.quit()