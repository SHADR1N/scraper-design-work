from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from time import time, sleep
from models import *

def browser():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--headless")
    options.add_argument('--no-sandbox')

    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options = options)
    return driver


def get_url():
    main_url = f'https://designer.ru/u/'
    return main_url

data_works = []
def scrapp(driver, data_words, data_black):
    
    url = get_url()
    driver.get(url)

    while True:
        if driver.find_elements_by_xpath('//div[@class="uk-width-large-1-5 uk-width-medium-1-3 uk-width-small-1-1 uk-margin-large-bottom"]'):
            break

    for item in driver.find_elements_by_xpath('//div[@class="uk-width-large-1-5 uk-width-medium-1-3 uk-width-small-1-1 uk-margin-large-bottom"]'):
        item.location_once_scrolled_into_view
        sleep(0.1)

        item_url = item.find_elements_by_xpath('.//a')[-1].get_attribute('href').replace('\n', '').strip()
        item_name = item.find_elements_by_xpath('.//b')[-1].text.replace('\n', '').strip()

        try:
            item_money = item.find_elements_by_xpath('.//p')[-1].text.strip()
        except:
            item_money = 'Нет информации'

        if item_money == '':
            item_money = 'Нет информации'

        answer = [ True for i in data_words if i.lower() in item_name.lower() ]
        answer = True if True in answer else False

        _answer = [ True for i in data_black if i.lower() in item_name.lower() ]
        _answer = True if True in _answer else False

        if not scrappIngfo.select().where(scrappIngfo.scrappUrl == item_url) and answer and not _answer:
            print('scrapp')
            scrappIngfo(scrappName = item_name, scrappCash = item_money, scrappUrl = item_url).save()
            
    return

def start_desig():
    driver = browser()

    data_words = str(words.get(words.id == 1).white).split(',')
    data_black = str(words.get(words.id == 1).black).split(',')

    try:
        scrapp(driver, data_words, data_black)
        print('End works. Not errors.')
        driver.close()
    except Exception as err:
        print(err) 
        driver.close()

