from ensurepip import version
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import kurtosis, skew, entropy 
import os

# https://github.com/andrews0/MMIC-PPG/blob/master/sketch.py 
# Andrew Shin 
# June 2022


# the main function
def clean(dir_name):
    """
    void func that takes each .npz file and separates em into good and bad csv files in 
    their respective dirs, using sqi

    Parameters
    ----------
    file_name : str
        name of folder containing .npz files
    """

    dir = '/Users/andrew/Documents/ML/ppg-process/vsqi/' + dir_name
    npz_list = [x for x in os.listdir(dir) if '.npz' in x]

    # for each .npz file

    for file in npz_list[37:4000:2700]:   # GET RID OF [::] LATER !!!!!!!!!!!!!!!!!!!
        # .npz file -> pd dataframe
        arr = np.load('PPG30min/' + file)['ppg']
        df = pd.DataFrame({'pleth':arr, 'timestamp':list(range(0, 1800000, 8)), 
            'sqi_s':[-1000]*225000, 'sqi_p':[-1000]*225000, 'sqi_k':[-1000]*225000})   # stamps by milisecond

        #create 2 piles for sending each chunk 
        df_good = pd.DataFrame({'pleth':[], 'timestamp':[], 'sqi_s':[], 'sqi_p':[], 'sqi_k':[]})
        df_bad = pd.DataFrame({'pleth':[], 'timestamp':[], 'sqi_s':[], 'sqi_p':[], 'sqi_k':[]})
        print('----------------------------')
        # for each 30 sec chunk of df
        window = 5 * 125
        for ii in range(0, 225000, window):
            smoll_df = df.iloc[ii:ii+window]
            # getting rid of portions with flat values; 
            # for each 1 sec segment, if constant: send to bad and drop from good pile
            for kk in range(ii, ii+window, 125):
                temp = df.iloc[kk:kk+125]
                if abs(temp['pleth'].max() - temp['pleth'].min()) < 0.005:
                    df_bad = pd.concat([df_bad, temp])
                    smoll_df = smoll_df.drop(list(range(kk, kk+125)))
                    
            # calc the 3 SQIs for smoll_df
            print(skew(smoll_df['pleth'], bias=False), skew(smoll_df['pleth'], bias=True))



            if '2 out of 3 sqi reaches their thresholds':
                df_good = pd.concat([df_good, smoll_df])
            else:
                df_bad = pd.concat([df_bad, smoll_df])
        
        # save good and bad df's to their respective folders, using to_csv
        # df_good.to_csv('ppg_good/' + file[:-4] + '.csv')
        # df_bad.to_csv('ppg_bad/' + file[:-4] + '.csv') 


        
        
        





clean('PPG30min')

# plotting:
    # plt.figure(figsize=(14.5, 7.5))
    # plt.scatter(df['timestamp'][10000:11000], df['pleth'][10000:11000])
    # plt.title(file + ' ')
    # plt.show() 