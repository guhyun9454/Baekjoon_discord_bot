from selenium.webdriver import ChromeOptions
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def get_실검():
    options = ChromeOptions()
    options.add_experimental_option("detach", True)
    options.add_argument("headless")

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)


    URL = 'https://signal.bz/news'
    driver.get(url=URL)
    driver.implicitly_wait(time_to_wait=10)
    date_now = driver.find_element(by=By.XPATH, value='//*[@id="app"]/div/main/div/section/div/section/section[1]/div[1]/div[1]/span')
    naver_results = driver.find_elements(By.CSS_SELECTOR, '#app > div > main > div > section > div > section > section:nth-child(2) > div > div > div > div > a > span.rank-text')

    temp = [date_now.text]

    for naver_result in naver_results:
        temp.append(naver_result.text)

    driver.quit()

    return temp
