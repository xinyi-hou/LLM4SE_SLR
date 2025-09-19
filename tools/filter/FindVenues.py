import pandas as pd
import re

VENUES = 'venues.xlsx'


def set_venue(df1, column, venue_file):
    # 对参数进行类型转换
    column = str(column)
    venue_file = str(venue_file)

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


def set_venue_lower(df1, column, venue_file):
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

        # 确保列值为字符串类型，并转换为小写
        column_value = str(row1[column]).lower()

        # 检查'VENUE'列是否已有值，如果有，查找其对应的rank并填入
        if df1.at[i, 'VENUE']:
            venue = df1.at[i, 'VENUE']
            rank_row = df_venues[df_venues['Abbreviation'].str.lower() == venue.lower()]
            if not rank_row.empty:
                df1.at[i, 'RANK'] = str(rank_row['Rank'].values[0])
            continue

        # 遍历每个会议期刊名称和其缩写
        for j, venue_row in df_venues.iterrows():
            full_name = str(venue_row['Full Name']).lower()
            abbr = str(venue_row['Abbreviation']).lower()
            rank = str(venue_row['Rank'])
            # 如果会议期刊全称或缩写在这一行的column列的值中
            if full_name in column_value or abbr in column_value:
                # 将会议期刊缩写写入'VENUE'列，将rank写入'RANK'列
                df1.at[i, 'VENUE'] = abbr
                df1.at[i, 'RANK'] = rank
                # 找到匹配项后停止内部循环
                break
    return df1


# 创建函数用于查找关键词
def find_keywords(text, c_keywords, t_keywords):
    found_context_keywords = [keyword for keyword in c_keywords if re.search(keyword, text, re.IGNORECASE)]
    found_techniques_keywords = [keyword for keyword in t_keywords if re.search(keyword, text, re.IGNORECASE)]
    if found_context_keywords and found_techniques_keywords:
        return ', '.join(found_context_keywords + found_techniques_keywords).replace(r'\b', '')
    else:
        return ''


# 创建函数用于查找关键词2
def find_keywords2(text, t_keywords):
    found_techniques_keywords = [keyword for keyword in t_keywords if re.search(keyword, text, re.IGNORECASE)]
    if found_techniques_keywords:
        return ', '.join(found_techniques_keywords).replace(r'\b', '')
    else:
        return ''