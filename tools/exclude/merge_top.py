import os
import pandas as pd

def merge_csv_files(directory):
    # 获取文件夹内所有csv文件
    csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]

    # 创建一个空的DataFrame用来存储数据
    df = pd.DataFrame()

    # 遍历csv文件
    for file in csv_files:
        file_path = os.path.join(directory, file)
        # 读取csv文件到临时的DataFrame
        temp_df = pd.read_csv(file_path)
        # 将临时的DataFrame添加到最终的DataFrame，如果列不一致，使用并集的方式添加
        df = pd.concat([df, temp_df], join='outer')

    # 返回合并后的DataFrame
    return df

# 指定你的文件夹路径
directory = '/Users/ashley/Downloads/litmap'

# 调用函数合并CSV文件
merged_df = merge_csv_files(directory)

# 你也可以保存合并后的DataFrame为新的CSV文件
merged_df.to_csv('litmap.csv', index=False)
