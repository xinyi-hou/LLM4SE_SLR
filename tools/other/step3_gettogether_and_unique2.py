import pandas as pd
paths = [
            "ACM/ACM",
            "Arxiv/Arxiv",
            "dblp/dblp",
            "IEEE/IEEE",
            "Springer/springer",
            "Science_Direct/Science_direct",
            "WebofScience/webofscience"
        ]
ends = [
    "_analysis_2_remained.csv",
    "_analysis_3.csv",
]

for end in ends:
    df = pd.concat([pd.read_csv(path + end) for path in paths], ignore_index=True)
    df = df.drop_duplicates(subset=['Title', 'Url'])
    df = df.sort_values('Title')

    temp = df
    # 标记重复值
    df['标记重复值'] = df.duplicated(subset=['Title'])
    # 输出去重后的数据到新文件
    df.to_csv('./ALL/all' + end, index=False)

    df = temp.drop_duplicates(subset=['Title'])
    df.to_csv('./ALL/all_title_unique' + end, index=False)

# 输出完成信息
print('去重后的数据已经保存')