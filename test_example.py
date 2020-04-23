from time import sleep
from random import choice, randint
from users import names, lastnames


def test_example(driver, url):
    sleep(randint(1, 180))
    driver.get(url)
    driver.get(url)
    driver.implicitly_wait(60)
    driver.find_element_by_xpath('//*[@id="name"]').send_keys(f'{choice(names)} {choice(lastnames)}')
    driver.find_element_by_xpath('//*[@id="modal-enter-to-event_0"]/div/div/div[4]/input').click()

    sleep(30)
