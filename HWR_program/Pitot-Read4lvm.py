# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 18:58:51 2019

@author: yuich
"""

#############################################################
#
#   【校正データ用】 Labview形式のlvmファイル読み込み用プログラム
#
#                                   June.,20th,2019 Y.Watanabe
#############################################################

from lvm_read import read
import pandas as pd
import os, tkinter, tkinter.filedialog, tkinter.messagebox
import numpy as np

###### 変数入力 #####
DATA='20190618_pitot_main' #データ保存名

######　ファイル選択ダイアログの表示　#####
root = tkinter.Tk()
root.withdraw()
fTyp = [("","*.lvm")]
iDir = os.path.abspath(os.path.dirname(__file__))
tkinter.messagebox.showinfo('lvm形式ファイルための読み込みプログラム','処理を実施したいファイルを複数選択してください！')
file = tkinter.filedialog.askopenfilenames(filetypes = fTyp,initialdir = iDir)

#####　選択ファイルリスト作成　#####
list_tmp = list(file)
tkinter.messagebox.showinfo('lvm形式ファイルための読み込みプログラム',list_tmp)

count=0

for j in range(0,len(list_tmp)):
    filepath=list_tmp[j]
    basename = os.path.basename(filepath)
    lvm_file = read(filepath)
    
    if j==0:
        tmp =lvm_file[0]['data'][0,0:4] #辞書型からキーを選択してデータを抽出する
        u_true = np.sqrt(2*tmp[1] * 1000 / tmp[3]) # U = SQRT (2 x Pd / rho ) [Pa]　マノメータの換算には出力電圧を1000倍する
        tmp = np.append(tmp,u_true)
        ttmp=np.reshape(tmp,(5,1)).T #抽出後は1次配列となるため，変換して行列にする
        
        df_lvm = pd.DataFrame(ttmp,index=[basename])
                
    else:
        tmp =lvm_file[0]['data'][0,0:4] #辞書型からキーを選択してデータを抽出する
        u_true = np.sqrt(2*tmp[1] * 1000 / tmp[3])
        tmp = np.append(tmp,u_true)
        
        df_lvm.loc[basename]=(tmp)
        
    count += 1    
    print(count)    
    
##### チャンネル情報 #####
df_lvm.columns=['U [m/s]','Diff.press [Pa]','Temp.[degree]','rho [kg/m3]','U_true [m/s]']

##### データを保存する #####
df_lvm.to_pickle(DATA +'.pkl')