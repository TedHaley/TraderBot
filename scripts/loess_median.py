import scipy
import numpy as np
import pandas as pd
from pandas import Series
import warnings

warnings.filterwarnings('ignore')


def rolling_loess_median(data, window=240, threshold=3):
    """
    Flags anomalous flow observations beased on their deviation from expectec value.

    Parameters
    ----------
    data : 
        Raw data .csv file
        
    window : int
        Size of moving window (number of historical values to be used to classify most recent flow point)
        Default = 240
        
    threshold :
        An anomaly will be classified if greater than Q75 + threshold * IQR or less than Q25 - threshold * IQR
        Default = 3

    Returns
    -------
    A dataframe containing detected anomalies:
    	gage_id		: Unique gauge identification
    	date_time	: Date and time the reading was taken in format year-month-day-hour-minute-second. Example: `2016-05-08T20:36:00Z`
    	flow		: Flow rate measured at the gauge in $m^3/s$
    	water_lev	: Water level
    	anomaly		: Classification (Detected anamlies)
    
    """

    # Load data
    # headers = ["gauge_id","date_time","flow","water_lev","del"]
    # df = pd.read_csv(data, names=headers)
    df = pd.read_csv(data)

    # Error handling
    # if data is None or (not isinstance(data,pd.DataFrame)):
    # raise TypeError("Input data must be a dataframe")
    if window <= 0:
        raise ValueError("Window size should be positive")
    if threshold <= 0:
        raise ValueError("threshold should be positive")

    # Arrange data by date
    df = df.sort_values('date_time')

    # Uncomment if you want to filter for a specific year
    #     df['std_date'] = pd.to_datetime(df['date_time'])
    #     df['year'] = df['std_date'].dt.year
    #     df = df.loc[(df['year'] == 2016)]

    # Converting flow column into series
    series = pd.Series(df["flow"])
    series = series.to_frame('flow')

    # Computing rolling median, quantiles and Inter Quartile Range (IQR)
    df['median'] = series.rolling(window).median()
    df['q25'] = pd.rolling_quantile(series, window, 0.25)
    df['q75'] = pd.rolling_quantile(series, window, 0.75)
    df['iq_range'] = df['q75'] - df['q25']

    # Setting up boundaries of range (based on number of IQRs)
    df['b_high_upper'] = df['q75'] + threshold * df['iq_range']
    df['b_high_lower'] = df['q25'] - threshold * df['iq_range']

    df['b_med_upper'] = df['q75'] + threshold * df['iq_range']
    df['b_med_lower'] = df['q25'] - threshold * df['iq_range']

    # Classifying points as anomalies or not
    df['anomaly'] = np.where((df['flow'] > df['b_high_upper']) | (df['flow'] < df['b_high_lower']), 1, 0)

    # If IQR range = 0, dont mark them as anomalies.
    mask = df['iq_range'] == 0
    df.loc[mask, 'anomaly'] = 0

    df_anomaly = df[['gage_id', 'date_time', 'flow', 'water_lev', 'anomaly']].loc[df['anomaly'] == 1]

    return df_anomaly


def median_loess_median(data, window=240, threshold=3):
    """
    Computes recall and precision metrics for anmalies detected by median regression model
    Recall: How complet the results are (How many of the labelled anomalies were detected)
    Precision: How useful the results are (How many of the detected anomalies were labelled)

    Parameters
    ----------
    data : 
        Raw data .csv file
        
    window : int
        Size of moving window (number of historical values to be used to classify most recent flow point)
        Default = 240
        
    threshold :
        An anomaly will be classified if greater than Q75 + threshold * IQR or less than Q25 - threshold * IQR
        Default = 3

    Returns
    -------
    	Recall, Precision
    
    """

    # Load data
    df = pd.read_csv(data)

    # Results from anomaly detection
    anomaly_df = rolling_loess_median(data, window, threshold)

    # Combining above two data frames into one
    df_complete = pd.concat([df, anomaly_df], axis=1)
    df_complete['anomaly'] = df_complete['anomaly'].replace(np.nan, 0)

    # Metrics

    # Recall

    # All anomalies
    recall_df = df_complete.loc[df_complete['del'] == 1]
    detected_recall = len(recall_df.loc[recall_df['anomaly'] == 1])
    labelled_recall = len(recall_df['del'])

    # Anomalies over Q2
    recall_df_q2 = df_complete.loc[(df_complete['del'] == 1) & (df_complete['Q2'] == 1)]
    detected_recall_q2 = len(recall_df_q2.loc[recall_df_q2['anomaly'] == 1])
    labelled_recall_q2 = len(recall_df_q2['del'])

    #   recall = detected_recall/labelled_recall * 100

    # Precision

    # All anomalies
    prec_df = df_complete.loc[df_complete['anomaly'] == 1]
    labelled_precision = len(prec_df.loc[prec_df['del'] == 1])
    detected_precision = len(prec_df['anomaly'])

    # Anomalies over Q2
    prec_df_q2 = df_complete.loc[(df_complete['anomaly'] == 1) & (df_complete['Q2'] == 1)]
    labelled_precision_q2 = len(prec_df_q2.loc[prec_df_q2['del'] == 1])
    detected_precision_q2 = len(prec_df_q2['anomaly'])

    # 	if ((detected_precision==0)|(detected_precision_q2==0)):
    #     	precision = 0
    #     else:
    #     	precision = labelled_precision/detected_precision * 100

    return (
    detected_recall, labelled_recall, detected_recall_q2, labelled_recall_q2, labelled_precision, detected_precision,
    labelled_precision_q2, detected_precision_q2)
