import pytest
from selenium import webdriver


def pytest_addoption(parser):
    parser.addoption('--url', default="https://events.webinar.ru/intermeda/3987434")


@pytest.fixture
def url(request):
    return request.config.getoption('--url')


@pytest.fixture
def driver(request):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')   # прячет все дополнительные окна браузера
    options.add_argument('mute-audio')   # запускает без звука
    driver = webdriver.Chrome(chrome_options=options)
    request.addfinalizer(driver.quit)
    return driver
