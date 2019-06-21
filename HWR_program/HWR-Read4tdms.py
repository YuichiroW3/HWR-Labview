# -*- coding: utf-8 -*-
"""
Created on Thu Sep 20 09:45:35 2018

@author: yuich
"""
#############################################################
#
#   【校正データ用】 Labview形式のtdmsファイル読み込み用プログラム
#
#                                   June.,20th,2019 Y.Watanabe
#############################################################

from nptdms import TdmsFile
import pandas as pd
import os, tkinter, tkinter.filedialog, tkinter.messagebox
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

##### グラフスタイル #####
sns.set_style('whitegrid')

###### 変数入力 #####
DATA='20190618_main-calib' #データ保存名
NAME='名称未設定' #TDMSファイルのタブ名
VULE1='電圧_0'    #チャンネル名
VULE2='電圧_1'

dt=2E-5 #時間刻み
list_t=1000000 #データ点数

######　ファイル選択ダイアログの表示　#####
root = tkinter.Tk()
root.withdraw()
fTyp = [("","*.tdms")]
iDir = os.path.abspath(os.path.dirname(__file__))
tkinter.messagebox.showinfo('tdms形式ファイルための読み込みプログラム','処理を実施したいファイルを複数選択してください！')
file = tkinter.filedialog.askopenfilenames(filetypes = fTyp,initialdir = iDir)

#####　選択ファイルリスト作成　#####
list_tmp = list(file)
tkinter.messagebox.showinfo('tdms形式ファイルための読み込みプログラム',list_tmp)

dt_dict=np.empty(list_t)
for jj in range(0,list_t):
    dt_dict[jj]=dt * jj

count=0
df_dict_all={}
df_mean=[]
   
for j in range(0,len(list_tmp)):
    filepath=list_tmp[j]
    basename = os.path.basename(filepath)
    tdms_file = TdmsFile(filepath)

    ch_1_1 = tdms_file.object(NAME, VULE1)
    ch_1_2 = tdms_file.object(NAME, VULE2)

    data_1_1 = ch_1_1.data
    data_1_2 = ch_1_2.data

    list_ch=[dt_dict,data_1_1,data_1_2]
    
    df_dict= {}

    ii=0
    
    ###### 平均化処理 #####
    mean1=np.mean(list_ch[1])
    mean2=np.mean(list_ch[2])
    
    if j==0:
        
        df_mean = pd.DataFrame([[mean1,mean2]],index=[basename])
        
    else:
        df_mean.loc[basename]=mean1,mean2
        
    ##### 辞書型にしてデータを格納する ######         
    df_dict[ii] = pd.DataFrame({'Time' : list_ch[0],
                                'Ch_1' : list_ch[1],
                                'Ch_2' : list_ch[2]})
      
    ii=ii+1 
             
    count += 1    
    print(count)
    ##### df_dict_allにすべてのデータが格納される #####
    df_dict_all[j]=df_dict
    
##### tdms形式のファイルからの読み込み終了 #####
    
##### チャンネル名を埋め込む #####    
df_mean.columns=['Ch_1','Ch_2']

##### データを保存する #####
df_mean.to_pickle(DATA +'.pkl')
df_dict_all.to_pickle('org_' + DATA + '.pkl')

##### グラフ化 #####
y=df_mean.iloc[:,1]
df_mean.plot( y=['Ch_1','Ch_2'])

plt.savefig(DATA + '.png')

#y=df_dict_all[0][0]
#pyplot.plot(y[['Ch_1']])
##pyplot.plot(y[['Ch_2']])

###### FFT分析　#####
#Fs=1/dt
#L=len(data_1_1)
#
#Y=sp.fftpack.fft(data_1_1,L)/L
#f=(Fs/L)*sp.arange(L/2 + 1)
#
#
#pyplot.plot(f,2*abs(Y[:L//2 + 1]))
#pyplot.yscale('log')