from pyedflib import highlevel
from wfdb import rdsamp, wrsamp
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import os
import glob
from mysqi.common import utils
from mysqi.common.utils import generate_timestamp
from mysqi.data.signal_sqi_class import SignalSQI
import mysqi.highlevel_functions.highlevel as sqi_hl 

# https://github.com/andrews0/MMIC-PPG/blob/master/sketch.py 


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
    for file in npz_list[37:4000:738]:   # GET RID OF [:] LATER !!!!!!!!!!!!!!!!!!!
        # .npz file -> pd dataframe
        arr = np.load('PPG30min/' + file)['ppg']
        df = pd.DataFrame({'pleth':arr, 'timestamp':list(range(0, 1800000, 8)), 
            'sqi_s':[-1000]*225000, 'sqi_p':[-1000]*225000, 'sqi_k':[-1000]*225000})   # stamps by milisecond



        #create 2 piles for sending each chunk 
        df_good = pd.DataFrame({'pleth':[], 'timestamp':[]})
        df_bad = pd.DataFrame({'pleth':[], 'timestamp':[]})

        # for each 30 sec chunk of df
        for ii in range(0, 225000, 3750):
            smoll_df = df.iloc[ii, ii+3750]

            if 'df is good':
                df_good = pd.concat([df_good, smoll_df], ignore_index=True)
            else:
                df_bad = pd.concat([df_bad, smoll_df], ignore_index=True)



        
        # save good and bad df's to their respective folders, using to_csv
        df_good.to_csv('ppg_good/' + file[:-4] + '.csv') 
        df_bad.to_csv('ppg_bad/' + file[:-4] + '.csv') 


        
        
        





clean('PPG30min')

# plotting:
    # plt.figure(figsize=(14.5, 7.5))
    # plt.scatter(df['timestamp'][10000:11000], df['pleth'][10000:11000])
    # plt.title(file + ' ')
    # plt.show() 