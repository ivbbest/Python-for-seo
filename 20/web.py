import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

path = os.path.join(os.getcwd(), 'chromedriver.exe')

text = 'hello world'
options = Options()

options.binary_location = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"    #chrome binary location specified here
options.add_argument("--start-maximized") #open Browser in maximized mode
options.add_argument("--no-sandbox") #bypass OS security model
options.add_argument("--disable-dev-shm-usage") #overcome limited resource problems
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
browser = webdriver.Chrome(executable_path=path, options=options)

browser.get('https://www.bing.com/translator')
sleep(2)

search_input_tag = browser.find_element_by_id('tta_input_ta')
search_input_tag.click()
search_input_tag.send_keys(text)
sleep(2)

# изменяю язык на немецкий

search_lang_tag = browser.find_element_by_id('tta_tgtsl')
search_lang_tag.find_element_by_css_selector('#t_tgtAllLang > option:nth-child(38)').click()

sleep(2)

translate = browser.find_element_by_xpath('//*[@id="tta_output_ta"]').get_attribute("value")
print(translate)

browser.close()

with open('translate.txt', 'w', encoding='utf-8') as f:
    f.write(translate)
