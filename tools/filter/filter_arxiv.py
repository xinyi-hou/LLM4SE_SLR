import bibtexparser
import pandas as pd
import re
from FindVenues import *

# 定义文件路径
UNIQUE_BIB = '../remove_duplicates/no_duplicates/arxiv_unique.bib'
INPUT_XLSX = 'arxiv/SE4LLM.xlsx'
OUTPUT_XLSX = 'arxiv/SE4LLM_output.xlsx'
CONTEXT_KEYWORDS = '../handle_keywords/context_related.txt'
TECHNIQUES_KEYWORDS = '../handle_keywords/llm_related.txt'

# 读取BibTeX文件
with open(UNIQUE_BIB, 'r') as bib_file:
    bib_database = bibtexparser.load(bib_file)

# # 将BibTeX条目转化为pandas DataFrame
# df = pd.DataFrame(bib_database.entries)

df = pd.read_excel(INPUT_XLSX)

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


def filter1():
    # 查找"title"、"abstract"和"keywords"字段中的关键词，并将找到的关键词记录在新的列中
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
            # 如果 'TITLE_CK', 'ABSTRACT_CK', 和 'KEYWORDS_CK'这三列都是空的，则在'NO_CK'列中填入'NO_CK'
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
# # 应用 find_year 函数并在适当的情况下填写 'EXCLUDE'
# df['comment_year'] = df['comment'].apply(find_year)
# df['submit_year'] = df['submit'].apply(find_year)
#
# df.loc[((df['comment_year'] < 2017) & df['comment_year'].notna()) | ((df['submit_year'] < 2017) & df['submit_year'].notna()), 'EXCLUDE'] = 'YEAR'
#
# # 删除临时创建的列
# df = df.drop(columns=['comment_year', 'submit_year'])

filter1()

df = set_venue(df, 'Url', VENUES)
df = set_venue(df, 'Journal Abbreviation', VENUES)
df = set_venue(df, 'Publication Title', VENUES)
df = set_venue(df, 'Series', VENUES)
# df = set_venue_lower(df, 'ID', VENUES)


# 将结果写入Excel的第一个表单
with pd.ExcelWriter(OUTPUT_XLSX, engine='openpyxl') as writer:
    df.to_excel(writer, index=False, sheet_name='All Entries')

    df_filtered = df[df['EXCLUDE'] == '']
    df_filtered.to_excel(writer, index=False, sheet_name='Filtered Entries')

    # # 过滤出ICSE的条目
    # df_icse = df[((df['comment'].str.contains('ICSE', case=False, na=False, regex=False)) | (
    #     df['comment'].str.contains('International Conference on Software Engineering', case=False, na=False,
    #                                regex=False))) & (df['EXCLUDE'] == '')]
    # df_icse.to_excel(writer, index=False, sheet_name='ICSE Entries')
    #
    # # 过滤出FSE的条目
    # df_fse = df[((df['comment'].str.contains('FSE', case=False, na=False, regex=False)) | (
    #     df['comment'].str.contains('Foundations of Software Engineering', case=False, na=False,
    #                                regex=False))) & (df['EXCLUDE'] == '')]
    # df_fse.to_excel(writer, index=False, sheet_name='FSE Entries')
    #
    # # 过滤出ISSTA的条目
    # df_issta = df[((df['comment'].str.contains('ISSTA', case=False, na=False, regex=False)) | (
    #     df['comment'].str.contains('International Symposium on Software Testing and Analysis', case=False, na=False,
    #                                regex=False))) & (df['EXCLUDE'] == '')]
    # df_issta.to_excel(writer, index=False, sheet_name='ISSTA Entries')
    #
    # # 过滤出ASE的条目
    # df_ase = df[((df['comment'].str.contains('ASE', case=False, na=False, regex=False)) | (
    #     df['comment'].str.contains('Automated Software Engineering Conference', case=False, na=False,
    #                                regex=False))) & (df['EXCLUDE'] == '')]
    # df_ase.to_excel(writer, index=False, sheet_name='ASE Entries')
    #
    # # 过滤出TSE的条目
    # df_tse = df[((df['comment'].str.contains('TSE', case=False, na=False, regex=False)) | (
    #     df['comment'].str.contains('Transactions on Software Engineering', case=False, na=False,
    #                                regex=False))) & (df['EXCLUDE'] == '')]
    # df_tse.to_excel(writer, index=False, sheet_name='TSE Entries')
    #
    # # 过滤出TOSEM的条目
    # df_tosem = df[((df['comment'].str.contains('TOSEM', case=False, na=False, regex=False)) | (
    #     df['comment'].str.contains('Transactions on Software Engineering and Methodology', case=False, na=False,
    #                                regex=False))) & (df['EXCLUDE'] == '')]
    # df_tosem.to_excel(writer, index=False, sheet_name='TOSEM Entries')
    #
    # # 过滤出Usenix Security的条目
    # df_usenix = df[((df['comment'].str.contains('Usenix Security', case=False, na=False, regex=False)) | (
    #     df['comment'].str.contains('USENIX Security Symposium', case=False, na=False,
    #                                regex=False))) & (df['EXCLUDE'] == '')]
    # df_usenix.to_excel(writer, index=False, sheet_name='Usenix Security Entries')
    #
    # # 过滤出CCS的条目
    # df_ccs = df[((df['comment'].str.contains('CCS', case=False, na=False, regex=False)) | (
    #     df['comment'].str.contains('Conference on Computer and Communications Security', case=False, na=False,
    #                                regex=False))) & (df['EXCLUDE'] == '')]
    # df_ccs.to_excel(writer, index=False, sheet_name='CCS Entries')
    #
    # # 过滤出ICSE的条目
    # df_icse = df[((df['comment'].str.contains('ICSE', case=False, na=False, regex=False)) | (
    #     df['comment'].str.contains('International Conference on Software Engineering', case=False, na=False,
    #                                regex=False))) & (df['EXCLUDE'] == '')]
    # df_icse.to_excel(writer, index=False, sheet_name='ICSE Entries')
    #
    # # 过滤出S&P的条目
    # df_sp = df[((df['comment'].str.contains('SP', case=False, na=False, regex=False)) | (
    #     df['comment'].str.contains('Symposium on Security and Privacy', case=False, na=False,
    #                                regex=False))) & (df['EXCLUDE'] == '')]
    # df_sp.to_excel(writer, index=False, sheet_name='S&P Entries')
    #
    # # 过滤出NDSS的条目
    # df_ndss = df[((df['comment'].str.contains('NDSS', case=False, na=False, regex=False)) | (
    #     df['comment'].str.contains('Network and Distributed System Security Symposium', case=False, na=False,
    #                                regex=False))) & (df['EXCLUDE'] == '')]
    # df_ndss.to_excel(writer, index=False, sheet_name='NDSS Entries')
    #
    # # 过滤出TIFS的条目
    # df_tifs = df[((df['comment'].str.contains('TIFS', case=False, na=False, regex=False)) | (
    #     df['comment'].str.contains('Transactions on Information Forensics and Security', case=False, na=False,
    #                                regex=False))) & (df['EXCLUDE'] == '')]
    # df_tifs.to_excel(writer, index=False, sheet_name='TIFS Entries')
    #
    # # 过滤出TSDC的条目
    # df_tsdc = df[((df['comment'].str.contains('TSDC', case=False, na=False, regex=False)) | (
    #     df['comment'].str.contains('Transactions on Dependable and Secure Computing', case=False, na=False,
    #                                regex=False))) & (df['EXCLUDE'] == '')]
    # df_tsdc.to_excel(writer, index=False, sheet_name='TSDC Entries')
