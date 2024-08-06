import bibtexparser

# 定义文件路径
ORIGINAL_BIB = 'original_bib/litmap.bib'
NO_DUPLICATES = 'no_duplicates/litmap_unique.bib'


def remove_duplicates_by_title(original_bib, no_duplicates):
    with open(original_bib, 'r') as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)

    print(f'Number of original BibTeX entries: {len(bib_database.entries)}')

    # 创建一个空集合，用于检测重复条目
    title_set = set()
    unique_entries = []

    for entry in bib_database.entries:
        title = entry['title']
        if title not in title_set:
            title_set.add(title)
            unique_entries.append(entry)

    # 创建一个新的 BibDatabase 对象，只包含非重复条目
    bib_database.entries = unique_entries

    with open(no_duplicates, 'w') as bibtex_file:
        bibtexparser.dump(bib_database, bibtex_file)

    print(f'Number of BibTeX entries after removing duplicates: {len(unique_entries)}')


# 使用脚本
remove_duplicates_by_title(ORIGINAL_BIB, NO_DUPLICATES)
