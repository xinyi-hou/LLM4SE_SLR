import re
#import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
paths = [
            #"ACM/ACM",
            "Arxiv/Arxiv",
            #"dblp/dblp",
            #"IEEE/IEEE",
            #"Springer/springer",
            #"Science_Direct/Science_direct",
            #"WebofScience/webofscience"
        ]
usecols=[
            #"Key",
            "Item Type",
            "Publication Year",
            "Title",
            "Publication Title",
            #"ISBN",
            #"ISSN",
            "DOI",
            "Url",
            "Abstract Note",
            "Pages",
            "Manual Tags",
        ]
pattern = re.compile(r'[^\d-]')

A_ = [
    "Software Engineering" , "Software Development" , "Program" , "Software Testing",
    "Software Mainten" , "SE" , "Software Lifecycle" , "Software Design",
    "Code representation" , "Code generation" , "Code comment generation" , "Code search",
    "Code localization" , "Code completion" , "Code summarization" , "Method name generation",
    "Bug detection" , "Bug localization" , "Vulnerability detection" , "Testing techniques",
    "Test case generation" , "Program analysis" , "Bug classification" , "Defect prediction",
    "Program repair" , "Code clone detection" , "Bug report" , "Software quality evaluation",
    "SATD detection" , "Code smell detection" , "Compiled-related" , "Code review" ,
    "Software classification" , "Code classification" , "Code change" , "Incident detection",
    "Requirement extraction" , "Requirement traceability" , "Requirement validation" , "Effort cost prediction",
    "Mining GitHub" , "Github mining" , "Mining SO" , "SO mining",
    "Mining app" , "App mining" , "Mining tag" , "Tag mining",
    "Developer-based mining"
]

