from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import time

# 初始化 WebDriver
driver = webdriver.Chrome()

# 启动chrome driver
service = Service(executable_path='/Users/ashley/PycharmProjects/slrtool-main/chromedriver')
driver = webdriver.Chrome(service=service)

# 访问IEEE搜索结果页面
driver.get(
    'https://ieeexplore.ieee.org/search/searchresult.jsp?highlight=true&returnType=SEARCH&refinements=ContentType:Courses&refinements=ContentType:Conferences&refinements=Author:Yu%20Zhang&ranges=2023_2023_Year&returnFacets=ALL')

# 等待搜索结果加载完成
wait = WebDriverWait(driver, 10)
wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='xplMainContent']/div[2]/div[2]/xpl-results-list")))

# 循环处理每一页的搜索结果
while True:
    # 找到类型为checkbox，Select All on Page
    checkbox = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, "results-actions-selectall-checkbox")))
    # 检查复选框的当前状态
    if not checkbox.is_selected():
        # 如果复选框未被选中，则点击勾选
        checkbox.click()

    # 点击导出按钮
    export_button1 = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='xplMainContent']/div[1]/div[1]/ul/li[2]/xpl-export-search-results/button/a")))
    export_button1.click()

    # 找到并点击"Citations"按钮
    cite_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Citations']")))
    cite_button.click()

    # 定位单选框元素"BibTeX"标签
    bibtex_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//label[@for='download-bibtex']//input")))
    bibtex_button.click()

    # 定位单选框元素citation-abstract
    ci_ab_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//label[@for='citation-abstract']//input")))
    ci_ab_button.click()

    # # 定位导出按钮元素,等待导出页面加载完成
    # button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='ngb-nav-24-panel']/div/form/div[2]/button")))
    # button.click()

    # 定位元素
    export_button = driver.find_element(By.XPATH, "//*[@id='ngb-nav-24-panel']/div/form/div[2]/button")

    # 创建 ActionChains 对象，移动鼠标到元素位置再点击
    actions = ActionChains(driver)
    actions.move_to_element(export_button).click().perform()


    # 切换到导出页面
    driver.switch_to.window(driver.window_handles[-1])

    # 获取并保存 BibTeX 内容
    bibtex_element = driver.find_element(By.TAG_NAME, "body")
    bibtex_content = bibtex_element.text
    # 在这里将 bibtex_content 保存到文件或其他位置
    print(bibtex_content)
    with open('bibtex_citations.bib', 'a') as f:
        f.write(bibtex_content + '\n')
    # 关闭导出页面
    driver.close()

    # 切换回搜索结果页面
    driver.switch_to.window(driver.window_handles[0])

    # 等待搜索结果页面加载完成
    wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='xplMainContent']/div[2]/div[2]/xpl-results-list")))
    #
    # # 点击下一页链接
    # next_link = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='xplMainContent']/div[2]/div[2]/xpl-paginator/div[2]/ul/li[3]/a")))
    # next_link.click()

    # 等待下一页加载完成
    time.sleep(5)  # 等待页面加载完成，根据实际情况调整等待时间

# 关闭浏览器
driver.quit()
