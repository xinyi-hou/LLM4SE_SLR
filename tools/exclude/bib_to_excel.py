import bibtexparser
import pandas as pd
import re

# 定义文件路径
UNIQUE_BIB = '/Users/ashley/Documents/acm_0131.bib'
OUTPUT_XLSX = '/Users/ashley/Documents/acm.xlsx'
CONTEXT_KEYWORDS = '../handle_keywords/context_related.txt'
TECHNIQUES_KEYWORDS = '../handle_keywords/llm_related.txt'

# 读取BibTeX文件
with open(UNIQUE_BIB, 'r') as bib_file:
    bib_database = bibtexparser.load(bib_file)

# 将BibTeX条目转化为pandas DataFrame
df = pd.DataFrame(bib_database.entries)
# #
# # # 在DataFrame中添加一个新的列
# # df['CHECK_PAGES'] = ""  # 标记页数少于8的
# # df['REVIEW'] = ""  # 标记SLR、Review、Survey
# df['TITLE_CK'] = ""   # title中含关键词A+B
# df['ABSTRACT_CK'] = ""  # abstract中含关键词A+B
# df['KEYWORDS_CK'] = ""  # keywords中含关键词A+B
# df['NO_CK'] = ""  # 不含关键词A+B
# # df['EXCLUDE'] = ""  # 不符合要求的替条目需要排除
# #
# # # 尝试将页数转换为数值，并标记无法转换的条目
# # df['start_page'] = pd.to_numeric(df['pages'].str.split('--', expand=True)[0], errors='coerce')
# # df['end_page'] = pd.to_numeric(df['pages'].str.split('--', expand=True)[1], errors='coerce')
# #
# # # 标记无法计算页数的条目
# # df.loc[df['start_page'].isna() | df['end_page'].isna(), 'CHECK_PAGES'] += 'Few pages'
# #
# # # 对于可以计算页数的条目，如果页数少于8页，则在备注列中添加 'Few pages '
# # df.loc[(df['end_page'] - df['start_page'] < 7) & (~df['start_page'].isna()) & (~df['end_page'].isna()), 'CHECK_PAGES'] += 'Few pages'
# # # 从数据帧中删除start_page和end_page列
# # df = df.drop(columns=['start_page', 'end_page'])
# #
# #
# # df.loc[df['title'].str.contains('Systematic Literature Review', case=False, na=False), 'REVIEW'] += '/SLR'
# # df.loc[df['title'].str.contains('Review', case=False, na=False), 'REVIEW'] += '/Review'
# # df.loc[df['title'].str.contains('Survey', case=False, na=False), 'REVIEW'] += '/Survey'
#
#
# # 读取关键词列表
# with open(CONTEXT_KEYWORDS, 'r') as file:
#     context_keywords = [r'\b' + line.strip() + r'\b' for line in file]
# with open(TECHNIQUES_KEYWORDS, 'r') as file:
#     techniques_keywords = [r'\b' + line.strip() + r'\b' for line in file]
#
#
# # 创建函数用于查找关键词
# def find_keywords(text, c_keywords, t_keywords):
#     found_context_keywords = [keyword for keyword in c_keywords if re.search(keyword, text, re.IGNORECASE)]
#     found_techniques_keywords = [keyword for keyword in t_keywords if re.search(keyword, text, re.IGNORECASE)]
#     if found_context_keywords and found_techniques_keywords:
#         return ', '.join(found_context_keywords + found_techniques_keywords).replace(r'\b', '')
#     else:
#         return ''
#
#
# # 查找"title"、"abstract"和"keywords"字段中的关键词，并将找到的关键词记录在新的列中
# for index, row in df.iterrows():
#     if pd.notnull(row['title']):
#         title_ck = find_keywords(row['title'], context_keywords, techniques_keywords)
#         if title_ck:
#             df.at[index, 'TITLE_CK'] = title_ck
#     if pd.notnull(row['abstract']):
#         abstract_ck = find_keywords(row['abstract'], context_keywords, techniques_keywords)
#         if abstract_ck:
#             df.at[index, 'ABSTRACT_CK'] = abstract_ck
#     if pd.notnull(row['keywords']):
#         keywords_ck = find_keywords(row['keywords'], context_keywords, techniques_keywords)
#         if keywords_ck:
#             df.at[index, 'KEYWORDS_CK'] = keywords_ck
#     # 如果 'TITLE_CK', 'ABSTRACT_CK', 和 'KEYWORDS_CK'这三列都是空的，则在'NO_CK'列中填入'NO_CK'
#     if df.loc[index, 'TITLE_CK'] == '' and df.loc[index, 'ABSTRACT_CK'] == '' and df.loc[index, 'KEYWORDS_CK'] == '':
#         df.loc[index, 'NO_CK'] = 'NO_CK'
#     if df.loc[index, 'NO_CK'] == 'NO_CK':
#         df.loc[index, 'EXCLUDE'] = 'EXCLUDE'
#
# 将结果写入Excel的第一个表单
with pd.ExcelWriter(OUTPUT_XLSX, engine='openpyxl') as writer:
    df.to_excel(writer, index=False, sheet_name='All Entries')
#
#     df_filtered = df[df['EXCLUDE'] == '']
#     df_filtered.to_excel(writer, index=False, sheet_name='Filtered Entries')

