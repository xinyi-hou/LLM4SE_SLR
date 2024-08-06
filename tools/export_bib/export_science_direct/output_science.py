import os

# 设置目录和文件名
BIB_DIR = "/Users/ashley/Downloads"
SCIENCE_BIB = "science.bib"

# 获取目录下所有的bib文件
bib_files = [file for file in os.listdir(BIB_DIR) if file.endswith(".bib")]

# 拼接所有bib文件的内容
content = ""
for bib_file in bib_files:
    bib_path = os.path.join(BIB_DIR, bib_file)
    with open(bib_path, "r") as file:
        content += file.read()

# 将拼接后的内容写入新的bib文件中
with open(SCIENCE_BIB, "w") as output_file:
    output_file.write(content)
