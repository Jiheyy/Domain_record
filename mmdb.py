# -*- coding: utf-8 -*-
import os
import csv
import datetime
from multiprocessing import Pool
# =============================================================================

AGENT_NAME = "mmdb_collector"
G_COMMON_LIB_VER = '0.0.0'
G_COMMON_LIB_DATE = '2021-01-14'
# by min(jh)
# =============================================================================
READ_FILE = "domain.csv"
RESULT_FILE = "test"
N_PROCESS = 7
# =============================================================================

query_options = ['NS', 'TXT', 'MX']
#AAAA, CNAME, PTR, SRV, SOA, CAA

csvof = open(RESULT_FILE, 'w', encoding='utf-8')
writer = csv.writer(csvof, delimiter='|', lineterminator='\n<<lt>>\n',quoting=csv.QUOTE_NONNUMERIC)


def find_mmdb(target) :
    new_data = []
    for query_option in query_options :
        cmd = 'dig '+ target +' '+ query_option
        print(cmd)
        output = os.popen(cmd).read()
        
        output = output.split('\n')
        for o in output:
            if ';' in o or len(o) <1 :
                continue
            data = o.split('\t')
            del data[1:3]
            new_data.append(data)
    return new_data


'''
def get_result(output) :
    new_data = []
    output = output.split('\n')
    for o in output:
        if ';' in o or len(o) < 1:
            continue
        data = o.split('\t')
        del data[1:3]
        new_data.append(data)
    #print(new_data)
    return new_data
'''


def get_target() :
    target = []
    f = open(READ_FILE, 'r')
    while True :
        line = f.readline()
        if not line : break
        target.append(line.replace('\n', ''))
    f.close()
    return target


if __name__ == "__main__":
    start_time = datetime.datetime.now()
    targets = get_target()

    new_data = []
    try: 
        pool = Pool(N_PROCESS)
        temp = pool.map(find_mmdb, targets)
        for r in temp:
            if r is None: continue
            writer.writerow(r)
        pool.close()
        pool.join()
    except Exception as ex:
        print(ex)
    finally:
        csvof.close()

    print(datetime.datetime.now()-start_time)
