# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 11:50:35 2019

@author: yuich
"""

#############################################################
#
#   【校正データ用】 校正曲線作成用プログラム
#
#                                   June.,21st,2019 Y.Watanabe
#############################################################

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import r2_score
from scipy.optimize import curve_fit
import csv

##### グラフスタイル #####
sns.set_style('whitegrid')  
plt.rcParams['font.family'] ='sans-serif'#使用するフォント
plt.rcParams['xtick.direction'] = 'in'#x軸の目盛線が内向き('in')か外向き('out')か双方向か('inout')
plt.rcParams['ytick.direction'] = 'in'#y軸の目盛線が内向き('in')か外向き('out')か双方向か('inout')
plt.rcParams['xtick.major.width'] = 1.0#x軸主目盛り線の線幅
plt.rcParams['ytick.major.width'] = 1.0#y軸主目盛り線の線幅
plt.rcParams['font.size'] = 8 #フォントの大きさ
plt.rcParams['axes.linewidth'] = 1.0# 軸の線幅edge

#### 変数入力 #####
file_path1='calib_20190618_U_Elin.pkl'
file_path2='20190618_main-calib.pickle'
file_path3='20190618_pitot.pickle'

Graph_Title1='E.org vs U'
DATA_1='Uvel_in_Y_direction_150mm'
DATA_2='Uvel_in_Y_direction_200mm'

#csv_file = open("traverse_v02.csv", "r", encoding="ms932", errors="", newline="" )
#f = csv.reader(csv_file, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)
#
##header = next(f)
##print(header)
#for row in f:
#    #rowはList
#    #row[0]で必要な項目を取得することができる
#    print(row)

csv_input = pd.read_csv("traverse_v02.csv", encoding="ms932", sep=",")

#### pickle読み込み #####
df_calib=pd.read_pickle(file_path1)
df_hwr=pd.read_pickle(file_path2)
df_pitot=pd.read_pickle(file_path3)

#### 本計測データを補正する #####
E_lin  = ((df_hwr.iloc[:,0] - df_calib['a'] ) / df_calib['b']) ** df_calib['m']
tmp = df_calib['int']+df_calib['sl']*E_lin[:]
E_lin = np.reshape(tmp,(len(df_hwr),1))

plt.figure()
plt.scatter(csv_input.iloc[0:28,2],E_lin[0:28])
plt.xlim((-150,150))
plt.ylim((25,33))
plt.xlabel('y [mm]')
plt.ylabel('U [m/s]')
plt.savefig(DATA_1 + '.png')

plt.figure()
plt.scatter(csv_input.iloc[29:56,2],E_lin[29:56])
plt.xlim((-150,150))
plt.ylim((25,33))
plt.xlabel('y [mm]')
plt.ylabel('U [m/s]')
plt.savefig(DATA_2 + '.png')