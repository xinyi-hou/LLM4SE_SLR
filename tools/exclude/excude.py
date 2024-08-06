import pandas as pd
import openpyxl
import re

# 定义文件路径
ALL_FILTERED = 'filtered_excel/all_filtered.xlsx'
UNIQUE_FILTERED = 'excluded_excel/unique_filtered.xlsx'
LLM_TOP_VENUES = 'filtered_excel/llm_top_venues.xlsx'
MERGE_LLM_ENTRIES = 'excluded_excel/merge_llm_title.xlsx'
CONTEXT_KEYWORDS = '../handle_keywords/context_related.txt'
TECHNIQUES_KEYWORDS = '../handle_keywords/llm_related.txt'
VENUES = 'venues.xlsx'

# 读取excel文件
df = pd.read_excel(ALL_FILTERED)
df_llm = pd.read_excel(LLM_TOP_VENUES)
df_merge = pd.read_excel(MERGE_LLM_ENTRIES)

df['Journal Title'] = ''
df['Book Title'] = ''
df['Event Title'] = ''
df['Submit'] = ''
df['Comment'] = ''
df['Keywords'] = ''
df['SAME_TITLE'] = ''
df['SOURCE'] = ''
df['TITLE_CK'] = ""  # title中含关键词A+B
df['ABSTRACT_CK'] = ""  # abstract中含关键词A+B
df['KEYWORDS_CK'] = ""  # keywords中含关键词A+B
df['NO_CK'] = ""  # 不含关键词A+B
df['VENUE'] = ''  # 会议期刊
df['RANK'] = ''  # 会议期刊

# 将标题转化为小写，并查找重复的条目
duplicate_mask = df['Title'].str.lower().duplicated(keep='first')
# 对于重复的条目，在"SAME_TITLE"列中填入"SAME_TITLE"
df.loc[duplicate_mask, 'SAME_TITLE'] = 'SAME_TITLE'

df.loc[df['Item Type'].str.contains('thesis', case=False, na=False, regex=False), 'SOURCE'] = 'PhD Thesis'
df.loc[df['Item Type'].str.contains('book', case=False, na=False, regex=False), 'SOURCE'] = 'book'
df.loc[df['Item Type'].str.contains('book', case=False, na=False, regex=False), 'SOURCE'] = 'bookSection'

# 将标题列转换为小写以进行大小写敏感匹配
df['Title'] = df['Title'].str.lower()
df_llm['title'] = df_llm['title'].str.lower()
# df_merge['title'] = df_merge['title'].str.lower

# 对每一个标题在LLM_TOP_VENUES中进行搜索
for index, row in df.iterrows():
    venue = df_llm[df_llm['title'] == row['Title']]['top venue'].values
    if len(venue) > 0:
        df.at[index, 'VENUE'] = venue[0]

for index, row in df.iterrows():
    abstract = df_merge[df_merge['title'] == row['Title']]['abstract'].values
    keywords = df_merge[df_merge['title'] == row['Title']]['keywords'].values
    pages = df_merge[df_merge['title'] == row['Title']]['pages'].values
    series = df_merge[df_merge['title'] == row['Title']]['series'].values
    journaltitle = df_merge[df_merge['title'] == row['Title']]['journaltitle'].values
    booktitle = df_merge[df_merge['title'] == row['Title']]['booktitle'].values
    eventtitle = df_merge[df_merge['title'] == row['Title']]['eventtitle'].values
    submit = df_merge[df_merge['title'] == row['Title']]['submit'].values
    comment = df_merge[df_merge['title'] == row['Title']]['comment'].values
    publishers = df_merge[df_merge['title'] == row['Title']]['PUBLISHERS'].values
    if len(abstract) > 0:
        df.at[index, 'Abstract Note'] = abstract[0]
    if len(keywords) > 0:
        df.at[index, 'Keywords'] = keywords[0]
    if len(pages) > 0:
        df.at[index, 'Pages'] = pages[0]
    if len(journaltitle) > 0:
        df.at[index, 'Journal Title'] = journaltitle[0]
    if len(booktitle) > 0:
        df.at[index, 'Book Title'] = booktitle[0]
    if len(eventtitle) > 0:
        df.at[index, 'Event Title'] = eventtitle[0]
    if len(submit) > 0:
        df.at[index, 'Submit'] = submit[0]
    if len(comment) > 0:
        df.at[index, 'Comment'] = comment[0]
    if len(publishers) > 0:
        df.at[index, 'Publisher'] = publishers[0]


# 读取关键词列表
with open(CONTEXT_KEYWORDS, 'r') as file:
    context_keywords = [r'\b' + line.strip() + r'\b' for line in file]
