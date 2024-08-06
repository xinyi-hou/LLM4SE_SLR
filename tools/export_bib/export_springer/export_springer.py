import os
import pandas as pd

# 定义目录和结果文件
SEARCH_RESULTS = "/Users/ashley/Downloads/search_results"
SPRINGER_URL = "springer_doi.txt"

# 获取目录下所有的csv文件
csv_files = [f for f in os.listdir(SEARCH_RESULTS) if f.endswith('.csv')]

# 创建一个空的set，用于存储所有的URL
urls = set()

# 遍历所有的csv文件
for file in csv_files:
    # 读取csv文件
    df = pd.read_csv(os.path.join(SEARCH_RESULTS, file))
    # 检查"URL"列是否存在
    if "Item DOI" in df.columns:
        # 提取"URL"列，并将其添加到set中
        urls.update(df["Item DOI"].tolist())

# 将URLs写入到结果文件中
with open(SPRINGER_URL, 'w') as f:
    for url in urls:
        f.write(url + '\n')
