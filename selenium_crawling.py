from selenium.webdriver import ChromeOptions
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from datetime import datetime

def get_weekday_number():
    today = datetime.today()
    weekday_number = today.isoweekday()
    return str(weekday_number)

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

def get_학식_경희대():
    options = ChromeOptions()
    options.add_experimental_option("detach", True)
    options.add_argument("headless")

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    URL = 'https://dorm2.khu.ac.kr/40/4050.kmc'
    driver.get(url=URL)
    # driver.implicitly_wait(time_to_wait=5)
    week_num = get_weekday_number()
    morning = driver.find_element(By.ID,"fo_menu_mor"+week_num).text
    lunch = driver.find_element(By.ID,"fo_menu_lun"+week_num).text
    evening = driver.find_element(By.ID,"fo_menu_eve"+week_num).text
    driver.quit()
    return (morning,lunch,evening)

def get_학식_경북대():
    output = []
    options = ChromeOptions()
    options.add_experimental_option("detach", True)
    options.add_argument("headless")

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    URL = "https://dorm.knu.ac.kr/_new_ver/newlife/05.php?get_mode=4"
    driver.get(url=URL)
    # driver.implicitly_wait(time_to_wait=5)
    week_num = get_weekday_number()
    elements = driver.find_elements(By.CLASS_NAME, "txt_right")
    for element in elements:
        output.append(element.text)

    driver.quit()
    return output
