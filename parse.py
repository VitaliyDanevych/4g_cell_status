import os
import re

__AUTHOR__ = 'Vitaliy Danevych'
__COPYRIGHT__ = 'Lifecell UA Company, 2018 Kiev, Ukraine'
__version__ = '0.4'
__license__ = "GPL"
__email__ = "oss_gxxx@lifexxx.cxx.ua"
__status__ = "Production"


def savetoFILE(out_file, header, list_my):
    with open(out_file, 'w+') as f:
        #f.write(header)
        f.write("\n")
        for each in list_my:
            f.write("%s" % each)
            f.write("\n")


def parseTXT(txtfile):
    """ TXT parser function """
    with open(txtfile, 'rt') as f:  ## open xml file for parsing
        sites = set()
        list_my = []
        cell_name = None
        adm_state = None
        oper_state = None
        #line_num = 0
        for line in f:
            #line_num +=1
            #cell name
            try:
                matched = re.search(r'^SubNetwork=ONRM_RootMo_R.+?EUtranCellFDD=([ERBS_]*?\w{2}\d{4}L\d{2})', line)
            except TypeError as e:
                print('TypeError occurs1', e)
            if matched:
                cell_name = matched.group(1)
                cell_name = cell_name.replace('ERBS_', '').strip()
                #print('cell_name: ', cell_name)

            #Adm state
            try:
                matched = re.search(r'^.*AdmState\):\s+(\d{1})$', line)
            except TypeError as e:
                print('TypeError occurs2', e)
            if matched:
                adm_state = matched.group(1).strip()
                if adm_state == '1':
                    adm_state = 'UNLOCKED'
                elif adm_state == '0':
                    adm_state = 'LOCKED'
                else:
                    adm_state = 'UNKNOWN'
                #print('adm_state: ', adm_state)

            #Oper State
            try:
                matched = re.search(r'^.*OperState\s+ro\):\s+(\d{1})$', line)
            except TypeError as e:
                print('TypeError occurs3', e)
            if matched:
                oper_state = matched.group(1).strip()
                if oper_state == '1':
                    oper_state = 'ENABLED'
                elif oper_state == '0':
                    oper_state = 'DISABLED'
                else:
                    oper_state = 'UNKNOWN'
                #print('oper_state: ', oper_state)

                #Make the whole line and add it to array
                if cell_name not in sites:
                    sites.add(cell_name)
                    if (cell_name is not None) and (adm_state is not None) and (oper_state is not None):
                        whole_line = cell_name + ';' + adm_state + ';' + oper_state
                        list_my.append(whole_line)
                        #if (cell_name == 'KI0085L11') or (cell_name == 'KI0417L13'):
                        #    print('line_num: ', line_num, ' whole_line: ', whole_line)

    return list_my


def main():
    in_file = '4g_cells_all.txt'
    out_file = '4g_cells_all.csv'
    abs_out_file = os.getcwd() + os.sep + out_file
    if os.name == 'posix':
        abs_in_file = '/home/fmuser2/scripts/4g_cell_status' + os.sep + in_file
    elif os.name == 'nt':
        abs_in_file = os.getcwd() + os.sep + 'in' + os.sep + in_file

    header = 'MO;AdmState;Op.State'  # csv file header for sqlloader

    try:
        list_my = parseTXT(abs_in_file)
    except TypeError as e:
        print('TypeError occurs', e)
        print('Exception!')

    savetoFILE(abs_out_file, header, list_my)


if __name__ == "__main__":
    main()
