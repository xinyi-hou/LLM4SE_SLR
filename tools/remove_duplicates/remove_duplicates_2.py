import bibtexparser
import os

# 定义文件路径
ORIGINAL_BIB_DIR = '/Users/ashley/Downloads/litmap'
NO_DUPLICATES = 'no_duplicates/litmap_unique.bib'

def remove_duplicates_by_title(original_bib_dir, no_duplicates):
    # 创建一个空的 BibDatabase 对象，用于保存所有的 BibTeX 条目
    bib_database = bibtexparser.bibdatabase.BibDatabase()

    # 遍历 original_bib_dir 下的所有 .bib 文件
    for filename in os.listdir(original_bib_dir):
        if filename.endswith('.bib'):
            try:
                with open(os.path.join(original_bib_dir, filename), 'r') as bibtex_file:
                    bib_db = bibtexparser.load(bibtex_file)
                    bib_database.entries.extend(bib_db.entries)
                print(f'Number of entries in {filename}: {len(bib_db.entries)}')
            except:
                print(f'Warning: Failed to parse {filename}. Skipping this file.')

    # 创建一个空集合，用于检测重复条目
    title_set = set()
    unique_entries = []

    for entry in bib_database.entries:
        try:
            title = entry['title']
            if title not in title_set:
                title_set.add(title)
                unique_entries.append(entry)
        except KeyError:
            print(f'Warning: No title field in a BibTeX entry. Skipping this entry.')

    # 创建一个新的 BibDatabase 对象，只包含非重复条目
    bib_database.entries = unique_entries

    with open(no_duplicates, 'w') as bibtex_file:
        bibtexparser.dump(bib_database, bibtex_file)

    print(f'Number of BibTeX entries after removing duplicates: {len(unique_entries)}')


# 使用脚本
remove_duplicates_by_title(ORIGINAL_BIB_DIR, NO_DUPLICATES)