B_ = [
    "LLM" , "Large Language Model" , "Language Model" , "LM",
    "PLM" , "Pre-trained" , "Pre-training" , "Natural Language Processing",
    "NLP" , "Machine Learning" , "ML" , "Deep Learning",
    "DL" , "Artificial Intelligence" , "AI" , "Transformer",
    "BERT" , "CODEX" , "GPT" , "T5",
    "Sequence Model" , "Attention Model" , "Transfer Learning" , "Neural Network",
    "Deep neural network" , "DNN"
]
C_ = [
    "reliab",
    "robust",
    "secur",
    "bais",
]
for path in paths:
    # 读取CSV文件
    df = pd.read_csv(
        f"{path}_unique.csv",
        usecols=usecols,
        low_memory=False
    )

    # 缺失值设为NAN
    df['Is_Top_venues'] = np.nan
    df['Is_page_ge_8'] = np.nan
    df['Is_Exclude'] = 0
    df['Have_keywords_Reliability'] = ""
    df['Have_keywords_A'] = ""
    df['Have_keywords_B'] = ""
    # 判断Publication Title字段是否包含顶会
    for i in range(len(df)):
    ##Keywords
        abstract: str = df.loc[i, 'Abstract Note']
        keywords: str = df.loc[i, 'Manual Tags']
        title: str = df.loc[i, 'Title']
        search_keyword: str = str(abstract) + str(keywords) + str(title)
        for keyword in A_:
            if keyword in search_keyword:
                df.loc[i, 'Have_keywords_A'] += keyword + ','
        for keyword in B_:
            if keyword in search_keyword:
                df.loc[i, 'Have_keywords_B'] += keyword + ','
        for keyword in C_:
            if keyword in search_keyword.lower():
                df.loc[i, 'Have_keywords_Reliability'] += keyword + ','
        if not (len(df.loc[i, 'Have_keywords_A']) and len(df.loc[i, 'Have_keywords_B'])):
            df.loc[i, 'Is_Exclude'] = 1
    ##JOURNAL
        journal = df.loc[i, 'Publication Title']
        doi = df.loc[i, 'DOI']
        url = df.loc[i, 'Url']
        journal_doi_url = str(journal) + '.' + str(doi) + '.' + str(url)

        if pd.isna(doi) and pd.isna(journal) and pd.isna(url):
            df.loc[i, 'Is_Top_venues'] = 'NAN'
        # Software Engineering顶会
        elif 'International Conference on Software Engineering' in journal_doi_url \
                or 'ICSE' in journal_doi_url:
            df.loc[i, 'Is_Top_venues'] = 'ICSE'
        elif 'ACM SIGSOFT Symposium on the Foundations of Software Engineering' in journal_doi_url \
                or 'FSE' in journal_doi_url:
            df.loc[i, 'Is_Top_venues'] = 'FSE'
        elif 'International Symposium on Software Testing and Analysis' in journal_doi_url \
                or 'ISSTA' in journal_doi_url:
            df.loc[i, 'Is_Top_venues'] = 'ISSTA'
        elif 'Automated Software Engineering Conference' in journal_doi_url \
                or 'ASE' in journal_doi_url:
            df.loc[i, 'Is_Top_venues'] = 'ASE'
        elif 'IEEE Transactions on Software Engineering' in journal_doi_url \
                or 'TSE' in journal_doi_url:
            df.loc[i, 'Is_Top_venues'] = 'TSE'
        elif 'ACM Transactions on Software Engineering and Methodology' in journal_doi_url \
                or 'TOSEM' in journal_doi_url:
            df.loc[i, 'Is_Top_venues'] = 'TOSEM'
        # Security顶会
        elif 'USENIX Security Symposium' in journal_doi_url \
                or 'Usenix Security' in journal_doi_url:
            df.loc[i, 'Is_Top_venues'] = 'Usenix Security'
        elif 'ACM Conference on Computer and Communications Security' in journal_doi_url \
                or 'CCS' in journal_doi_url:
            df.loc[i, 'Is_Top_venues'] = 'CCS'
        elif 'IEEE Symposium on Security and Privacy' in journal_doi_url \
                or 'S&P' in journal_doi_url:
            df.loc[i, 'Is_Top_venues'] = 'S&P'
        elif 'Network and Distributed System Security Symposium' in journal_doi_url \
                or 'NDSS' in journal_doi_url:
            df.loc[i, 'Is_Top_venues'] = 'NDSS'
        elif 'IEEE Transactions on Information Forensics and Security' in journal_doi_url \
                or 'TIFS' in journal_doi_url:
            df.loc[i, 'Is_Top_venues'] = 'TIFS'
        elif 'IEEE Transactions on Dependable and Secure Computing' in journal_doi_url \
                or 'TSDC' in journal_doi_url:
            df.loc[i, 'Is_Top_venues'] = 'TSDC'
        elif path != "Arxiv/Arxiv":
            df.loc[i, 'Is_Top_venues'] = 'NOT TOP VENUES'
            df.loc[i, 'Is_Exclude'] = 1


        if path == "Arxiv/Arxiv":
            continue
    ##Page_number
        page_number = df.loc[i, 'Pages']
        page = str(page_number).replace('–', '-').replace('P', '').replace('3C.3-', '')

        if pd.isna(page_number) or pattern.search(page):
            df.loc[i, 'Is_page_ge_8'] = 'NAN'
        else:
            temp = page.split('-')
            if len(temp) == 1 or temp[1] == "":
                res = int(temp[0])
            else:
                res = int(temp[1]) - int(temp[0]) + 1
            if 500 > res >= 8:
                df.loc[i,'Is_page_ge_8'] = str(res)
            elif res >= 500:
                df.loc[i, 'Is_page_ge_8'] = f'页码:{res}'
            else:
                df.loc[i, 'Is_page_ge_8'] = 'lower than 8 pages'
                df.loc[i,'Is_Exclude'] = 1

    # 输出去重后的数据到新文件
    df.to_csv(path + '_analysis_2.csv', index=False)
    result1 = df[(df['Item Type'] != 'patent')
                & (df['Item Type'] != 'book')
                & (df['Item Type'] != 'thesis')
                & (df['Is_Exclude'] == 0)]
    result1.to_csv(path + '_analysis_2_remained.csv', index=False)
    result2 = result1[result1['Have_keywords_Reliability'] != ""]
    result2.to_csv(path + '_analysis_3.csv', index=False)

    # 输出完成信息
    print(f'已将结果保存至./{path}')