from time import sleep
from random import choice, randint
from users import names, lastnames
from helpers import string_generator


def test_example(driver, url):
    sleep(randint(1, 300))
    driver.get(url)
    driver.implicitly_wait(60)
    driver.find_element_by_xpath('//*[text()="зарегистрироваться"]').click()
    driver.find_element_by_xpath('//*[@id="email"]').send_keys(f'{string_generator(7)}@bot.ru')
    driver.find_element_by_xpath('//*[@id="lastName"]').send_keys(f'{choice(lastnames)}')
    driver.find_element_by_xpath('//*[@id="firstName"]').send_keys(f'{choice(names)}')
    driver.find_element_by_xpath('/html/body/div[6]/div/div/div[3]/div[4]/input').send_keys(f'{+79998887766}')
    driver.find_element_by_xpath('/html/body/div[6]/div/div/div[3]/div[5]/input').send_keys(f'{"Москва"}')
    driver.find_element_by_xpath('/html/body/div[6]/div/div/div[3]/div[6]/input').send_keys(f'{"Москва"}')
    driver.find_element_by_xpath('/html/body/div[6]/div/div/div[3]/div[7]/input').send_keys(f'{"Москва"}')
    driver.find_element_by_xpath('/html/body/div[6]/div/div/div[3]/div[8]/input').send_keys(f'{"Москва"}')
    driver.find_element_by_xpath('//*[@id="modal-enter-register-form_0"]/div/div/div[4]/input').click()
    driver.find_element_by_xpath('//*[@id="modal-enter-to-event_0"]/div/div/div[4]/input').click()

    sleep(7200)
