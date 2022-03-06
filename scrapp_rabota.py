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


def get_url(get, index):
    get = get.replace(' ', '+').strip().lower()
    main_url = f'https://www.rabota.ru/vacancy/?query={get}&sort=date&schedule_ids=6&period=month'
    return main_url

data_works = []
checker = []
def scrapp(get, driver, data_words, data_black):
    url = get_url(get, 0)
    driver.get(url)

    while True:
        if driver.find_elements_by_xpath('//div[@class="vacancy-preview-card__wrapper white-box"]'):
            sleep(3)
            break

    for item in driver.find_elements_by_xpath('//div[@class="vacancy-preview-card__wrapper white-box"]'):
        item.location_once_scrolled_into_view
        sleep(0.1)

        item_url = item.find_element_by_xpath('.//a[@itemprop="title"]').get_attribute('href').replace('\n', '').strip()
        item_name = item.find_element_by_xpath('.//a[@itemprop="title"]').text.replace('\n', '').strip()

        try:
            item_money = item.find_element_by_xpath('.//div[@class="vacancy-preview-card__salary vacancy-preview-card__salary-blue"]').text.strip()
        except:
            item_money = 'Нет информации'

        if item_money == '':
            item_money = 'Нет информации'

        answer = [ True for i in data_words if i.lower() in item_name.lower() ]
        answer = True if True in answer else False

        _answer = [ True for i in data_black if i.lower() in item_name.lower() ]
        _answer = True if True in _answer else False

        
        if not scrappIngfo.select().where(scrappIngfo.scrappName == item_name, scrappIngfo.scrappCash == item_money) and answer and not _answer:
            print('scrapp')
            scrappIngfo(scrappName = item_name, scrappCash = item_money, scrappUrl = item_url).save()    
    return

def start_rabota():
    driver = browser()

    data_words = str(words.get(words.id == 1).white).split(',')
    data_black = str(words.get(words.id == 1).black).split(',')

    try:
        for search in data_words:
            scrapp(search, driver, data_words, data_black)
            sleep(3)

        print('End works. Not errors.')
        driver.close()
    except Exception as err:
        print(err) 
        driver.close()

