import os
import re
import numpy as np

def write_csv(dir_name, CO2_angle, C_OH_distance, C_O_distance):
    with open('WorkFunction.csv', '1') as w:
        w.write(dir_name+',')
        w.write(str(CO2_angle)+',')
        w.write(str(C_OH_distance)+',')
        w.write(str(C_O_distance) + '\n')

class CO2_geometry():
    def __init__(self, dirs_path):
        self.dir_path = dirs_path+'\\'+dir

    # 获取CO2以及吸附位点的坐标信息
    def data_process(self):
        with open(self.dir_path, 'r') as f:
            line = f.readlines()
            las_index_list = []
            for i, rows in enumerate(line):
                if 'C                    0' in rows:
                    fir_index = i
                if 'O                    0' in rows:
                    las_index_list.append(i)
                if 'O                    -模板' in rows:
                    o_atom_of_oh_xyz = i

            C_atom_xyz = np.float_(re.findall(r'-?\d+\.*\d*', line[fir_index])[1:])
            O1_atom_xyz = np.float_(re.findall(r'-?\d+\.*\d*', line[las_index_list[0]])[1:])
            O2_atom_xyz = np.float_(re.findall(r'-?\d+\.*\d*', line[las_index_list[1]])[1:])
            O_atom_of_OH_xyz = np.float_(re.findall(r'-?\d+\.*\d*', line[o_atom_of_oh_xyz])[1:])

        return C_atom_xyz, O1_atom_xyz, O2_atom_xyz, O_atom_of_OH_xyz

    def CO2_angle(self):
        C_atom, O_atom1, O_atom2, _ = self.data_process()
        O1_C = np.asarray(O_atom1-C_atom)
        O2_C = np.asarray(O_atom2-C_atom)
        l_x = np.sqrt(O1_C.dot(O1_C))
        l_y = np.sqrt(O2_C.dot(O2_C))
        dian = O1_C.dot(O2_C)
        cos = dian / (l_x * l_y)
        angle = np.arccos(cos) * 180 / np.pi
        return angle
    # CO2的C原子与吸附位点O原子的距离
    def CO2_OH_distance(self):
        C_atom, _, _, O_atom_of_OH = self.data_process()
        C_O_distance = O_atom_of_OH-C_atom
        CO2_OH_distance = np.sqrt(sum(i**2 for i in C_O_distance))
        return CO2_OH_distance
    # CO2中C-O平均键长
    def CO_distance_of_CO2(self):
        C_atom, O_atom1, O_atom2, _ = self.data_process()
        C_O_distance1 = O_atom1-C_atom
        C_O_distance2 = O_atom2-C_atom
        CO_distance1 = np.sqrt(sum(i**2 for i in C_O_distance1))
        CO_distance2 = np.sqrt(sum(i ** 2 for i in C_O_distance2))
        a = [CO_distance1, CO_distance2]
        CO_distance = np.mean(a)
        return CO_distance


if __name__ == '__main__':
    dirs_path = "C:\\Users\Wangy\Desktop\新建文件夹"
    dirs = os.listdir(dirs_path)
    for dir in dirs:
        res = CO2_geometry(dirs_path)
        CO2_angle = res.CO2_angle()
        CO2_OH_distance = res.CO2_OH_distance()
        C_O_distance = res.CO_distance_of_CO2()
        write_csv(dir, CO2_angle, CO2_OH_distance, C_O_distance)