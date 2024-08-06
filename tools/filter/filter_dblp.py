import bibtexparser
import pandas as pd
import re
from FindVenues import *

# 定义文件路径
UNIQUE_BIB = '../remove_duplicates/no_duplicates/dblp_0131.bib'
OUTPUT_XLSX = 'dblp/dblp_output_0131.xlsx'
CONTEXT_KEYWORDS = '../handle_keywords/context_related.txt'
TECHNIQUES_KEYWORDS = '../handle_keywords/llm_related.txt'

# # 读取BibTeX文件
# with open(UNIQUE_BIB, 'r') as bib_file:
#     bib_database = bibtexparser.load(bib_file)
#
# # 将BibTeX条目转化为pandas DataFrame
# df = pd.DataFrame(bib_database.entries)
df = pd.read_excel('dblp/dblp_0131.xlsx')

# 在DataFrame中添加新的列
df['REVIEW'] = ""  # 标记SLR、Review、Survey
df['TITLE_CK'] = ""   # title中含关键词A+B
df['ABSTRACT_CK'] = ""  # abstract中含关键词A+B
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


# 查找"title"、"abstract"和"keywords"字段中的关键词，并将找到的关键词记录在新的列中
def filter1():
    for index, row in df.iterrows():
        if pd.notnull(row['Title']):
            title_ck = find_keywords(row['Title'], context_keywords, techniques_keywords)
            if title_ck:
                df.at[index, 'TITLE_CK'] = title_ck
        if pd.notnull(row['Abstract Note']):
            abstract_ck = find_keywords(row['Abstract Note'], context_keywords, techniques_keywords)
            if abstract_ck:
                df.at[index, 'ABSTRACT_CK'] = abstract_ck
        # 如果 'TITLE_CK', 'ABSTRACT_CK', 和 'KEYWORDS_CK'这三列都是空的，则在'NO_CK'列中填入'NO_CK'
        if df.loc[index, 'TITLE_CK'] == '' and df.loc[index, 'ABSTRACT_CK'] == '':
            df.loc[index, 'NO_CK'] = 'NO_CK'
        # 页数少于8，不含关键词的条目排除
        if df.loc[index, 'NO_CK'] == 'NO_CK':
            df.loc[index, 'EXCLUDE'] = 'EXCLUDE'

def filter2():
    for index, row in df.iterrows():
        if pd.notnull(row['Title']):
            title_ck = find_keywords2(row['Title'], techniques_keywords)
            if title_ck:
                df.at[index, 'TITLE_CK'] = title_ck
        if pd.notnull(row['Abstract Note']):
            abstract_ck = find_keywords2(row['Abstract Note'], techniques_keywords)
            if abstract_ck:
                df.at[index, 'ABSTRACT_CK'] = abstract_ck
        # 如果 'TITLE_CK', 'ABSTRACT_CK'都是空的，则在'NO_CK'列中填入'NO_CK'
        if df.loc[index, 'TITLE_CK'] == '' and df.loc[index, 'ABSTRACT_CK'] == '':
            df.loc[index, 'NO_CK'] = 'NO_CK'
        # 页数少于8，不含关键词的条目排除
        if df.loc[index, 'NO_CK'] == 'NO_CK':
            df.loc[index, 'EXCLUDE'] = 'EXCLUDE'


def find_year(text):
    if pd.isna(text):  # 如果文本是NaN（即空的），则返回None
        return None
    else:
        # 使用正则表达式查找所有的四位数字
        numbers = re.findall(r'\b\d{4}\b', text)
        # 如果没有找到四位数字，返回None
        if not numbers:
            return None
        # 如果找到了四位数字，返回其中最大的一个
        else:
            return max(int(number) for number in numbers)

#
# # 尝试将 'date' 列转换为 datetime 对象，无法转换的置为 NaT
# df['date'] = pd.to_datetime(df['date'], errors='coerce')
#
# # 创建一个新的日期对象
# date_threshold = pd.to_datetime('2017-01-01')
#
# # 在 'date' 早于阈值并且不是 NaT 的地方，在 'EXCLUDE' 列中添加 'YEAR'
# df.loc[(df['date'] < date_threshold) & (df['date'].notna()), 'EXCLUDE'] += 'YEAR'

