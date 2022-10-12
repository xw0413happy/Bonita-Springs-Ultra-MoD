# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 10:53:17 2022

@author: xiw
"""

# Title: Plotting Ultra (On Demand Transit) graph GUI desktop app development
# Contact: wxi@leegov.com
# Author: Wang Xi
# Last Updated: 09-07-2022

# Update notes: customtkinter couldn't work on .ipynb
# Update notes: detect the most last 30-days daily trip, monthly trips & customizing the specific date range
# Update notes: constraint all images into the same size
# File Format: .py file


# Import library
import os
import pandas as pd
import datetime
from datetime import timedelta, datetime
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.dates import date2num
import tkinter as tk
# import customtkinter
from PIL import Image, ImageTk
from resizeimage import resizeimage
# from tkinter import ttk
import tkinter.font as font
from tkinter import filedialog

# Set up directory
# os.chdir(r'S:\LeeTran\Planning\Intern\Wang Xi\LeeTran_Wang\Ultra')
# os.getcwd()

    
# Define button function
def run_py_btn (Ultra_data):
    # df = pd.read_excel(r'S:\LeeTran\Planning\Ridership\Ultra_data_2022\Ultra_Data.xlsx')
    df = pd.read_excel(Ultra_data)

    df['Request_time'] = df['Request Time (Local)']
    df['Trip_ID_internal'] = df['Trip ID']

    for index, row in df.iterrows():
        df.loc[df['Booking Method'] == 'Bounce', 'Rider ID'] = 'Bounce Rider of the day' # assigning Rider ID
        df.loc[df['Booking Method'] == 'Central', 'Rider ID'] = df['Rider First Name'] + df['Rider Last Name'] # assigning Rider ID

    df['requested_datetime'] = df['Request Date (Local)'].astype(str) + ' ' + df['Request Time (Local)']
    df["requested_datetime"] = pd.to_datetime(df["requested_datetime"])  # convert text input to datetime format

    df = df.sort_values(['requested_datetime'], ascending=[True])
    dates_ls = df['Request Date (Local)'].tolist()
    dates_ls = list(set(dates_ls))
    dates_ls.sort()

    df_multi_trials = pd.DataFrame() # empty df to stroe the results

    k = 1
    h = 1

    for date in dates_ls:
        print('# On Date', date) 
        df_date = df[df["Request Date (Local)"]==date] # all users trips of a day
        users = df_date['Rider ID'].tolist()
        
        l1=[]
        dup_user = []
        for i in users:
            if i not in l1:
                l1.append(i)
            else:
                dup_user.append(i)
                
            dup_user = list(set(dup_user))
    #     print('* all users:', len(l1), l1)
    #     print('* multi-trip users:', len(dup_user), dup_user)  # find multiple trip users
        
        print('* all users:', len(l1))
        print('* multi-trip users:', len(dup_user))  # find multiple trip users
        
        print()
        
            # selet trips of every multiple trip user:
            
        for user in dup_user: # for every multiple trip users
            df_date_dup_user = df_date[df_date["Rider ID"]==user] # trips of a multiple trip user in a day
    #         print(df_date_dup_user)
            
            pick_list=df_date_dup_user['Pickup Address'].tolist()
            
            print('   --- user',user, '---')
            print()
            print('    *** all pick up locations of the user:', pick_list)
            
            # find the duplicate trip pick off location
            a=[]
            dup_pick_list=[]
            
            for i in pick_list:
                if i not in a:
                    a.append(i)
                else:
                    dup_pick_list.append(i)
            dup_pick_list = list(set(dup_pick_list))
            print('    *** dup_pick_list', dup_pick_list, len(dup_pick_list), 'duplicate picked up locations from the user.')
            print()
            
            
            if len(dup_pick_list) != 0: # if the list is not empty
                print('    **** The user had multiple tries on', len(dup_pick_list), 'pick up location')
                print()
                
                # select the data
                for pick in dup_pick_list:
                    multi_trip_cluster = df_date_dup_user[df_date_dup_user["Pickup Address"]==pick]
    #                 print(multi_trip_cluster)
                    print('-- pick up location:', pick)
                
                    # determine if the records are from the same intended trip
                    # start time and end time are within a time range
                    
                    max_time = multi_trip_cluster.requested_datetime.max()
                    min_time = multi_trip_cluster.requested_datetime.min() # get time as str
                    
                    print('--- time of the last try:', max_time)
                    print('--- time of the first try:', min_time)

                    time_elapsed = max_time - min_time  # calculate the time lapse between max and min
    #                 print('~~~ time_elapsed',time_elapsed, type(time_elapsed))
                    
                    thres = timedelta(minutes = 130) # if the time between the requests are within thres mins, we think they are for the same trip
    #                 print('threshold', thres, type(thres))
        
                    if thres > time_elapsed:
                        print("The requests are most likely from the same trip")

                        cluster_status_ls = multi_trip_cluster['Status'].tolist()
                        print(cluster_status_ls)
            
                        if cluster_status_ls.count('Completed') == 1:
                            print('Tried and completed!!!!!!!!!!')
                            multi_trip_cluster['multi_trials_trip_status'] = 'Tried and completed'
                            multi_trip_cluster['multi_trials_complete_count'] = k
                            k = k + 1
                            df_multi_trials = df_multi_trials.append(multi_trip_cluster, ignore_index=True)
                            
                        if 'Completed' not in cluster_status_ls:
                            print('Tried and Failed!!!!!!!!!!')
                            multi_trip_cluster['multi_trials_trip_status'] = 'Tried and failed'
                            multi_trip_cluster['multi_trials_failed_count'] = h
                            h = h + 1
                            df_multi_trials = df_multi_trials.append(multi_trip_cluster, ignore_index=True)
                            
                        if cluster_status_ls.count('Completed') > 1:
                            print('Rider completed more than one trip in the time window!!!!!!!!!!')
                            
                    else:
                        print("The requests are possibly not from the same trip")
                        
                    print()
                            
    df_multi_trials.to_csv(r'S:\LeeTran\Planning\Technology\Python Projects\Bonita Springs Ultra GUI App\User_trials_and_results130.csv', index=False) 

    multi_tripID_ls = df_multi_trials['Trip ID'].tolist()  # all the duplicated trips' IDs

    df_multi_trials['DropID'] = df_multi_trials['multi_trials_trip_status'] + df_multi_trials['multi_trials_complete_count'].astype(str) + df_multi_trials['multi_trials_failed_count'].astype(str)

    df_multi_trials_no_dup = df_multi_trials.drop_duplicates(subset="DropID", keep='last') # drop duplicates and keep fisrt record

    multi_tripID_keep_ls = df_multi_trials_no_dup['Trip ID'].tolist() # trips after droping duplicates

    trips_to_remove_ls = multi_tripID_ls.copy()

    for r in multi_tripID_keep_ls:
        if r in trips_to_remove_ls:
            trips_to_remove_ls.remove(r)

    # remove multi_tripID_ls from base table
    # remove duplicate casued by the multi-trial requests

    trip_ID_df = df[~df.Trip_ID_internal.isin(multi_tripID_ls)]
    trip_ID_df = trip_ID_df.append(df_multi_trials_no_dup, ignore_index=True) # add the no duplicates records back in
    
    trip_ID_df['date'] = trip_ID_df['Request Date (Local)'].astype(str)
    trip_ID_df['month'] = pd.DatetimeIndex(trip_ID_df['date']).month
    trip_ID_df['year'] = pd.DatetimeIndex(trip_ID_df['date']).year
    trip_ID_df['year-month'] = pd.to_datetime(trip_ID_df['date']).dt.to_period('M')

    trip_ID_df.to_csv(r'S:\LeeTran\Planning\Technology\Python Projects\Bonita Springs Ultra GUI App\unique_trips.csv', index=False) 



    # First graph
    plt.figure().clear()
    plt.close()
    plt.cla()
    plt.clf()
    # sns.set(style="whitegrid")
    # sns.set_theme(style="whitegrid")
    sns.set(rc = {'figure.figsize':(15,8)})
    ax = sns.countplot(x="date", hue="Status", data=trip_ID_df, palette = "Set2", linewidth=0.5)
    ax.legend(bbox_to_anchor=(1.02, 1), loc=2, borderaxespad=0.,fontsize = 10, title = 'Trip Status')
    ax.set_xticklabels(ax.get_xticklabels(), rotation = 60)

    plt.title('Final status of unique trips',fontsize = 18)
    plt.savefig(r'S:\LeeTran\Planning\Technology\Python Projects\Bonita Springs Ultra GUI App\Final status of unique trips.jpg', dpi=300,bbox_inches='tight')
    
    
    # First graph-monthly trip
    plt.figure().clear()
    plt.close()
    plt.cla()
    plt.clf()
    # sns.set(style="whitegrid")
    # sns.set_theme(style="whitegrid")
    sns.set(rc = {'figure.figsize':(15,8)})
    ax = sns.countplot(x="year-month", hue="Status", data=trip_ID_df, palette = "Set2",linewidth=0.5)
    ax.legend(bbox_to_anchor=(1.02, 1), loc=2, borderaxespad=0.,fontsize = 12, title = 'Trip Status')
    ax.set_xticklabels(ax.get_xticklabels(), rotation = 60)

    plt.title('Final status of unique trips by month',fontsize = 20)
    plt.savefig(r'S:\LeeTran\Planning\Technology\Python Projects\Bonita Springs Ultra GUI App\Final status of unique monthly trips.jpg', dpi=300,bbox_inches='tight')


    # First graph-last 30 days daily trip
    # plt.figure().clear()
    # plt.close()
    # plt.cla()
    # plt.clf()
    
    # today = datetime.today()
    # last_30_days = today - timedelta(days=30)
    # last_30_days = last_30_days.strftime("%Y-%m-%d")
    ## trip_ID_df['last_30_days'] = last_30_days 
    ## last_30_days = trip_ID_df['last_30_days'].astype(str)
    # last_date = trip_ID_df.iloc[-1, trip_ID_df.columns.get_loc('date')]
    # if last_date >= last_30_days:
        # trip_ID_df_30 = trip_ID_df[(trip_ID_df.date >= last_30_days)]
        ## len(trip_ID_df)
        ## len(trip_ID_df_30)
        # start = datetime.strptime(last_30_days,"%Y-%m-%d")
        # today = today.strftime("%Y-%m-%d")
        # end = datetime.strptime(today,"%Y-%m-%d")
        # date_range = pd.date_range(start, end)
        # date_range = date_range.astype(str)
        # trip_ID_df_30 = trip_ID_df[trip_ID_df["date"].isin(date_range)] # df.loc doesn't work because it is a datetime index


        # sns.set(rc = {'figure.figsize':(15,8)})
        # ax = sns.countplot(x="date", hue="Status", data=trip_ID_df_30, palette = "Set2",linewidth=0.5)
        # ax.legend(bbox_to_anchor=(1.02, 1), loc=2, borderaxespad=0.,fontsize = 12, title = 'Trip Status')
        # ax.set_xticklabels(ax.get_xticklabels(), rotation = 60)

        # plt.title('Final status of unique daily trips for last 30-days',fontsize = 20)
        # plt.savefig(r'S:\LeeTran\Planning\Technology\Python Projects\Bonita Springs Ultra GUI App\Final status of unique daily trips for last 30-days.jpg', dpi=300,bbox_inches='tight')
    # else:
        # print ("---------------------The last 30 days figure failed--------------")
    
    
  
    # First graph-customize the date range
    plt.figure().clear()
    plt.close()
    plt.cla()
    plt.clf()
    
    start = datetime.strptime(entry_start.get(),"%Y-%m-%d")
    end = datetime.strptime(entry_end.get(),"%Y-%m-%d")
    date_range = pd.date_range(start, end)
    date_range= date_range.astype(str)
    trip_ID_df_range = trip_ID_df[trip_ID_df["date"].isin(date_range)] # df.loc doesn't work because it is a datetime index
    
    
    sns.set(rc = {'figure.figsize':(15,8)})
    flatui = ["#3498db", "#9b59b6", "#95a5a6", "#e74c3c"]
    ax = sns.countplot(x="date", hue="Status", data=trip_ID_df_range, palette = flatui, linewidth=0.5)
    ax.legend(bbox_to_anchor=(1.02, 1), loc=2, borderaxespad=0.,fontsize = 8, title = 'Trip Status')
    ax.set_xticklabels(ax.get_xticklabels(), rotation = 60)
    start = start.strftime("%m/%d/%Y")
    end = end.strftime("%m/%d/%Y")
    new_name = 'Customizing the date range' + ' from ' + start + ' to ' + end + ' for final status of unique daily trips'

    plt.title(new_name, fontsize = 12)
    plt.savefig(r'S:\LeeTran\Planning\Technology\Python Projects\Bonita Springs Ultra GUI App\Customizing the date range for final status of unique daily trips.jpg', dpi=300,bbox_inches='tight')
    
    
    
    # Second graph
    plt.figure().clear()
    plt.close()
    plt.cla()
    plt.clf()
    
    trip_ID_df_plot = trip_ID_df.groupby(['date', 'Seats']).size().reset_index().pivot(columns='Seats', index='date', values=0)
    # plt.figure(figsize=(15, 8))
    trip_ID_df_plot.plot(kind='bar', stacked=True)
    
    plt.title('1-seat trip vs 2-seats trip (unique trips)',fontsize = 20)
    # plt.show()
    plt.rcParams['figure.figsize'] = [15, 8]
    plt.legend(title = "Seats", title_fontsize = 12, bbox_to_anchor =(1.01, 1), loc=2)
    plt.savefig(r'S:\LeeTran\Planning\Technology\Python Projects\Bonita Springs Ultra GUI App\1-seat trip vs 2-seats trip.jpg', dpi=300,bbox_inches='tight')

    # Second graph-month
    plt.figure().clear()
    plt.close()
    plt.cla()
    plt.clf()

    trip_ID_df_plot = trip_ID_df.groupby(['year-month', 'Seats']).size().reset_index().pivot(columns='Seats', index='year-month', values=0)
    trip_ID_df_plot.plot(kind='bar', stacked=True)
    plt.title('1-seat trip vs 2-seats trip (unique trips) by month',fontsize = 20)
    # fig_width, fig_height = plt.gcf().get_size_inches()
    # print(fig_width, fig_height)
    plt.legend(title = "Seats", title_fontsize = 12, bbox_to_anchor =(1.01, 1), loc=2)
    plt.savefig(r'S:\LeeTran\Planning\Technology\Python Projects\Bonita Springs Ultra GUI App\1-seat trip vs 2-seats monthly trip.jpg', dpi=300,bbox_inches='tight')


    # Second graph-last 30 days
    # plt.figure().clear()
    # plt.close()
    # plt.cla()
    # plt.clf()

    # trip_ID_df_plot = trip_ID_df_30.groupby(['date', 'Seats']).size().reset_index().pivot(columns='Seats', index='date', values=0)
    # trip_ID_df_plot.plot(kind='bar', stacked=True)
    # plt.title('1-seat trip vs 2-seats daily trip (unique trips) for last 30-days',fontsize = 20)
    # plt.legend(title = "Seats", title_fontsize = 12, bbox_to_anchor =(1.01, 1), loc=2)
    # plt.savefig(r'S:\LeeTran\Planning\Technology\Python Projects\Bonita Springs Ultra GUI App\1-seat trip vs 2-seats daily trip for last 30-days.jpg', dpi=300,bbox_inches='tight')
    
    
    # Second graph-customizing 1-seat vs 2-seat trips
    plt.figure().clear()
    plt.close()
    plt.cla()
    plt.clf()
    
    start = datetime.strptime(entry_start.get(),"%Y-%m-%d")
    end = datetime.strptime(entry_end.get(),"%Y-%m-%d")
    date_range = pd.date_range(start, end)
    date_range= date_range.astype(str)
    trip_ID_df_range = trip_ID_df[trip_ID_df["date"].isin(date_range)] # df.loc doesn't work because it is a datetime index

    trip_ID_df_plot = trip_ID_df_range.groupby(['date', 'Seats']).size().reset_index().pivot(columns='Seats', index='date', values=0)
    trip_ID_df_plot.plot(kind='bar', stacked=True)
    
    start = start.strftime("%m/%d/%Y")
    end = end.strftime("%m/%d/%Y")
    new_name = 'Customizing the date range' + ' from ' + start + ' to ' + end + ' for 1-seat vs 2-seat daily trip'
       
    plt.title(new_name, fontsize = 15)
    plt.legend(title = "Seats", title_fontsize = 12, bbox_to_anchor =(1.01, 1), loc=2)
    plt.savefig(r'S:\LeeTran\Planning\Technology\Python Projects\Bonita Springs Ultra GUI App\Customizing 1-seat vs 2-seats daily trip.jpg', dpi=300,bbox_inches='tight')


    # Third graph
    plt.figure().clear()
    plt.close()
    plt.cla()
    plt.clf()

    # index_col ="date", makes "date" column, the index of the data frame
    df_d = pd.read_csv(r'S:\LeeTran\Planning\Technology\Python Projects\Bonita Springs Ultra GUI App\unique_trips.csv', parse_dates =["Request Date (Local)"], index_col ="Request Date (Local)")

    daily_resampled_data = df_d.resample('D').sum()

    df_d_completed = df_d[df_d["Status"]=='Completed']
    df_d_completed_resampled_data = df_d_completed.resample('D').sum()

    # weekly_resampled_data['date_for_visual'] = weekly_resampled_data['Request Date (Local)']
    daily_resampled_data.reset_index(inplace=True)


    sns.set_theme(style="darkgrid")
    sns.set(rc = {'figure.figsize':(15,8)})

    ax = sns.lineplot(data=daily_resampled_data, x="Request Date (Local)", y="Seats", color='steelblue',label="Seats requested")
    ax1 = sns.lineplot(data=df_d_completed_resampled_data, x="Request Date (Local)", y="Seats", color='purple',label="Seats completed" )
    ax.tick_params(axis='x', rotation=90)

    plt.xlabel("Date") 
    plt.ylabel("Seats") 
    plt.legend(bbox_to_anchor=(1.02, 1), loc=2, borderaxespad=0.,fontsize = 12)

    plt.title('Seats requested vs. seats completed (unique trips)',fontsize = 20)
    plt.savefig(r'S:\LeeTran\Planning\Technology\Python Projects\Bonita Springs Ultra GUI App\Seats requested vs completed.jpg', dpi=300,bbox_inches='tight')


    # 4th graph
    # index_col ="date", makes "date" column, the index of the data frame
    df_h = pd.read_csv(r'S:\LeeTran\Planning\Technology\Python Projects\Bonita Springs Ultra GUI App\unique_trips.csv', parse_dates =["Request Time (Local)"], index_col ="Request Time (Local)")

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

    hourly_resampled_data = df_h.resample('60min').sum()
    hourly_resampled_data.reset_index(inplace=True)

    # remove the dates from the field
    hourly_resampled_data['TIME_INTERVALS'] = hourly_resampled_data['Request Time (Local)'].dt.time
    hourly_resampled_data['TIME_INTERVALS_str'] = hourly_resampled_data['TIME_INTERVALS'].astype(str)

    plt.figure().clear()
    plt.close()
    plt.cla()
    plt.clf()


    trip_ID_df = pd.read_csv(r'S:\LeeTran\Planning\Technology\Python Projects\Bonita Springs Ultra GUI App\unique_trips.csv')
    trip_ID_df['date'] = trip_ID_df['Request Date (Local)'].astype(str)
    trip_ID_df.loc[trip_ID_df['Matched'].isnull() , 'Matched'] = 'Not matched'
    # print(trip_ID_df)

    trip_ID_df_plot = trip_ID_df.groupby(['date', 'Matched']).size().reset_index().pivot(columns='Matched', index='date', values=0)
    # print(trip_ID_df_plot)
    trip_ID_df_plot.plot(kind='bar', stacked=True, color= ['orange', 'c'])

    plt.title('Matched vs. Not matched unique trips',fontsize = 20)
    plt.legend(title = "Matched Status", title_fontsize = 12, bbox_to_anchor =(1.01, 1), loc=2)
    plt.savefig(r'S:\LeeTran\Planning\Technology\Python Projects\Bonita Springs Ultra GUI App\Matched unique trips.jpg', dpi=300,bbox_inches='tight')


    # 4th graph-month
    plt.figure().clear()
    plt.close()
    plt.cla()
    plt.clf()

    trip_ID_df = pd.read_csv(r'S:\LeeTran\Planning\Technology\Python Projects\Bonita Springs Ultra GUI App\unique_trips.csv')
    trip_ID_df['date'] = trip_ID_df['Request Date (Local)'].astype(str)
    trip_ID_df.loc[trip_ID_df['Matched'].isnull() , 'Matched'] = 'Not matched'
    # print(trip_ID_df)

    trip_ID_df_plot = trip_ID_df.groupby(['year-month', 'Matched']).size().reset_index().pivot(columns='Matched', index='year-month', values=0)
    # print(trip_ID_df_plot)
    trip_ID_df_plot.plot(kind='bar', stacked=True, color= ['orange', 'c'])

    plt.title('Matched vs. Not matched unique trips by month',fontsize = 20)
    plt.legend(title = "Matched Status", title_fontsize = 12, bbox_to_anchor =(1.01, 1), loc=2)
    plt.savefig(r'S:\LeeTran\Planning\Technology\Python Projects\Bonita Springs Ultra GUI App\Matched unique monthly trips.jpg', dpi=300,bbox_inches='tight')


    # 4th graph-for last 30 days
    # plt.figure().clear()
    # plt.close()
    # plt.cla()
    # plt.clf()

    # trip_ID_df = pd.read_csv(r'S:\LeeTran\Planning\Technology\Python Projects\Bonita Springs Ultra GUI App\unique_trips.csv')
    # trip_ID_df['date'] = trip_ID_df['Request Date (Local)'].astype(str)
    # trip_ID_df_30.loc[trip_ID_df_30['Matched'].isnull() , 'Matched'] = 'Not matched'

    # trip_ID_df_plot = trip_ID_df_30.groupby(['date', 'Matched']).size().reset_index().pivot(columns='Matched', index='date', values=0)
    # trip_ID_df_plot.plot(kind='bar', stacked=True, color= ['orange', 'c'])

    # plt.title('Matched vs. Not matched unique daily trips for last 30-days',fontsize = 20)
    # plt.legend(title = "Matched Status", title_fontsize = 12, bbox_to_anchor =(1.01, 1), loc=2)
    # plt.savefig(r'S:\LeeTran\Planning\Technology\Python Projects\Bonita Springs Ultra GUI App\Matched unique daily trips for last 30-days.jpg', dpi=300,bbox_inches='tight')
    
    
    # 4th graph-for customizing the specific date range
    plt.figure().clear()
    plt.close()
    plt.cla()
    plt.clf()

    trip_ID_df = pd.read_csv(r'S:\LeeTran\Planning\Technology\Python Projects\Bonita Springs Ultra GUI App\unique_trips.csv')
    trip_ID_df['date'] = trip_ID_df['Request Date (Local)'].astype(str)
       
    start = datetime.strptime(entry_start.get(),"%Y-%m-%d")
    end = datetime.strptime(entry_end.get(),"%Y-%m-%d")
    date_range = pd.date_range(start, end)
    date_range= date_range.astype(str)
    trip_ID_df_range = trip_ID_df[trip_ID_df["date"].isin(date_range)] # df.loc doesn't work because it is a datetime index
    trip_ID_df_range.loc[trip_ID_df_range['Matched'].isnull() , 'Matched'] = 'Not matched'
    
    trip_ID_df_plot = trip_ID_df_range.groupby(['date', 'Matched']).size().reset_index().pivot(columns='Matched', index='date', values=0)
    trip_ID_df_plot.plot(kind='bar', stacked=True, color= ['orange', 'c'])
    start = start.strftime("%m/%d/%Y")
    end = end.strftime("%m/%d/%Y")
    new_name = 'Customizing the date range' + ' from ' + start + ' to ' + end + ' for Matched vs. Not Matched unique daily trips'

    plt.title(new_name, fontsize = 15)
    plt.legend(title = "Matched Status", title_fontsize = 12, bbox_to_anchor =(1.01, 1), loc=2)
    plt.savefig(r'S:\LeeTran\Planning\Technology\Python Projects\Bonita Springs Ultra GUI App\Customizing matched unique daily trips.jpg', dpi=300,bbox_inches='tight')


    # 5th graph
    plt.figure().clear()
    plt.close()
    plt.cla()
    plt.clf()

    # index_col ="date", makes "date" column, the index of the data frame

    df_h = pd.read_csv(r'S:\LeeTran\Planning\Technology\Python Projects\Bonita Springs Ultra GUI App\unique_trips.csv', parse_dates =["Request Time (Local)"], index_col ="Request Time (Local)")
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

    df_weekdays.to_csv(r'S:\LeeTran\Planning\Technology\Python Projects\Bonita Springs Ultra GUI App\df_weekdays.csv', index=False) 
    df_weekends.to_csv(r'S:\LeeTran\Planning\Technology\Python Projects\Bonita Springs Ultra GUI App\df_weekends.csv', index=False) 

    hourly_resampled_weekdays = df_weekdays.resample('60min').sum()
    hourly_resampled_weekends = df_weekends.resample('60min').sum()

    hourly_resampled_weekdays.reset_index(inplace=True)
    hourly_resampled_weekends.reset_index(inplace=True)

    # remove the dates from the field
    hourly_resampled_weekdays['TIME_INTERVALS'] = hourly_resampled_weekdays['Request Time (Local)'].dt.time
    hourly_resampled_weekdays['TIME_INTERVALS_str'] = hourly_resampled_weekdays['TIME_INTERVALS'].astype(str)

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
    plt.xlabel("Time of The Day") 
    plt.ylabel("Counts") 
    plt.legend(bbox_to_anchor=(1.02, 1), loc=2, borderaxespad=0.,fontsize = 12)

    plt.title('Unique trip status by time of the day - Weekdays', fontsize = 15)
    plt.savefig(r'S:\LeeTran\Planning\Technology\Python Projects\Bonita Springs Ultra GUI App\Unique trip status by time of the day - Weekdays.jpg', dpi=300,bbox_inches='tight')
    
    
    
    # 5th graph-customize the date range
    plt.figure().clear()
    plt.close()
    plt.cla()
    plt.clf()
    
    df_h = pd.read_csv(r'S:\LeeTran\Planning\Technology\Python Projects\Bonita Springs Ultra GUI App\unique_trips.csv', parse_dates =["Request Time (Local)"], index_col ="Request Time (Local)")
    
    # set-up date range based on the entry
    start = datetime.strptime(entry_start.get(),"%Y-%m-%d")
    end = datetime.strptime(entry_end.get(),"%Y-%m-%d")
    date_range = pd.date_range(start, end)
    date_range= date_range.astype(str)
    df_h_range = df_h[df_h["date"].isin(date_range)] # df.loc doesn't work because it is a datetime index
    
    
    df_h_range['datetime_format_date']= pd.to_datetime(df_h_range['Request Date (Local)'])
    df_h_range['day_of_week'] = df_h_range['datetime_format_date'].dt.dayofweek

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
        
    df_h_range['Comple_Count'] = df_h_range.apply(lambda row: categ_comple(row), axis=1)  
    df_h_range['Rid_Cancl_Count'] = df_h_range.apply(lambda row: categ_rc(row), axis=1)    
    df_h_range['Drv_Cancl_Count'] = df_h_range.apply(lambda row: categ_dc(row), axis=1)    
    df_h_range['Unfil_Count'] = df_h_range.apply(lambda row: categ_unf(row), axis=1)    
    df_h_range['Trip_Count'] = 1   

    df_weekdays_range = df_h_range[(df_h_range["day_of_week"]!=5) & (df_h_range["day_of_week"]!=6)]
    df_weekends_range = df_h_range[(df_h_range["day_of_week"]==5) | (df_h_range["day_of_week"]==6)]

    df_weekdays_range.to_csv(r'S:\LeeTran\Planning\Technology\Python Projects\Bonita Springs Ultra GUI App\df_weekdays_cutrng.csv', index=False) 
    df_weekends_range.to_csv(r'S:\LeeTran\Planning\Technology\Python Projects\Bonita Springs Ultra GUI App\df_weekends_cutrng.csv', index=False) 

    hourly_resampled_weekdays_range = df_weekdays_range.resample('60min').sum()
    hourly_resampled_weekends_range = df_weekends_range.resample('60min').sum()

    hourly_resampled_weekdays_range.reset_index(inplace=True)
    hourly_resampled_weekends_range.reset_index(inplace=True)

    # remove the dates from the field
    hourly_resampled_weekdays_range['TIME_INTERVALS'] = hourly_resampled_weekdays_range['Request Time (Local)'].dt.time
    hourly_resampled_weekdays_range['TIME_INTERVALS_str'] = hourly_resampled_weekdays_range['TIME_INTERVALS'].astype(str)

    # remove the dates from the field
    hourly_resampled_weekends_range['TIME_INTERVALS'] = hourly_resampled_weekends_range['Request Time (Local)'].dt.time
    hourly_resampled_weekends_range['TIME_INTERVALS_str'] = hourly_resampled_weekends_range['TIME_INTERVALS'].astype(str)


    sns.set_theme(style="darkgrid")
    sns.set(rc = {'figure.figsize':(12,8)})

    ax = sns.lineplot(data=hourly_resampled_weekdays_range, x="TIME_INTERVALS_str", y="Trip_Count", color='black',label="Trips requested")
    ax = sns.lineplot(data=hourly_resampled_weekdays_range, x="TIME_INTERVALS_str", y="Seats", color='black', linestyle="dashed", label="Seats requested")
    ax = sns.lineplot(data=hourly_resampled_weekdays_range, x="TIME_INTERVALS_str", y="Comple_Count", color='green',linestyle="dashed", label="Passengers completed")
    ax = sns.lineplot(data=hourly_resampled_weekdays_range, x="TIME_INTERVALS_str", y="Rid_Cancl_Count", color='purple',linestyle="dashed", label="Passengers canceled")
    ax = sns.lineplot(data=hourly_resampled_weekdays_range, x="TIME_INTERVALS_str", y="Drv_Cancl_Count", color='b',linestyle="dashed",label="Passengers canceled by Driver")
    ax = sns.lineplot(data=hourly_resampled_weekdays_range, x="TIME_INTERVALS_str", y="Unfil_Count", color='red',linestyle="dashed",label="Passengers unfulfilled")

    ax.tick_params(axis='x', rotation=30)
    plt.xlabel("Time of The Day") 
    plt.ylabel("Counts") 
    plt.legend(bbox_to_anchor=(1.02, 1), loc=2, borderaxespad=0.,fontsize = 12)
    start = start.strftime("%m/%d/%Y")
    end = end.strftime("%m/%d/%Y")
    new_name = 'Customizing the date range' + ' from ' + start + ' to ' + end + ' for unique trip status by time of the day - Weekdays'

    plt.title(new_name, fontsize = 15)
    plt.savefig(r'S:\LeeTran\Planning\Technology\Python Projects\Bonita Springs Ultra GUI App\Customizing unique trip status by time of the day - Weekdays.jpg', dpi=300,bbox_inches='tight')


    # 6th graph
    plt.figure().clear()
    plt.close()
    plt.cla()
    plt.clf()


    sns.set_theme(style="darkgrid")
    sns.set(rc = {'figure.figsize':(12,8)})

    ax = sns.lineplot(data=hourly_resampled_weekends, x="TIME_INTERVALS_str", y="Trip_Count", color='black',label="Trips requested")
    ax = sns.lineplot(data=hourly_resampled_weekends, x="TIME_INTERVALS_str", y="Seats", color='black', linestyle="dashed", label="Seats requested")
    ax = sns.lineplot(data=hourly_resampled_weekends, x="TIME_INTERVALS_str", y="Comple_Count", color='green',linestyle="dashed", label="Passengers completed")
    ax = sns.lineplot(data=hourly_resampled_weekends, x="TIME_INTERVALS_str", y="Rid_Cancl_Count", color='purple',linestyle="dashed", label="Passengers canceled")
    ax = sns.lineplot(data=hourly_resampled_weekends, x="TIME_INTERVALS_str", y="Drv_Cancl_Count", color='b',linestyle="dashed",label="Passengers canceled by Driver")
    ax = sns.lineplot(data=hourly_resampled_weekends, x="TIME_INTERVALS_str", y="Unfil_Count", color='red',linestyle="dashed",label="Passengers unfulfilled")

    ax.tick_params(axis='x', rotation=30)
    plt.xlabel("Time of The Day") 
    plt.ylabel("Counts") 
    plt.legend(bbox_to_anchor=(1.02, 1), loc=2, borderaxespad=0.,fontsize = 12)

    plt.title('Unique trip status by time of the day - Weekends', fontsize = 15)
    plt.savefig(r'S:\LeeTran\Planning\Technology\Python Projects\Bonita Springs Ultra GUI App\Unique trip status by time of the day - Weekends.jpg', dpi=300,bbox_inches='tight')
    
    
    
    # 6th graph-customize the specific date range
    plt.figure().clear()
    plt.close()
    plt.cla()
    plt.clf()


    sns.set_theme(style="darkgrid")
    sns.set(rc = {'figure.figsize':(12,8)})

    ax = sns.lineplot(data=hourly_resampled_weekends_range, x="TIME_INTERVALS_str", y="Trip_Count", color='black',label="Trips requested")
    ax = sns.lineplot(data=hourly_resampled_weekends_range, x="TIME_INTERVALS_str", y="Seats", color='black', linestyle="dashed", label="Seats requested")
    ax = sns.lineplot(data=hourly_resampled_weekends_range, x="TIME_INTERVALS_str", y="Comple_Count", color='green',linestyle="dashed", label="Passengers completed")
    ax = sns.lineplot(data=hourly_resampled_weekends_range, x="TIME_INTERVALS_str", y="Rid_Cancl_Count", color='purple',linestyle="dashed", label="Passengers canceled")
    ax = sns.lineplot(data=hourly_resampled_weekends_range, x="TIME_INTERVALS_str", y="Drv_Cancl_Count", color='b',linestyle="dashed",label="Passengers canceled by Driver")
    ax = sns.lineplot(data=hourly_resampled_weekends_range, x="TIME_INTERVALS_str", y="Unfil_Count", color='red',linestyle="dashed",label="Passengers unfulfilled")

    ax.tick_params(axis='x', rotation=30)
    plt.xlabel("Time of The Day") 
    plt.ylabel("Counts") 
    plt.legend(bbox_to_anchor=(1.02, 1), loc=2, borderaxespad=0.,fontsize = 12)
    # start = start.strftime("%m/%d/%Y")
    # end = end.strftime("%m/%d/%Y")
    new_name = 'Customizing the date range' + ' from ' + start + ' to ' + end + ' for unique trip status by time of the day - Weekends'

    plt.title(new_name, fontsize = 15)
    plt.savefig(r'S:\LeeTran\Planning\Technology\Python Projects\Bonita Springs Ultra GUI App\Customizing unique trip status by time of the day - Weekends.jpg', dpi=300,bbox_inches='tight')
    
    
    
    
    # 7th Customizing Seat Request
    plt.figure().clear()
    plt.close()
    plt.cla()
    plt.clf()

    # index_col ="date", makes "date" column, the index of the data frame
    df_d = pd.read_csv(r'S:\LeeTran\Planning\Technology\Python Projects\Bonita Springs Ultra GUI App\unique_trips.csv', parse_dates =["Request Date (Local)"], index_col ="Request Date (Local)")
    
    start = datetime.strptime(entry_start.get(),"%Y-%m-%d")
    end = datetime.strptime(entry_end.get(),"%Y-%m-%d")
    date_range = pd.date_range(start, end)
    date_range= date_range.astype(str)
    df_d_range = df_d[df_d["date"].isin(date_range)] # df.loc doesn't work because it is a datetime index
    

    daily_resampled_data = df_d_range.resample('D').sum()

    df_d_completed = df_d_range[df_d_range["Status"]=='Completed']
    df_d_completed_resampled_data = df_d_completed.resample('D').sum()

    # weekly_resampled_data['date_for_visual'] = weekly_resampled_data['Request Date (Local)']
    daily_resampled_data.reset_index(inplace=True)


    sns.set_theme(style="darkgrid")
    sns.set(rc = {'figure.figsize':(15,8)})

    ax = sns.lineplot(data=daily_resampled_data, x="Request Date (Local)", y="Seats", color='steelblue',label="Seats requested")
    ax1 = sns.lineplot(data=df_d_completed_resampled_data, x="Request Date (Local)", y="Seats", color='purple',label="Seats completed" )
    ax.tick_params(axis='x', rotation=90)

    plt.xlabel("Date") 
    plt.ylabel("Seats") 
    plt.legend(bbox_to_anchor=(1.02, 1), loc=2, borderaxespad=0.,fontsize = 12)
    start = start.strftime("%m/%d/%Y")
    end = end.strftime("%m/%d/%Y")
    new_name = 'Customizing the date range' + ' from ' + start + ' to ' + end + ' for Seats requested vs. Seats completed (unique trips)'

    plt.title(new_name, fontsize = 15)
    plt.savefig(r'S:\LeeTran\Planning\Technology\Python Projects\Bonita Springs Ultra GUI App\Customizing seats requested vs completed.jpg', dpi=300,bbox_inches='tight')
    
        
    print("**********Completed***********")




# root = customtkinter.CTk()
root = tk.Tk()
root.configure(background="#6897bb")
root.title('Bonita Springs MoD Graph')
root.geometry("600x480")

# Set up windows background
# canvas = tk.Canvas(root, bg ='#efdecd')
# canvas.pack(fill = tk.BOTH, expand=True)

# Define the images
# add_py_image = ImageTk.PhotoImage(Image.open(r'C:\Users\xiw\Desktop\pic\file png.png').resize((10, 10), Image.ANTIALIAS))
# add_graph_image = ImageTk.PhotoImage(Image.open(r'C:\Users\xiw\Desktop\pic\graph jpg.jpg').resize((5, 5), Image.ANTIALIAS))

# Resize Ultra logo
# logo = Image.open(r'S:\LeeTran\Planning\Intern\Wang Xi\LeeTran_Wang\Ultra\pic\ultra logo.png')
# logo.size
# logo_resize = logo.resize((logo.width // 2, logo.height // 2)) # same as logo.reduce(2)
# logo_resize.show()
# logo_resize.save(r'S:\LeeTran\Planning\Intern\Wang Xi\LeeTran_Wang\Ultra\pic\resized ultra logo.png')

# Set up logo positions
logo0 = Image.open(r'S:\LeeTran\Planning\Technology\Python Projects\Bonita Springs Ultra GUI App\pic\Bonita Springs long text logo.png')
logo0 = logo0.reduce(2)
logo0 = ImageTk.PhotoImage(logo0)
logo0_label = tk.Label(image=logo0)
logo0_label.image = logo0 # cannot skip this line of code, it's necessary
logo0_label.grid(row=0, column=1, pady=10)

logo2 = Image.open(r'S:\LeeTran\Planning\Technology\Python Projects\Bonita Springs Ultra GUI App\pic\resized ultra logo.png')
logo2 = ImageTk.PhotoImage(logo2)
logo2_label = tk.Label(image=logo2)
logo2_label.image = logo2 # cannot skip this line of code, it's necessary
logo2_label.grid(row=0, column=0, pady=10)

# Entry widget set-up
entry = tk.StringVar()
path0 = []

def addPath():
    filename = filedialog.askopenfilename(initialdir='/', title="Select Ultra xlsx File Path", 
                                          filetypes=(("Ultra excel File Path", "*.xlsx"), ))
    path0.append(filename)
    print(filename)
    for path in path0:
        Label_entry = tk.Label(root, text = path, bg='gray')
        E1.insert(0,filename)
        Label_entry.pack()

B1 = tk.Button(root, text="Ultra Data .xlsx File Path", command=addPath, bg="#c19a6b", fg='white')
B1.grid(row=1, column=0, pady=5)

E1 = tk.Entry(root, width=60, textvariable=entry, bg="#91a3b0")
E1.grid(row=1, column=1, pady=5)      

# Set up date range
entry_start = tk.StringVar()
entry_end = tk.StringVar()

L1 = tk.Label(root, text = "Enter Start Date (yyyy-mm-dd)", bg="#1e4d2b", fg='white')
L1.grid(row=2, column=0, pady=5, padx=10)
E2 = tk.Entry(root, width=60, textvariable=entry_start, bg="#91a3b0")
E2.grid(row=2, column=1, pady=5)

L2 = tk.Label(root, text = "Enter End Date (yyyy-mm-dd)", bg="#1e4d2b", fg='white')
L2.grid(row=3, column=0, pady=5, padx=10)
E3 = tk.Entry(root, width=60, textvariable=entry_end, bg="#91a3b0")
E3.grid(row=3, column=1, pady=5)  


# loop over the images
img_index = 0

# Define button functions    
def check():
    run_py_btn(entry.get())

def clicker():
    global pop
    global my_label
    global img_index
    pop = tk.Toplevel(root)
   
    
    pop.title("Bonita Springs Ultra Service MoD Data Plotting")
    for i in range(3):
        pop.columnconfigure(i, weight=1, minsize=75)
        pop.rowconfigure(i, weight=1, minsize=50)
       
    
    # Loop over images
    # Create buttons
    # button_1 = customtkinter.CTkButton(master = root, text="Add Python File", width = 190, height = 40, corner_radius = 20)
    # button_1.pack(pady = 20, padx = 20)
    # button_1 .place(x = 10, y = 20)
    # button_2 = customtkinter.CTkButton(master = root, text="Add Image", width = 190, height = 40, fg_color = "#D35B58", hover_color = "#C77C78")
    # button_2.pack(pady = 10, padx = 20)

    my_img1 = Image.open(r'S:\LeeTran\Planning\Technology\Python Projects\Bonita Springs Ultra GUI App\Final status of unique trips.jpg')
    # my_img1 = my_img1.resize((my_img1.width // 4, my_img1.height // 4))
    # my_img1 = resizeimage.resize_cover(my_img1, [1200, 600])
    my_img1 = my_img1.resize((1200, 600))
    # my_img1.show()
    my_img1 = ImageTk.PhotoImage(my_img1)

    my_img2 = Image.open(r'S:\LeeTran\Planning\Technology\Python Projects\Bonita Springs Ultra GUI App\1-seat trip vs 2-seats trip.jpg')
    # my_img2 = my_img2.resize((my_img2.width // 4, my_img2.height // 4))
    # my_img2 = resizeimage.resize_cover(my_img2, [1200, 600])
    my_img2 = my_img2.resize((1200, 600))
    # my_img2.show()
    my_img2 = ImageTk.PhotoImage(my_img2)

    my_img3 = Image.open(r'S:\LeeTran\Planning\Technology\Python Projects\Bonita Springs Ultra GUI App\Seats requested vs completed.jpg')
    # my_img3 = my_img3.resize((my_img3.width // 4, my_img3.height // 4))
    # my_img3 = resizeimage.resize_cover(my_img3, [1200, 600])
    my_img3 = my_img3.resize((1200, 600))
    # my_img3.show()
    my_img3 = ImageTk.PhotoImage(my_img3)

    my_img4 = Image.open(r'S:\LeeTran\Planning\Technology\Python Projects\Bonita Springs Ultra GUI App\Matched unique trips.jpg')
    # my_img4 = my_img4.resize((my_img4.width // 4, my_img4.height // 4))
    # my_img4 = resizeimage.resize_cover(my_img4, [1300, 700])
    my_img4 = my_img4.resize((1200, 600))
    # my_img4.show()
    my_img4 = ImageTk.PhotoImage(my_img4)

    my_img5 = Image.open(r'S:\LeeTran\Planning\Technology\Python Projects\Bonita Springs Ultra GUI App\Unique trip status by time of the day - Weekdays.jpg')
    # my_img5 = my_img5.resize((my_img5.width // 4, my_img5.height // 4))
    # my_img5 = resizeimage.resize_cover(my_img5, [1300, 700])
    my_img5 = my_img5.resize((1200, 600))
    # my_img5.show()
    my_img5 = ImageTk.PhotoImage(my_img5)

    my_img6 = Image.open(r'S:\LeeTran\Planning\Technology\Python Projects\Bonita Springs Ultra GUI App\Unique trip status by time of the day - Weekends.jpg')
    # my_img6 = my_img6.resize((my_img6.width // 4, my_img6.height // 4))
    # my_img6 = resizeimage.resize_cover(my_img6, [1300, 700])
    my_img6 = my_img6.resize((1200, 600))
    # my_img6.show()
    my_img6 = ImageTk.PhotoImage(my_img6)

    # my_img7 = Image.open(r'S:\LeeTran\Planning\Technology\Python Projects\Bonita Springs Ultra GUI App\Final status of unique daily trips for last 30-days.jpg')
    # my_img7 = my_img7.resize((1200, 600))
    # my_img7 = ImageTk.PhotoImage(my_img7)

    # my_img8 = Image.open(r'S:\LeeTran\Planning\Technology\Python Projects\Bonita Springs Ultra GUI App\1-seat trip vs 2-seats daily trip for last 30-days.jpg')
    # my_img8 = my_img8.resize((1200, 600))
    # my_img8 = ImageTk.PhotoImage(my_img8)

    # my_img9 = Image.open(r'S:\LeeTran\Planning\Technology\Python Projects\Bonita Springs Ultra GUI App\Matched unique daily trips for last 30-days.jpg')
    # my_img9 = my_img9.resize((1200, 600))
    # my_img9 = ImageTk.PhotoImage(my_img9)

    my_img7 = Image.open(r'S:\LeeTran\Planning\Technology\Python Projects\Bonita Springs Ultra GUI App\Final status of unique monthly trips.jpg')
    my_img7 = my_img7.resize((1200, 600))
    my_img7 = ImageTk.PhotoImage(my_img7)

    my_img8 = Image.open(r'S:\LeeTran\Planning\Technology\Python Projects\Bonita Springs Ultra GUI App\1-seat trip vs 2-seats monthly trip.jpg')
    my_img8 = my_img8.resize((1200, 600))
    my_img8 = ImageTk.PhotoImage(my_img8)

    my_img9 = Image.open(r'S:\LeeTran\Planning\Technology\Python Projects\Bonita Springs Ultra GUI App\Matched unique monthly trips.jpg')
    my_img9 = my_img9.resize((1200, 600))
    my_img9 = ImageTk.PhotoImage(my_img9)
    
    # customizing images start from here
    my_img10 = Image.open(r'S:\LeeTran\Planning\Technology\Python Projects\Bonita Springs Ultra GUI App\Customizing the date range for final status of unique daily trips.jpg')
    # my_img10 = my_img10.resize((my_img10.width // 4, my_img10.height // 4))
    # my_img10 = resizeimage.resize_cover(my_img10, [1300, 700])
    my_img10 = my_img10.resize((1200, 600))
    my_img10 = ImageTk.PhotoImage(my_img10)
    
    my_img11 = Image.open(r'S:\LeeTran\Planning\Technology\Python Projects\Bonita Springs Ultra GUI App\Customizing unique trip status by time of the day - Weekdays.jpg')
    # my_img11 = my_img11.resize((my_img11.width // 4, my_img11.height // 4))
    # my_img11 = resizeimage.resize_cover(my_img11, [1300, 700])
    my_img11 = my_img11.resize((1200, 600))
    my_img11 = ImageTk.PhotoImage(my_img11)
    
    my_img12 = Image.open(r'S:\LeeTran\Planning\Technology\Python Projects\Bonita Springs Ultra GUI App\Customizing unique trip status by time of the day - Weekends.jpg')
    # my_img12 = my_img12.resize((my_img12.width // 4, my_img12.height // 4))
    # my_img12 = resizeimage.resize_cover(my_img12, [1300, 700])
    my_img12 = my_img12.resize((1200, 600))
    my_img12 = ImageTk.PhotoImage(my_img12)
  
    my_img13 = Image.open(r'S:\LeeTran\Planning\Technology\Python Projects\Bonita Springs Ultra GUI App\Customizing Seats requested vs completed.jpg')
    # my_img13 = my_img13.resize((my_img13.width // 4, my_img13.height // 4))
    # my_img13 = resizeimage.resize_cover(my_img13, [1300, 700])
    my_img13 = my_img13.resize((1200, 600))
    my_img13 = ImageTk.PhotoImage(my_img13)
    
    my_img14 = Image.open(r'S:\LeeTran\Planning\Technology\Python Projects\Bonita Springs Ultra GUI App\Customizing 1-seat vs 2-seats daily trip.jpg')
    # my_img14 = my_img14.resize((my_img14.width // 4, my_img14.height // 4))
    # my_img14 = resizeimage.resize_cover(my_img14, [1300, 700])
    my_img14 = my_img14.resize((1200, 600))
    my_img14 = ImageTk.PhotoImage(my_img14)
    
    my_img15 = Image.open(r'S:\LeeTran\Planning\Technology\Python Projects\Bonita Springs Ultra GUI App\Customizing matched unique daily trips.jpg')
    # my_img15 = my_img15.resize((my_img15.width // 4, my_img15.height // 4))
    # my_img15 = resizeimage.resize_cover(my_img15, [1300, 700])
    my_img15 = my_img15.resize((1200, 600))
    my_img15 = ImageTk.PhotoImage(my_img15)


    image_list = [my_img1, my_img2, my_img3, my_img4, my_img5, my_img6, my_img7, my_img8, my_img9, my_img10, my_img11, my_img12, my_img13, my_img14, my_img15]
    
    my_label = tk.Label(pop, image = my_img1)
    my_label.grid(row=0, column=0, columnspan=3)
    
    
    def forward():
        global pop
        global my_label
        global img_index
        global button_forward
        global button_back
        
        my_label.grid_forget()
        img_index += 1
        
        my_label = tk.Label(pop, image=image_list[img_index])
        button_forward = tk.Button(pop, text = ">>", command = forward)
        button_back = tk.Button(pop, text = "<<", command = back)
        
        if img_index  == 14:
            button_forward = tk.Button(pop, text = ">>", state=tk.DISABLED)
        
        my_label.grid(row=0, column=0, columnspan=3)
        what_text = tk.StringVar()
        what_text.set("Image  " + str(img_index + 1) + " out of  " + str(len(image_list)))
        what_img = tk.Label(pop, textvariable = what_text, font=("shanti", 12), fg="#9955bb")
        
        
        button_back.grid(row=1, column=0)
        what_img.grid(row=1, column=1)
        button_forward.grid(row=1, column=2)


    def back():
        global pop
        global my_label
        global img_index
        global button_forward
        global button_back
        
        my_label.grid_forget()
        img_index -= 1
        
        my_label = tk.Label(pop, image=image_list[img_index])
        button_forward = tk.Button(pop, text = ">>", command = forward)
        button_back = tk.Button(pop, text = "<<", command = back)
        
        if img_index  == 0:
            button_back = tk.Button(pop, text = "<<", state=tk.DISABLED)
        
        my_label.grid(row=0, column=0, columnspan=3)
        what_text = tk.StringVar()
        what_text.set("Image  " + str(img_index + 1) + " out of  " + str(len(image_list)))
        what_img = tk.Label(pop, textvariable = what_text, font=("shanti", 12), fg="#9955bb")
          
        button_back.grid(row=1, column=0)
        what_img.grid(row=1, column=1)
        button_forward.grid(row=1, column=2)
        
    button_back = tk.Button(pop, text = "<<", command = back, state=tk.DISABLED)
    button_forward = tk.Button(pop, text = ">>", command = forward)
    
    what_text = tk.StringVar()
    what_text.set("Image   " + str(img_index + 1) + " out of  " + str(len(image_list)))
    what_img = tk.Label(pop, textvariable = what_text, font=("shanti", 12), fg="#9955bb")
    

    button_back.grid(row=1, column=0)
    what_img.grid(row=1, column=1, sticky="ew")
    button_forward.grid(row=1, column=2)


# Set up logo positions
logo1 = Image.open(r'S:\LeeTran\Planning\Technology\Python Projects\Bonita Springs Ultra GUI App\pic\resized LeeTran logo png.png')
logo1 = ImageTk.PhotoImage(logo1)
logo1_label = tk.Label(image=logo1)
logo1_label.image = logo1 # cannot skip this line of code, it's necessary
logo1_label.grid(row=4, column=0, padx=10, pady=10)

# Fit multiple buttons in one grid cell
gridframe = tk.Frame(root, bg="#6897bb") # notes: need set-up another frame
gridframe.grid(row=4, column=1, sticky="nsew")

py_btn = tk.Button(gridframe, text="Run Python File", font = ("shati"), command=check, bg='#26619c', fg='white')
py_btn_Font = font.Font(weight="bold")
py_btn['font'] = py_btn_Font 
py_btn.grid(row=0, column=0, padx=20, pady=10)

img_btn = tk.Button(gridframe, text = "Check Images", font = ("shati"), command=clicker, bg="#26619c", fg='white')
img_btn_Font = font.Font(weight="bold")
img_btn['font'] = img_btn_Font 
img_btn.grid(row=0, column=1, padx=20, pady=10)

# Instructions
instro_title = tk.Label(root, text = " Image List", font=("shati"), bg="#6897bb") # bg="#a1caf1"
instro_title_Font = font.Font(weight="bold", size=12)
instro_title['font'] = instro_title_Font 
instro_title.grid(row=5, column=0, columnspan=2)

instro = tk.Label(root, 
                  text = " Image 1: Final Status of Unique Trip \n Image 2: 1-Seat Trip vs 2-Seats Trip \n Image 3: Seats Requested vs Completed Trips \n Image 4: Matched vs Unmatched Trip \n Image 5: Unique Trip Status by Time of the Day - Weekdays \n Image 6: Unique Trip Status by Time of the Day - Weekends \n Image 7-9: Monthly Trip Presentation \n Image 10+: Customize", 
                  font=("shati", 12), bg="#6897bb") # bg="#a1caf1"
instro.grid(row=6, column=0, columnspan=2)


root.mainloop()


# convert py to exe
# auto-py-to-exe