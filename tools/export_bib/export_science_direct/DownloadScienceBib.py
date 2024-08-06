from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
import time


def download_bib(search_url):
    # 初始化 WebDriver
    driver = webdriver.Chrome()

    # 启动chrome driver
    service = Service(executable_path='/Users/ashley/PycharmProjects/slrtool-main/chromedriver')
    driver = webdriver.Chrome(service=service)
    FLAG = True

    # 访问Science Direct搜索结果页面
    driver.get(search_url)

    # 等待搜索结果加载完成
    wait = WebDriverWait(driver, 10)
    wait.until(EC.visibility_of_element_located((By.ID, 'srp-results-list')))

    # # 每页显示100
    # display_button = WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.XPATH, '//*[@id="srp-pagination-options"]/div[1]/ol/li[3]/span')))
    # display_button.click()

    while FLAG:
        select_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="srp-toolbar"]/div[1]/div[1]/div/label/span[1]')))
        select_button.click()

        export_button1 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="srp-toolbar"]/div[1]/div[3]/div/div/button/span/span')))
        export_button1.click()

        bibtex_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div/div/div/p/div/div/button[3]/span')))
        bibtex_button.click()

        time.sleep(3)

        try:
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//li[@class='pagination-link next-link']/a")))
            driver.execute_script("arguments[0].scrollIntoView();", next_button)
            next_button.click()
        except TimeoutException:  # 当 next_button 不存在时
            FLAG = False
            driver.quit()

        time.sleep(3)  # 等待页面加载完成，根据实际情况调整等待时间


class DownloadScienceBib:
    pass





