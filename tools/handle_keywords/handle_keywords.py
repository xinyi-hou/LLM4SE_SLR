# 按行分割的关键词列列表
KEYWORDS_LIST = "llm_related.txt"
OUTPUT = "handle_llm_related_ieee2.txt"

# 从KEYWORDS_LIST读取关键词并生成新的关键词形式
with open(KEYWORDS_LIST, "r") as file:
    lines = file.readlines()

new_keywords = " OR ".join(f'"Abstract":"{line.strip()}"' for line in lines)

# 将新的关键词形式写入新文件OUTPUT
with open(OUTPUT, "w") as file:
    file.write(new_keywords)
