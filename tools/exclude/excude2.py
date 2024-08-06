import pandas as pd
import openpyxl
import re

# 定义文件路径
ALL_FILTERED = 'filtered_excel/merge_llm_entries.xlsx'
UNIQUE_FILTERED = 'excluded_excel/merge_llm_filtered.xlsx'
LLM_TOP_VENUES = 'filtered_excel/llm_top_venues.xlsx'

# 读取excel文件
df = pd.read_excel(ALL_FILTERED)
df_llm = pd.read_excel(LLM_TOP_VENUES)

df['SAME_TITLE'] = ''
df['SOURCE'] = ''
df['VENUE'] = ''

# 将标题转化为小写，并查找重复的条目
duplicate_mask = df['title'].str.lower().duplicated(keep='first')
# 对于重复的条目，在"SAME_TITLE"列中填入"SAME_TITLE"
df.loc[duplicate_mask, 'SAME_TITLE'] = 'SAME_TITLE'

# df.loc[df['Item Type'].str.contains('thesis', case=False, na=False, regex=False), 'SOURCE'] = 'PhD Thesis'
# df.loc[df['Item Type'].str.contains('book', case=False, na=False, regex=False), 'SOURCE'] = 'book'
# df.loc[df['Item Type'].str.contains('book', case=False, na=False, regex=False), 'SOURCE'] = 'bookSection'

# 将标题列转换为小写以进行大小写敏感匹配
df['title'] = df['title'].str.lower()
df_llm['title'] = df_llm['title'].str.lower()

# 对每一个标题在LLM_TOP_VENUES中进行搜索
for index, row in df.iterrows():
    venue = df_llm[df_llm['title'] == row['title']]['top venue'].values
    if len(venue) > 0:
        df.at[index, 'VENUE'] = venue[0]

# 保存到新的工作表单
with pd.ExcelWriter(UNIQUE_FILTERED, engine="openpyxl") as writer:
    df.to_excel(writer, index=False, sheet_name='All filtered')

    # 获取'SAME_TITLE'列为空的所有条目
    df_unique = df[df['SAME_TITLE'] == '']
    df_unique.to_excel(writer, index=False, sheet_name='Unique filtered')

    # # 获取'SOURCE'列为空的所有条目
    # df_source = df[(df['SOURCE'] == '') & (df['SAME_TITLE'] == '')]
    # df_source.to_excel(writer, index=False, sheet_name='Source filtered')