with open(TECHNIQUES_KEYWORDS, 'r') as file:
    techniques_keywords = [r'\b' + line.strip() + r'\b' for line in file]


# 创建函数用于查找关键词
def find_keywords(text, c_keywords, t_keywords):
    found_context_keywords = [keyword for keyword in c_keywords if re.search(keyword, text, re.IGNORECASE)]
    found_techniques_keywords = [keyword for keyword in t_keywords if re.search(keyword, text, re.IGNORECASE)]
    if found_context_keywords and found_techniques_keywords:
        return ', '.join(found_context_keywords + found_techniques_keywords).replace(r'\b', '')
    else:
        return ''


def set_venue(df1, column, venue_file):
    # 读取Excel文件
    df_venues = pd.read_excel(venue_file)

    # 在原df添加'VENUE'和'RANK'列
    if 'VENUE' not in df1.columns:
        df1['VENUE'] = ''
    if 'RANK' not in df1.columns:
        df1['RANK'] = ''

    # 遍历每一行
    for i, row1 in df1.iterrows():
        # 如果这一行的column列的值为空，则跳过这一行
        if pd.isna(row1[column]):
            continue

        # 确保列值为字符串类型
        column_value = str(row1[column])

        # 检查'VENUE'列是否已有值，如果有，查找其对应的rank并填入
        if df1.at[i, 'VENUE']:
            venue = df1.at[i, 'VENUE']
            rank_row = df_venues[df_venues['Abbreviation'] == venue]
            if not rank_row.empty:
                df1.at[i, 'RANK'] = str(rank_row['Rank'].values[0])
            continue

        # 遍历每个会议期刊名称和其缩写
        for j, venue_row in df_venues.iterrows():
            full_name = str(venue_row['Full Name'])
            abbr = str(venue_row['Abbreviation'])
            rank = str(venue_row['Rank'])
            # 如果会议期刊全称或缩写在这一行的column列的值中
            if full_name in column_value or abbr in column_value:
                # 将会议期刊缩写写入'VENUE'列，将rank写入'RANK'列
                df1.at[i, 'VENUE'] = abbr
                df1.at[i, 'RANK'] = rank
                # 找到匹配项后停止内部循环
                break
    return df1


df = set_venue(df, 'Publication Title', VENUES)
df = set_venue(df, 'DOI', VENUES)
df = set_venue(df, 'Journal Abbreviation', VENUES)
df = set_venue(df, 'Series', VENUES)
df = set_venue(df, 'Conference Name', VENUES)
df = set_venue(df, 'Journal Title', VENUES)
df = set_venue(df, 'Book Title', VENUES)
df = set_venue(df, 'Event Title', VENUES)
df = set_venue(df, 'Submit', VENUES)
df = set_venue(df, 'Comment', VENUES)
df = set_venue(df, 'Abstract Note', VENUES)


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
    if pd.notnull(row['Keywords']):
        keywords_ck = find_keywords(row['Keywords'], context_keywords, techniques_keywords)
        if keywords_ck:
            df.at[index, 'KEYWORDS_CK'] = keywords_ck
    # 如果 'TITLE_CK', 'ABSTRACT_CK'这两列都是空的，则在'NO_CK'列中填入'NO_CK'
    if df.loc[index, 'TITLE_CK'] == '' and df.loc[index, 'ABSTRACT_CK'] == '' and df.loc[index, 'KEYWORDS_CK'] == '':
        df.loc[index, 'NO_CK'] = 'NO_CK'

# 保存到新的工作表单
with pd.ExcelWriter(UNIQUE_FILTERED, engine="openpyxl") as writer:
    df.to_excel(writer, index=False, sheet_name='All filtered')

    # 获取'SAME_TITLE'列为空的所有条目
    df_unique = df[df['SAME_TITLE'] == '']
    df_unique.to_excel(writer, index=False, sheet_name='Unique filtered')

    # 获取'SOURCE'列为空的所有条目
    df_source = df[(df['SOURCE'] == '') & (df['SAME_TITLE'] == '')]
    df_source.to_excel(writer, index=False, sheet_name='Source filtered')

    # 获取'VENUE'列不为空的所有条目
    df_venue = df[(df['VENUE'] != '') & (df['SOURCE'] == '') & (df['SAME_TITLE'] == '')]
    df_venue.to_excel(writer, index=False, sheet_name='Venue filtered')

    # 获取'VENUE'列为空的所有条目
    df_venue = df[(df['VENUE'] == '') & (df['SOURCE'] == '') & (df['SAME_TITLE'] == '')]
    df_venue.to_excel(writer, index=False, sheet_name='None Venue')