filter2()

df = set_venue(df, 'Url', VENUES)
df = set_venue(df, 'Short Title', VENUES)
df = set_venue(df, 'DOI', VENUES)
df = set_venue(df, 'Abstract Note', VENUES)
df = set_venue(df, 'Publication Title', VENUES)
df = set_venue(df, 'Notes', VENUES)
df = set_venue(df, 'Series', VENUES)

# 将结果写入Excel的第一个表单
with pd.ExcelWriter(OUTPUT_XLSX, engine='openpyxl') as writer:
    df.to_excel(writer, index=False, sheet_name='All Entries')

    df_filtered = df[df['EXCLUDE'] == '']
    df_filtered.to_excel(writer, index=False, sheet_name='Filtered Entries')
    #
    # # 过滤出ICSE的条目
    # df_icse = df[((df['doi'].str.contains('ICSE', case=False, na=False, regex=False)) | (
    #     df['eventtitle'].str.contains('International Conference on Software Engineering', case=False, na=False,
    #                                   regex=False)) | (
    #                   df['booktitle'].str.contains('International Conference on Software Engineering', case=False,
    #                                                na=False, regex=False))) & (df['EXCLUDE'] == '')]
    # df_icse.to_excel(writer, index=False, sheet_name='ICSE Entries')
    #
    # # 过滤出FSE的条目
    # df_fse = df[((df['booktitle'].str.contains('Foundations of Software Engineering', case=False, na=False,
    #                                            regex=False)) | (
    #                  df['eventtitle'].str.contains('Foundations of Software Engineering', case=False, na=False,
    #                                                regex=False))) & (df['EXCLUDE'] == '')]
    # df_fse.to_excel(writer, index=False, sheet_name='FSE Entries')
    #
    # # 过滤出ISSTA的条目
    # df_issta = df[(df['eventtitle'].str.contains('International Symposium on Software Testing and Analysis', case=False,
    #                                              na=False, regex=False)) & (df['EXCLUDE'] == '')]
    # df_issta.to_excel(writer, index=False, sheet_name='ISSTA Entries')
    #
    # # 过滤出ASE的条目
    # df_ase = df[((df['journaltitle'].str.contains('Automated Software Engineering Conference', case=False, na=False,
    #                                               regex=False)) | (
    #     df['eventtitle'].str.contains('Automated Software Engineering Conference', case=False, na=False,
    #                                   regex=False))) & (df['EXCLUDE'] == '')]
    # df_ase.to_excel(writer, index=False, sheet_name='ASE Entries')
    #
    # # 过滤出TSE的条目
    # df_tse = df[(df['doi'].str.contains('TSE', case=False, na=False, regex=False))  & (df['EXCLUDE'] == '')]
    # df_tse.to_excel(writer, index=False, sheet_name='TSE Entries')
    #
    # # 过滤出TOSEM的条目
    # df_tosem = df[(df['journaltitle'].str.contains('Transactions on Software Engineering and Methodology', case=False,
    #                                                na=False, regex=False)) & (df['EXCLUDE'] == '')]
    # df_tosem.to_excel(writer, index=False, sheet_name='TOSEM Entries')
    #
    # # 过滤出TIFS的条目
    # df_tifs = df[(df['doi'].str.contains('TIFS', case=False, na=False, regex=False)) & (df['EXCLUDE'] == '')]
    # df_tifs.to_excel(writer, index=False, sheet_name='TIFS Entries')
    #
    # # 过滤出TSDC的条目
    # df_tsdc = df[(df['journaltitle'].str.contains('Transactions on Dependable and Secure Computing', case=False,
    #                                               na=False, regex=False)) & (df['EXCLUDE'] == '')]
    # df_tsdc.to_excel(writer, index=False, sheet_name='TSDC Entries')
