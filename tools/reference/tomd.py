import pandas as pd


def convert_excel_to_markdown(input_file, output_file):
    # 读取Excel文件
    df = pd.read_excel(input_file)

    # 构建Markdown格式的字符串
    markdown = ""

    # 遍历每一行数据
    for index, row in df.iterrows():
        # 获取每一列的值
        title = row['Title']
        year = row['Publication Year']
        venue = row['VENUE']
        author = row['Author']

        # 构建Markdown行
        markdown += f"- **{title}** ({year}), {venue}, {author}.\n"

    # 将Markdown格式写入文件
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(markdown)


# 输入Excel文件路径
input_file = 'input/tomd.xlsx'

# 输出文本文件路径
output_file = 'output/1.txt'

# 转换为Markdown格式并输出到文件
convert_excel_to_markdown(input_file, output_file)

print("转换完成。")