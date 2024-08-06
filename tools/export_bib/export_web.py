import os

# 定义目录和结果文件
RIS_DIR = r"C:\Users\Ashley\Downloads\web_of_science"
OUTPUT_RIS = "web_of_science.ris"

# 获取目录下所有的ris文件
ris_files = [f for f in os.listdir(RIS_DIR) if f.endswith('.ris')]

# 为结果文件创建一个新的文件
with open(OUTPUT_RIS, 'w', encoding='utf-8') as outfile:
    # 遍历所有的ris文件
    for filename in ris_files:
        with open(os.path.join(RIS_DIR, filename), 'r', encoding='utf-8') as infile:
            # 读取文件内容并写入到结果文件
            for line in infile:
                outfile.write(line)
        # 在每个文件之间添加一个空行，以清晰地分隔不同的ris条目
        outfile.write('\n')
