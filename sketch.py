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


def npz_to_df(file_name):
    """
    Parameters
    ----------
    file_name : str
        name of folder containing .npz files


    Returns
    -------
    List of dataframe objects
    """
    # for each .npz file:
    for file in dirToFiles('PPG30min')[37:4000:538]:   # GET RID OF [:] LATER !!
        arr = np.load('PPG30min/' + file)['ppg']
        df = pd.DataFrame({'pleth':arr, 'timestamp':list(range(0, 1800000, 8))})   # stamps by milisecond

        plt.figure(figsize=(14.5, 7.5))
        plt.scatter(df['timestamp'][10000:11000], df['pleth'][10000:11000])
        plt.title(file + ' ')
        plt.show()
        ppg_data = 5
        sqis = sqi_hl.compute_SQI(ppg_data.signals, '5s', 0, 20, 'ppg', 125, 1)
        print(sqis.columns)

        if wave_type == 'ppg':
            sqis = signal.groupby(pd.Grouper(freq=segment_length)).apply(segment_PPG_SQI_extraction, sampling_rate, primary_peakdet, secondary_peakdet, (1, 1), (20, 4), template_type)

        #create 2 piles for sending each chunk 
        df_good = 
        df_bad = 


        # save good and bad df's to their respective folders, using to_csv
        








def PPG_reader(file_name, signal_idx, timestamp_idx, info_idx,
               timestamp_unit='ms', sampling_rate=None,
               start_datetime=None):
    """

    Parameters
    ----------
    file_name : str
        absolute path to ppg file

    signal_idx : list
        name of one column containing signal

    timestamp_idx : list
        name of one column containing timestamps

    info_idx : list
        name of the columns for other info

    timestamp_unit : str
        unit of timestamp, only 'ms' or 's' accepted
         (Default value = 'ms')
    sampling_rate : float
        if None, sampling_rate can be inferred from the
        timestamps
         (Default value = None)
    start_datetime : str
        in '%Y-%m-%d '%H:%M:%S.%f' format
         (Default value = None)

    Returns
    -------
    object of class SignalSQI

    """
    cols = timestamp_idx + signal_idx + info_idx
    print(type(file_name))
    if type(file_name) == str:
        tmp = pd.read_csv(file_name,
                      usecols=cols,
                      skipinitialspace=True,
                      skip_blank_lines=True)
    else:
        tmp = file_name[cols]

    timestamps = tmp[timestamp_idx[0]]
    #TODO: Generate timestamps if they are not part of the signal, infer from sampling rate
    if start_datetime is None:
        start_datetime = timestamps[0]
    if isinstance(start_datetime, str):
        try:
            start_datetime = dt.datetime.strptime(start_datetime, '%Y-%m-%d '
                                                                  '%H:%M:%S')
        except Exception:
            start_datetime = None
            pass
    else:
        start_datetime = None
    if sampling_rate is None:
        if timestamp_unit is None:
            raise Exception("Missing sampling_rate, not able to infer "
                            "sampling_rate without timestamp_unit")
        elif timestamp_unit == 'ms':
            timestamps = timestamps / 1000
        elif timestamp_unit != 's':
            raise Exception("Timestamp unit must be either second (s) or "
                            "millisecond (ms)")
        sampling_rate = utils.calculate_sampling_rate(timestamps.to_numpy())
    
    info = tmp[info_idx].to_dict('list')
    #Add index column
    signals = tmp[signal_idx]
    signals = signals.reset_index()
    #Transform timestamps
    signals['timedelta'] = pd.to_timedelta(signals.index / sampling_rate, unit='s')
    #signals['idx'] = signals.index
    signals = signals.set_index('timedelta')
    signals = signals.rename(columns={'index': 'idx'})

    out = SignalSQI(signals = signals, wave_type = 'ppg',
                    sampling_rate = sampling_rate,
                    start_datetime = start_datetime,
                    info = info)
    return out


def PPG_writer(signal_sqi, file_name):
    """

    Parameters
    ----------
    signal_sqi : object of class SignalSQI

    file_name : str
        absolute path

    file_type : str
        file type to write, either 'csv' or 'xlsx'
    Returns
    -------
    bool
    """
    timestamps = utils.generate_timestamp(
        start_datetime=signal_sqi.start_datetime,
        sampling_rate=signal_sqi.sampling_rate,
        signal_length=len(signal_sqi.signals[0]))

    signals = signal_sqi.signals[0]
    timestamps = np.array(timestamps)
    out_df = pd.DataFrame({'time': timestamps, 'pleth': signals})

    out_df.to_csv(file_name, index=False, header=True)
  
    return os.path.isfile(file_name)



def dirToFiles(dir_name):
    """
    Parameters
    ----------
    dir_name : str 
        name of directory (subdir of curr dir)

    Returns
    -------
    List of str, of file names (.npz)
    """
    dir = '/Users/andrew/Documents/ML/ppg-process/vsqi/' + dir_name
    return [x for x in os.listdir(dir) if '.npz' in x]






npz_to_df('PPG30min')