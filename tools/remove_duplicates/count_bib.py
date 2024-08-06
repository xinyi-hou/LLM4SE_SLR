import bibtexparser


def count_entries_in_bib(file_path):
    with open(file_path, 'r') as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)

    print(f'Number of BibTeX entries in {file_path}: {len(bib_database.entries)}')


count_entries_in_bib('no_duplicates/LLM_SLR_unique.bib')

