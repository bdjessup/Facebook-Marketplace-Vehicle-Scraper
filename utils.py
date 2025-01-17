import json
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


with open("./setup.json") as fin:
    setup = json.load(fin)

# search queries
location = "mansfield"
model = "r6"
exact = "False"
maxPrice = 2000

sortby = 0  # 0-name, 1-price, 2-mileage, 3-loc


def send(driver, cmd, params={}):
    resource = "/session/%s/chromium/send_command_and_get_result" % driver.session_id
    url = driver.command_executor._url + resource
    body = json.dumps({'cmd': cmd, 'params': params})
    response = driver.command_executor._request('POST', url, body)
    return response.get('value')


def save_page(url, fname):
    # open page
    options = webdriver.ChromeOptions()
    options.add_argument("--save-page-as-mhtml")
    options.add_argument("--disable-notifications")
    browser = webdriver.Chrome(executable_path=(
        setup['facebook']['WebDriver_Path']), options=options)
    # Bypass facebook login
    browser.get(url)
    browser.find_element(By.NAME, "email").send_keys(setup['facebook']['email'])
    browser.find_element(By.NAME, "pass").send_keys(
        setup['facebook']['password'])
    browser.find_element(By.XPATH, "//div[@aria-label='Accessible login button']").click()
    sleep(5)
    browser.find_element(By.XPATH,
        "//input[@aria-label='Search Marketplace']").click()
    sleep(1)
    browser.find_element(By.XPATH,
        "//input[@aria-label='Search Marketplace']").clear()
    sleep(1)
    browser.find_element(By.XPATH,
        "//input[@aria-label='Search Marketplace']").send_keys(setup['facebook']['model'])
    sleep(1)
    browser.find_element(By.XPATH,
        "//input[@aria-label='Search Marketplace']").send_keys(Keys.ENTER)
    sleep(1)
    browser.find_element(By.XPATH,
        "//input[@aria-label='Minimum Range']").click()
    sleep(1)
    browser.find_element(By.XPATH,
        "//input[@aria-label='Minimum Range']").clear()
    sleep(1)
    browser.find_element(By.XPATH,
        "//input[@aria-label='Minimum Range']").send_keys(setup['facebook']['min_price'])
    sleep(1)
    browser.find_element(By.XPATH,
        "//input[@aria-label='Maximum Range']").click()
    sleep(1)
    browser.find_element(By.XPATH,
        "//input[@aria-label='Maximum Range']").clear()
    sleep(1)
    browser.find_element(By.XPATH,
        "//input[@aria-label='Maximum Range']").send_keys(setup['facebook']['max_price'])
    sleep(1)
    browser.find_element(By.XPATH,
        "//input[@aria-label='Search Marketplace']").send_keys(Keys.ENTER)
    
    browser.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[3]/div/div/div[1]/div[1]/div[1]/div/div[3]/div[1]/div[2]/div[3]/div[2]/div[2]/div[1]/div[1]/div[1]/span/span").click()
    browser.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[3]/div/div/div[1]/div[1]/div[1]/div/div[3]/div[1]/div[2]/div[3]/div[2]/div[2]/div[2]/div/div[1]/div[3]/div/div[1]/div/div[1]/div/div/div/span").click()

    
    sleep(1)
    print(browser.current_url)

    # scroll
    for i in range(3):
        browser.execute_script(f"window.scrollTo(0, {4000*i})")
        sleep(2)

    # snapshot and save
    res = send(browser, "Page.captureSnapshot", {"format": "mhtml"})

    resd = str(res['data']).replace("=\n\n", "")
    with open(fname, "w",  encoding='utf-8') as file:
        file.write(resd)
    return fname


def get_price(pcl):
    # print(pcl[0].get_text().split("$"))
    return "$"+str(int(pcl[0].get_text().split("$")[1].replace(",", "").replace("\n", "")))


def get_mileage(pcl):
    # return pcl[3].get_text().replace(" miles","")
    strmiles = pcl[3].get_text().split(" =")[0].replace(
        " miles", "").replace("K", "000").replace("M", "000000")
    if "." in strmiles:
        strsep = strmiles.replace(".", "")
        return int(strsep)

    if len(strmiles) > 0:
        if str(strmiles) == "Dealership":
            strmiles2 = "Dealership"
        elif int(float(strmiles)) == int(strmiles):
            strmiles2 = int(strmiles)
        else:
            strmiles2 = "N/A"
    else:
        strmiles2 = "N/A"  # (or number = 0 if you prefer)

    return strmiles2


def get_link(p):
    linktmp = p.parent.parent.parent.find("a").get("href")
    if "3D\"" in linktmp[0:3]:
        return linktmp[3:-1]
    return linktmp
