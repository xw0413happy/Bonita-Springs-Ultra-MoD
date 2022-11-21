# -*- coding: utf-8 -*-
"""
Created on Wed Nov  9 15:45:49 2022

@author: xiw
"""



# Import library
import os
import pandas as pd
import datetime
from datetime import timedelta, datetime, time
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.dates import date2num
from matplotlib import dates as mdates
import tkinter as tk
# import customtkinter
from PIL import Image, ImageTk
from resizeimage import resizeimage
# from tkinter import ttk
import tkinter.font as font
from tkinter import filedialog

# Set up directory
os.chdir(r'S:\LeeTran\Planning\Intern\Wang Xi\LeeTran_Wang\Bonita Springs Ultra GUI App')
os.getcwd()


df_h = pd.read_csv(r'S:\LeeTran\Planning\Intern\Wang Xi\LeeTran_Wang\Bonita Springs Ultra GUI App\unique_trips.csv', parse_dates =["Request Time (Local)"], index_col ="Request Time (Local)")
df_h['datetime_format_date']= pd.to_datetime(df_h['Request Date (Local)'])
df_h['day_of_week'] = df_h['datetime_format_date'].dt.dayofweek

def categ_comple(row):  
    if row['Status'] == 'Completed':
        return row['Seats']
    
def categ_rc(row):  
    if row['Status'] == 'Rider Canceled':
        return row['Seats']
    
def categ_dc(row):  
    if row['Status'] == 'Driver Canceled':
        return row['Seats']
    
def categ_unf(row):  
    if row['Status'] == 'Unfulfilled':
        return row['Seats']
    
df_h['Comple_Count'] = df_h.apply(lambda row: categ_comple(row), axis=1)  
df_h['Rid_Cancl_Count'] = df_h.apply(lambda row: categ_rc(row), axis=1)    
df_h['Drv_Cancl_Count'] = df_h.apply(lambda row: categ_dc(row), axis=1)    
df_h['Unfil_Count'] = df_h.apply(lambda row: categ_unf(row), axis=1)    
df_h['Trip_Count'] = 1   

df_weekdays = df_h[(df_h["day_of_week"]!=5) & (df_h["day_of_week"]!=6)]
df_weekends = df_h[(df_h["day_of_week"]==5) | (df_h["day_of_week"]==6)]

df_weekdays.to_csv(r'S:\LeeTran\Planning\Intern\Wang Xi\LeeTran_Wang\Bonita Springs Ultra GUI App\df_weekdays.csv', index=False) 
df_weekends.to_csv(r'S:\LeeTran\Planning\Intern\Wang Xi\LeeTran_Wang\Bonita Springs Ultra GUI App\\df_weekends.csv', index=False) 

hourly_resampled_weekdays = df_weekdays.resample('60min').sum()
# hourly_resampled_weekdays = df_weekdays.resample('1H', base=2).sum()
hourly_resampled_weekends = df_weekends.resample('60min').sum()

hourly_resampled_weekdays.reset_index(inplace=True)
hourly_resampled_weekends.reset_index(inplace=True)

# remove the dates from the field
hourly_resampled_weekdays['TIME_INTERVALS'] = hourly_resampled_weekdays['Request Time (Local)'].dt.time
hourly_resampled_weekdays['TIME_INTERVALS_str'] = hourly_resampled_weekdays['TIME_INTERVALS'].astype(str)

start_time = hourly_resampled_weekdays['TIME_INTERVALS_str'][2]
end_time = hourly_resampled_weekdays['TIME_INTERVALS_str'][16]



# remove the dates from the field
hourly_resampled_weekends['TIME_INTERVALS'] = hourly_resampled_weekends['Request Time (Local)'].dt.time
hourly_resampled_weekends['TIME_INTERVALS_str'] = hourly_resampled_weekends['TIME_INTERVALS'].astype(str)


sns.set_theme(style="darkgrid")
sns.set(rc = {'figure.figsize':(12,8)})

ax = sns.lineplot(data=hourly_resampled_weekdays, x="TIME_INTERVALS_str", y="Trip_Count", color='black',label="Trips requested")
ax = sns.lineplot(data=hourly_resampled_weekdays, x="TIME_INTERVALS_str", y="Seats", color='black', linestyle="dashed", label="Seats requested")
ax = sns.lineplot(data=hourly_resampled_weekdays, x="TIME_INTERVALS_str", y="Comple_Count", color='green',linestyle="dashed", label="Passengers completed")
ax = sns.lineplot(data=hourly_resampled_weekdays, x="TIME_INTERVALS_str", y="Rid_Cancl_Count", color='purple',linestyle="dashed", label="Passengers canceled")
ax = sns.lineplot(data=hourly_resampled_weekdays, x="TIME_INTERVALS_str", y="Drv_Cancl_Count", color='b',linestyle="dashed",label="Passengers canceled by Driver")
ax = sns.lineplot(data=hourly_resampled_weekdays, x="TIME_INTERVALS_str", y="Unfil_Count", color='red',linestyle="dashed",label="Passengers unfulfilled")

ax.tick_params(axis='x', rotation=30)
ax.set_xlim([start_time, end_time])

plt.xlabel("Time of The Day") 
plt.ylabel("Counts") 
plt.legend(bbox_to_anchor=(1.02, 1), loc=2, borderaxespad=0.,fontsize = 12)

plt.title('Unique trip status by time of the day - Weekdays', fontsize = 15)
plt.savefig(r'C:\Users\xiw\Desktop\test - Weekdays.jpg', dpi=300,bbox_inches='tight')