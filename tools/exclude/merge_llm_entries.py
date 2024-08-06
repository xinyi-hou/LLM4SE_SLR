import pandas as pd

# 读取Excel文件
LLM_ENTRIES = 'filtered_excel/llm_entries.xlsx'
MERGE_LLM_ENTRIES = 'filtered_excel/merge_llm_entries.xlsx'

# 用pandas打开Excel文件
with pd.ExcelFile(LLM_ENTRIES) as xls:
    # 获取所有工作表名
    sheet_names = xls.sheet_names

    # 读取第一个工作表
    df = pd.read_excel(xls, sheet_names[0])

    # 对每个其他工作表
    for sheet_name in sheet_names[1:]:
        # 读取工作表
        df_temp = pd.read_excel(xls, sheet_name)
        # 合并工作表
        df = pd.concat([df, df_temp], ignore_index=True, sort=False)

# 将合并后的DataFrame保存到新的Excel文件中
with pd.ExcelWriter(MERGE_LLM_ENTRIES) as writer:
    df.to_excel(writer, index=False)
