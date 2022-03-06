from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from time import time, sleep
import json
from models import *

def browser():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--headless")
    options.add_argument('--no-sandbox')

    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options = options)
    driver.get('https://hh.ru/')

    sleep(3)
    with open('hh.json', 'r') as f:
        kok = json.load(f)
        
        for i in kok:
            driver.add_cookie(i)

    return driver


def get_url(get, index):
    get = get.replace(' ', '+').strip().lower()
    main_url = f'https://hh.ru/search/vacancy?area=1&clusters=true&enable_snippets=true&text={get}&schedule=remote&showClusters=true&page={index}'
    return main_url

data_works = []
def scrapp(get, driver, data_words, data_black):
    
    url = get_url(get, 0)

    driver.get(url)
    while True:
        if driver.find_elements_by_xpath('//div[@class="vacancy-serp-item"]'):
            break
    paginations = len(driver.find_element_by_xpath('//span[@class="bloko-button-group"]').find_elements_by_xpath('.//*[@data-qa="pager-page"]'))
    for i in range(paginations):
        url = get_url(get, i)
        driver.get(url)
        while True:
            if driver.find_elements_by_xpath('//div[@class="vacancy-serp-item"]'):
                break

        conteiner = driver.find_element_by_xpath('//div[@data-qa="vacancy-serp__results"]')
        for item in conteiner.find_elements_by_xpath('.//div[@data-qa="vacancy-serp__vacancy vacancy-serp__vacancy_standard_plus"]'):
            item.location_once_scrolled_into_view
            sleep(0.1)

            item_url = item.find_element_by_xpath('.//a[@data-qa="vacancy-serp__vacancy-title"]').get_attribute('href').replace('\n', '').strip()
            item_name = item.find_element_by_xpath('.//a[@data-qa="vacancy-serp__vacancy-title"]').text.replace('\n', '').strip()

            if item.find_elements_by_xpath('.//div[@class="vacancy-serp-item__sidebar"]'):
                item_money = item.find_element_by_xpath('.//div[@class="vacancy-serp-item__sidebar"]').text.replace(' ', '').replace('\n', '').strip()
            else:
                item_money = 'Нет информации'

            if item_money == '':
                item_money = 'Нет информации'

            answer = [ True for i in data_words if i.lower() in item_name.lower() ]
            answer = True if True in answer else False

            _answer = [ True for i in data_black if i.lower() in item_name.lower() ]
            _answer = True if True in _answer else False
            
            item_url = item_url.split('?from')[0].strip()
            if not scrappIngfo.select().where(scrappIngfo.scrappUrl == item_url) and answer and not _answer:
                print('scrapp')
                scrappIngfo(scrappName = item_name, scrappCash = item_money, scrappUrl = item_url).save()

        sleep(3)
            
    return

def start_hh():
    driver = browser()

    data_words = str(words.get(words.id == 1).white).split(',')
    data_black = str(words.get(words.id == 1).black).split(',')

    try:
        for search in data_words:
            scrapp(search, driver, data_words, data_black)
            sleep(5)

        print('End works. Not errors.')
        driver.close()
    except Exception as err:
        print(err) 
        driver.close()




