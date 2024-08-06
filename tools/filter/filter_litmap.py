import bibtexparser
import pandas as pd
import re
from FindVenues import *

# 定义文件路径
UNIQUE_BIB = '../remove_duplicates/no_duplicates/litmap_unique.bib'
OUTPUT_XLSX = 'litmap/litmap_output_llm3.xlsx'
CONTEXT_KEYWORDS = '../handle_keywords/context_related.txt'
TECHNIQUES_KEYWORDS = '../handle_keywords/llm_related.txt'

# # 读取BibTeX文件
# with open(UNIQUE_BIB, 'r') as bib_file:
#     bib_database = bibtexparser.load(bib_file)
#
# # 将BibTeX条目转化为pandas DataFrame
# df = pd.DataFrame(bib_database.entries)

df = pd.read_excel('litmap/litmap1.xlsx')

# 在DataFrame中添加新的列
df['REVIEW'] = ""  # 标记SLR、Review、Survey
df['TITLE_CK'] = ""   # title中含关键词A+B
df['ABSTRACT_CK'] = ""  # abstract中含关键词A+B
# df['KEYWORDS_CK'] = ""  # keywords中含关键词A+B
df['NO_CK'] = ""  # 不含关键词A+B
df['EXCLUDE'] = ""  # 不符合要求的替条目需要排除
df['VENUE'] = ''  # 会议期刊
df['RANK'] = ''  # 会议期刊等级

df.loc[df['Title'].str.contains('Systematic Literature Review', case=False, na=False), 'REVIEW'] += '/SLR'
df.loc[df['Title'].str.contains('Review', case=False, na=False), 'REVIEW'] += '/Review'
df.loc[df['Title'].str.contains('Survey', case=False, na=False), 'REVIEW'] += '/Survey'


# 读取关键词列表
with open(CONTEXT_KEYWORDS, 'r') as file:
    context_keywords = [r'\b' + line.strip() + r'\b' for line in file]
with open(TECHNIQUES_KEYWORDS, 'r') as file:
    techniques_keywords = [r'\b' + line.strip() + r'\b' for line in file]


def filter1():
    # 查找"title"、"abstract"和"keywords"字段中的关键词，并将找到的关键词记录在新的列中
    for index, row in df.iterrows():
        try:
            if pd.notnull(row['Title']):
                title_ck = find_keywords(row['Title'], context_keywords, techniques_keywords)
                if title_ck:
                    df.at[index, 'TITLE_CK'] = title_ck
            if pd.notnull(row['Abstract Note']):
                abstract_ck = find_keywords(row['Abstract Note'], context_keywords, techniques_keywords)
                if abstract_ck:
                    df.at[index, 'ABSTRACT_CK'] = abstract_ck
        except TypeError as e:
            print("Error occurred:", e)
        # if pd.notnull(row['keywords']):
        #     keywords_ck = find_keywords(row['keywords'], context_keywords, techniques_keywords)
        #     if keywords_ck:
        #         df.at[index, 'KEYWORDS_CK'] = keywords_ck
        # 如果 'TITLE_CK', 'ABSTRACT_CK', 和 'KEYWORDS_CK'这三列都是空的，则在'NO_CK'列中填入'NO_CK'
        if df.loc[index, 'TITLE_CK'] == '' and df.loc[index, 'ABSTRACT_CK'] == '':
            df.loc[index, 'NO_CK'] = 'NO_CK'
        # 页数少于8，不含关键词的条目排除
        if df.loc[index, 'NO_CK'] == 'NO_CK':
            df.loc[index, 'EXCLUDE'] = 'EXCLUDE'


def filter2():
    for index, row in df.iterrows():
        try:
            if pd.notnull(row['Title']):
                title_ck = find_keywords2(row['Title'], techniques_keywords)
                if title_ck:
                    df.at[index, 'TITLE_CK'] = title_ck
            if pd.notnull(row['Abstract Note']):
                abstract_ck = find_keywords2(row['Abstract Note'], techniques_keywords)
                if abstract_ck:
                    df.at[index, 'ABSTRACT_CK'] = abstract_ck
        except TypeError as e:
            print("Error occurred:", e)

        # if pd.notnull(row['keywords']):
        #     keywords_ck = find_keywords2(row['keywords'], techniques_keywords)
        #     if keywords_ck:
        #         df.at[index, 'KEYWORDS_CK'] = keywords_ck
        # 如果 'TITLE_CK', 'ABSTRACT_CK', 和 'KEYWORDS_CK'这三列都是空的，则在'NO_CK'列中填入'NO_CK'
        if df.loc[index, 'TITLE_CK'] == '' and df.loc[index, 'ABSTRACT_CK'] == '':
            df.loc[index, 'NO_CK'] = 'NO_CK'
        # 页数少于8，不含关键词的条目排除
        if df.loc[index, 'NO_CK'] == 'NO_CK':
            df.loc[index, 'EXCLUDE'] = 'EXCLUDE'


filter2()

df = set_venue(df, 'Conference Name', VENUES)
df = set_venue(df, 'Publication Title', VENUES)

# try:
#     df = set_venue(df, 'journal', VENUES)
# except ValueError as e:
#     print("Error occurred while setting venue:", e)
# try:
#     df = set_venue(df, 'doi', VENUES)
# except ValueError as e:
#     print("Error occurred while setting venue:", e)



# 将结果写入Excel
with pd.ExcelWriter(OUTPUT_XLSX, engine='openpyxl') as writer:
    df.to_excel(writer, index=False, sheet_name='All Entries')

    df_filtered = df[df['EXCLUDE'] == '']
    df_filtered.to_excel(writer, index=False, sheet_name='Filtered Entries')
