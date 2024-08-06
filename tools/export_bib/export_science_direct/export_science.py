from DownloadScienceBib import *

# os.environ['https_proxy'] = 'http://127.0.0.1:1080'
SEARCH_URL_LIST = "science_search_urls.txt"

# 读取URL列表文件
with open(SEARCH_URL_LIST, 'r') as file:
    search_urls = file.readlines()

count = 0
# 遍历每个URL
for search_url in search_urls:
    search_url = search_url.strip() + "&show=100"  # 去除可能存在的换行符
    count = count + 1
    print(count, ": ", search_url)

    # 初始化 WebDriver
    driver = webdriver.Chrome()

    try:
        download_bib(search_url)

    except Exception as e:
        print(f"Error while processing URL {search_url}: {e}")
        continue  # 如果发生错误，跳过这个URL并继续处理下一个URL

    finally:
        # 关闭浏览器
        driver.quit()
