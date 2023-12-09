import os
import re
import numpy as np

def write_csv(dir_name, total_charge):
    with open('HCO3_charge.csv', '1') as w:
        w.write(dir_name+','+str(total_charge)+'\n')


def cif_read(cif_dirs_path):
    with open(cif_dirs_path, 'r') as f:
        line = f.readlines()
        fir_index = 0
        H_index = 0
        O_index = 0
        C_index = 0
        for i, rows in enumerate(line):
            if '_atom_site_type_symbol' in rows:
                fir_index = i
            if '模板.000000 H' in rows:
                H_index = i
            if '模板.000000 C' in rows:
                C_index = i
            if '模板.000000 O' in rows:
                O_index = i

            O1_index = O_index-2-fir_index
            O2_index = O_index-1-fir_index
            O3_index = O_index-fir_index
            H1_index = H_index-fir_index
            C1_index = C_index-fir_index
    return H1_index, C1_index, O1_index, O2_index, O3_index

def get_HCO3_charge(charge_path, H, C, O1, O2, O3):
    with open(charge_path, 'r') as f:
        line = f.readlines()
        H_index = H+1
        C_index = C+1
        O1_index = O1+1
        O2_index = O2+1
        O3_index = O3+1
        H_charge = np.float_(re.findall(r'-?\d+\.*\d*', line[H_index])[4])-1
        C_charge = np.float_(re.findall(r'-?\d+\.*\d*', line[C_index])[4])-4
        O1_charge = np.float_(re.findall(r'-?\d+\.*\d*', line[O1_index])[4])-6
        O2_charge = np.float_(re.findall(r'-?\d+\.*\d*', line[O2_index])[4])-6
        O3_charge = np.float_(re.findall(r'-?\d+\.*\d*', line[O3_index])[4])-6
        total_charge = H_charge+C_charge+O1_charge+O2_charge+O3_charge
    return total_charge

if __name__ == '__main__':
    cif_path = "C:\\Users\Wangy\Desktop\新建文件夹\cif"
    charge_path = "C:\\Users\Wangy\Desktop\新建文件夹\charge"
    dirs = os.listdir(cif_path)
    dirs.remove('desktop.ini')
    for dir in dirs:
        H, C, O1, O2, O3 = cif_read(cif_path+'\\'+dir)
        dir = dir.replace('.cif', '.dat')
        charge_num = get_HCO3_charge(charge_path+'\\'+dir, H, C, O1, O2, O3)
        write_csv(dir, charge_num)