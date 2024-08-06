import pandas as pd

# 读取CSV文件
df = pd.read_csv('./Springer/springer.csv',low_memory=False)

# 根据Title和Url字段去重
df = df.drop_duplicates(subset=['Title', 'Url'])

# 输出去重后的数据到新文件
df.to_csv('./Springer/springer_unique.csv', index=False)

# 输出完成信息
print('去重后的数据已经保存')