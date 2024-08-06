import bibtexparser
import pandas as pd
import re
from FindVenues import *

# 定义文件路径
UNIQUE_BIB = '../remove_duplicates/no_duplicates/springer_unique.bib'
OUTPUT_XLSX = 'springer/springer_output_llm2.xlsx'
CONTEXT_KEYWORDS = '../handle_keywords/context_related.txt'
TECHNIQUES_KEYWORDS = '../handle_keywords/llm_related.txt'

# 读取BibTeX文件
with open(UNIQUE_BIB, 'r') as bib_file:
    bib_database = bibtexparser.load(bib_file)

# 将BibTeX条目转化为pandas DataFrame
df = pd.DataFrame(bib_database.entries)

# 在DataFrame中添加一个新的列
df['CHECK_PAGES'] = ""  # 标记页数少于8的
df['REVIEW'] = ""  # 标记SLR、Review、Survey
df['TITLE_CK'] = ""   # title中含关键词A+B
df['ABSTRACT_CK'] = ""  # abstract中含关键词A+B
df['KEYWORDS_CK'] = ""  # keywords中含关键词A+B
df['NO_CK'] = ""  # 不含关键词A+B
df['EXCLUDE'] = ""  # 不符合要求的替条目需要排除
df['VENUE'] = ''  # 会议期刊
df['RANK'] = ''  # 会议期刊等级

# 尝试将页数转换为数值，并标记无法转换的条目
df['start_page'] = pd.to_numeric(df['pages'].str.split('--', expand=True)[0], errors='coerce')
df['end_page'] = pd.to_numeric(df['pages'].str.split('--', expand=True)[1], errors='coerce')

# 标记无法计算页数的条目
df.loc[df['start_page'].isna() | df['end_page'].isna(), 'CHECK_PAGES'] += 'Few pages'

# 对于可以计算页数的条目，如果页数少于8页，则在备注列中添加 'Few pages '
df.loc[(df['end_page'] - df['start_page'] < 7) & (~df['start_page'].isna()) & (~df['end_page'].isna()), 'CHECK_PAGES'] += 'Few pages'
# 从数据帧中删除start_page和end_page列
df = df.drop(columns=['start_page', 'end_page'])


df.loc[df['title'].str.contains('Systematic Literature Review', case=False, na=False), 'REVIEW'] += '/SLR'
df.loc[df['title'].str.contains('Review', case=False, na=False), 'REVIEW'] += '/Review'
df.loc[df['title'].str.contains('Survey', case=False, na=False), 'REVIEW'] += '/Survey'

# 读取关键词列表
with open(CONTEXT_KEYWORDS, 'r') as file:
    context_keywords = [r'\b' + line.strip() + r'\b' for line in file]
with open(TECHNIQUES_KEYWORDS, 'r') as file:
    techniques_keywords = [r'\b' + line.strip() + r'\b' for line in file]


def filter1():
    # 查找"title"、"abstract"和"keywords"字段中的关键词，并将找到的关键词记录在新的列中
    for index, row in df.iterrows():
        if pd.notnull(row['title']):
            title_ck = find_keywords(row['title'], context_keywords, techniques_keywords)
            if title_ck:
                df.at[index, 'TITLE_CK'] = title_ck
        if pd.notnull(row['abstract']):
            abstract_ck = find_keywords(row['abstract'], context_keywords, techniques_keywords)
            if abstract_ck:
                df.at[index, 'ABSTRACT_CK'] = abstract_ck
        # 如果 'TITLE_CK', 'ABSTRACT_CK', 和 'KEYWORDS_CK'这三列都是空的，则在'NO_CK'列中填入'NO_CK'
        if df.loc[index, 'TITLE_CK'] == '' and df.loc[index, 'ABSTRACT_CK'] == '' == '':
            df.loc[index, 'NO_CK'] = 'NO_CK'
        # 页数少于8，不含关键词的条目排除
        if df.loc[index, 'CHECK_PAGES'] == 'Few pages' or df.loc[index, 'NO_CK'] == 'NO_CK' or pd.to_numeric(
                df.loc[index, 'year']) < 2017:
            df.loc[index, 'EXCLUDE'] = 'EXCLUDE'


def filter2():
    for index, row in df.iterrows():
        if pd.notnull(row['title']):
            title_ck = find_keywords2(row['title'], techniques_keywords)
            if title_ck:
                df.at[index, 'TITLE_CK'] = title_ck
        if pd.notnull(row['abstract']):
            abstract_ck = find_keywords2(row['abstract'], techniques_keywords)
            if abstract_ck:
                df.at[index, 'ABSTRACT_CK'] = abstract_ck
        # 如果 'TITLE_CK', 'ABSTRACT_CK', 和 'KEYWORDS_CK'这三列都是空的，则在'NO_CK'列中填入'NO_CK'
        if df.loc[index, 'TITLE_CK'] == '' and df.loc[index, 'ABSTRACT_CK'] == '' == '':
            df.loc[index, 'NO_CK'] = 'NO_CK'
        # 页数少于8，不含关键词的条目排除
        if df.loc[index, 'CHECK_PAGES'] == 'Few pages' or df.loc[index, 'NO_CK'] == 'NO_CK' or pd.to_numeric(
                df.loc[index, 'year']) < 2017:
            df.loc[index, 'EXCLUDE'] = 'EXCLUDE'


filter2()

df = set_venue(df, 'url', VENUES)
df = set_venue(df, 'journal', VENUES)
df = set_venue(df, 'doi', VENUES)
df = set_venue(df, 'abstract', VENUES)
df = set_venue_lower(df, 'ID', VENUES)

# 将结果写入Excel的第一个表单
with pd.ExcelWriter(OUTPUT_XLSX, engine='openpyxl') as writer:
    df.to_excel(writer, index=False, sheet_name='All Entries')

    df_filtered = df[df['EXCLUDE'] == '']
    df_filtered.to_excel(writer, index=False, sheet_name='Filtered Entries')

    # # 过滤出ICSE的条目
    # df_icse = df[df['abstract'].str.contains('ICSE', case=False, na=False, regex=False) & (df['EXCLUDE'] == '')]
    # df_icse.to_excel(writer, index=False, sheet_name='ICSE Entries')
    #
    # # 过滤出ASE的条目
    # df_ase = df[df['journal'].str.contains('Automated Software Engineering', case=False, na=False, regex=False) & (
    #             df['EXCLUDE'] == '')]
    # df_ase.to_excel(writer, index=False, sheet_name='ASE Entries')
    #
    # # 过滤出TSE的条目
    # df_tse = df[df['abstract'].str.contains('TSE', case=False, na=False, regex=False) & (df['EXCLUDE'] == '')]
    # df_tse.to_excel(writer, index=False, sheet_name='TSE Entries')

