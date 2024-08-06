import pdfplumber
import os
import re
import pandas as pd

path1 = '/Users/ashley/Desktop/0131/229'
path2 = '/Users/ashley/Desktop/0131/selection_0131'
path3 = '/Users/ashley/Desktop/0131/test'
# 指定要搜索的文件夹路径
folder_path = path2

# GitHub链接的正则表达式
github_url_pattern = re.compile(r'https://github\.com/[a-zA-Z0-9\-_]+/[a-zA-Z0-9\-_]+')

# 参考文献部分可能使用的标题
references_titles = ["References", "Bibliography"]

# 用于存储结果的列表，每个元素将是一个包含文件名和链接的列表
results = []

# 获取所有PDF文件的路径
pdf_files = [os.path.join(root, file) for root, dirs, files in os.walk(folder_path) for file in files if file.endswith('.pdf')]

# 遍历所有PDF文件
for i, pdf_path in enumerate(pdf_files, start=1):
    print(f"Processing file {i}/{len(pdf_files)}: {os.path.basename(pdf_path)}")
    links_found = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    # 检查是否到达了参考文献部分
                    if any(title in text for title in references_titles):
                        print("  Skipping references section...")
                        break  # 假设参考文献部分位于文档末尾，跳出循环

                    links = github_url_pattern.findall(text)
                    if links:
                        links_found.extend(links)  # 将找到的链接添加到列表中
                        print(f"  Found {len(links)} GitHub links on this page.")
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")

    if links_found:  # 如果找到了链接
        # 将所有链接合并为一个字符串，每个链接之间用换行符分隔
        links_str = '\n'.join(set(links_found))  # 使用set去重
        results.append([os.path.basename(pdf_path), links_str])

# 创建DataFrame
df = pd.DataFrame(results, columns=["File Name", "GitHub Links"])

# 保存到Excel文件
excel_path = os.path.join(folder_path, 'github_links22.xlsx')
df.to_excel(excel_path, index=False)

print(f"Results saved to {excel_path}.")