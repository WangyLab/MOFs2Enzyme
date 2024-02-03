import os
import numpy
import re
import csv
from scipy.special import wofz
import pandas as pd
import matplotlib.pyplot as plt

path = "aaa"
dirs = os.listdir(path)
for dir in dirs:
    with open(path+'\\'+dir, 'r') as f:
        lines = f.readlines()
        freq = []
        IR = []
        Raman = []
        for line in lines:
            if 'Frequencies' in line:
                x = re.findall(r'-?\d+\.*\d*', line)
                for i in x:
                    freq.append(float(i))

            if 'IR Inten' in line:
                x = re.findall(r'-?\d+\.*\d*', line)
                for i in x:
                    IR.append(float(i))

            if 'Raman Activ' in line:
                x = re.findall(r'-?\d+\.*\d*', line)
                for i in x:
                    Raman.append(float(i))
    dir_name = dir.replace('.log', '')

    with open(path+'\\'+dir_name+'-IR.inp', 'w') as f:
        writer = csv.writer(f, delimiter='\t')
        header = [len(freq), 1]
        writer.writerow(header)
        writer.writerows(zip(freq, IR))

    with open(path+'\\'+dir_name+'-Raman.inp', 'w') as f:
        writer = csv.writer(f, delimiter='\t')
        header = [len(freq), 1]
        writer.writerow(header)
        writer.writerows(zip(freq, Raman))

def Gauss(x, A, xc, sigma):
    y = A / (sigma * np.sqrt(2 * np.pi)) * np.exp(-(x - xc) ** 2 / (2 * sigma ** 2))
    return y


def Lorentz(x, A, xc, sigma):
    y = (A / np.pi) * (sigma / ((x - xc) ** 2 + sigma ** 2))
    return y


def Voigt(x, y0, amp, pos, fwhm, shape=1):
    tmp = 1 / wofz(np.zeros((len(x))) + 1j * np.sqrt(np.log(2.0)) * shape).real
    return y0 + tmp * amp * wofz(2 * np.sqrt(np.log(2.0)) * (x - pos) / fwhm + 1j * np.sqrt(np.log(2.0)) * shape).real


class SpecBroadener():
    def __init__(self, inp_path, spec_lenth, broaden_factor, mode='Raman', make_noise=False, bias=False) -> None:
        self.path = inp_path
        self.name = inp_path.split('.')[0]
        aaa = pd.read_csv(self.path, delimiter='\t')
        self.n_mode = int(aaa.columns.values[0])
        self.shape = int(aaa.columns.values[1])
        self.freq = list(aaa[f'{self.n_mode}'])
        self.inti = list(aaa[f'{self.shape}'])
        self.spec_length = spec_lenth
        self.mode = mode
        self.bias = bias
        self.make_noise = make_noise
        self.fwhm = broaden_factor
        self.x, self.y = self._form_data()

        # self.noise = self._get_noise()

    def _Voigt(self, x, y0, amp, pos, fwhm, shape=1):
        tmp = 1 / wofz(np.zeros((len(x))) + 1j * np.sqrt(np.log(2.0)) * shape).real
        return y0 + tmp * amp * wofz(
            2 * np.sqrt(np.log(2.0)) * (x - pos) / fwhm + 1j * np.sqrt(np.log(2.0)) * shape).real

    def _form_data(self):
        x = np.array([i for i in range(self.spec_length)])
        y0 = np.array([0.0 for _ in range(self.spec_length)])
        yf = y0
        for n in range(self.n_mode):
            if self.bias:
                y = self._Voigt(x, y0, self.inti[n], self.freq[n] * np.random.choice([0.01 * i for i in range(80, 90)]),
                                self.fwhm)
            else:
                y = self._Voigt(x, y0, self.inti[n], self.freq[n], self.fwhm)
            yf = yf + y
        if self.make_noise:
            self._get_noise()
            if self.mode == 'Raman':
                yf = yf + self.noise
            elif self.mode == 'IR':
                yf = yf + 0.1 * self.noise
        return x, yf

    def _get_noise(self):
        noi_num = np.random.randint(6, 12)
        noi_freq = list(np.random.rand(noi_num) * 1000)
        noi_inti = list(np.random.rand(noi_num) * 2)
        x = np.array([i for i in range(self.spec_length)])
        noi0 = np.array([0.0 for _ in range(self.spec_length)])
        for n in range(noi_num):
            noi = self._Voigt(x, noi0, noi_inti[n], noi_freq[n], 20)
            noi0 = noi0 + noi
        self.noise = noi0

    def draw_pict(self):
        # x, y = self._form_data()
        plt.plot(self.x, self.y)
        plt.savefig(f'{self.name}.png')
        plt.cla()

    def save_data(self):
        # x, y = self._form_data()
        with open(f'{self.name}.txt', '1') as f:
            for i in range(len(self.x)):
                f.writelines(str(self.x[i]) + ',' + str(self.y[i]) + '\n')


if __name__ == '__main__':
    path = "aaa"
    dirs = os.listdir(path)
    for dir in dirs:
        # print(dir)
        if 'IR.inp' in dir:
            xxx = SpecBroadener(path+'\\'+dir, length, factor, mode='IR',
                                make_noise=False, bias=False)
            xxx.draw_pict()
            xxx.save_data()
        if 'Raman.inp' in dir:
            yyy = SpecBroadener(path+'\\'+dir, length, factor, mode='Raman',
                                make_noise=False, bias=False)
            yyy.draw_pict()
            yyy.save_data()
