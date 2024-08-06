import csv

filepath = "Science_Direct/Science_direct_analysis_2.csv"  # CSV文件路径

with open(filepath, 'r', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        #Software Engineering顶会
        if 'International Conference on Software Engineering' in row \
                or 'ICSE' in row:
            print('ICSE:',row)
        elif 'ACM SIGSOFT Symposium on the Foundations of Software Engineering' in row \
                or 'FSE' in row:
            print('FSE:',row)
        elif 'International Symposium on Software Testing and Analysis' in row \
                or 'ISSTA' in row:
            print('ISSTA:',row)
        elif 'Automated Software Engineering Conference' in row \
                or 'ASE' in row:
            print('ASE:',row)
        elif 'IEEE Transactions on Software Engineering' in row \
                or 'TSE' in row:
            print('TSE:',row)
        elif 'ACM Transactions on Software Engineering and Methodology' in row \
                or 'TOSEM' in row:
            print('TOSEM:',row)
        #Security顶会
        elif 'USENIX Security Symposium' in row \
                or 'Usenix Security' in row:
            print('Usenix Security:',row)
        elif 'ACM Conference on Computer and Communications Security' in row \
                or 'CCS' in row:
            print('CCS:',row)
        elif 'IEEE Symposium on Security and Privacy' in row \
                or 'S&P' in row:
            print('S&P:',row)
        elif 'Network and Distributed System Security Symposium' in row\
                or 'NDSS' in row:
            print('NDSS:',row)
        elif 'IEEE Transactions on Information Forensics and Security' in row \
                or 'TIFS' in row:
            print('TIFS:',row)
        elif 'IEEE Transactions on Dependable and Secure Computing' in row \
                or 'TSDC' in row:
            print('TSDC:',row)
