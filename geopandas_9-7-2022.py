# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 10:49:45 2022

@author: xiw
"""

# Title: Plotting Ultra (On Demand Transit) graph GUI desktop app development
# Contact: wxi@leegov.com
# Author: Wang Xi
# Last Updated: 09-07-2022

# Update notes: plotting geographic data with latitude and longitude on a map
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

import numpy
import pandas
import geopandas as gpd
# import pysal
import seaborn
import contextily
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from shapely.geometry import Point, Polygon
import descartes


# Set up directory
os.chdir(r'S:\LeeTran\Planning\Intern\Wang Xi\LeeTran_Wang\Bonita Springs Ultra GUI App')
os.getcwd()
df = pd.read_excel('Ultra_data.xlsx')
# df.info()

# Generate scatter plot
pick_up = seaborn.jointplot(x="Pickup Long", y="Pickup Lat", data=df, s=0.5)
plt.savefig(r'S:\LeeTran\Planning\Technology\Python Projects\Bonita Springs Ultra GUI App\Pick-up Geolocation Patterns as Dots on a Map.jpg', dpi=300,bbox_inches='tight')

drop_off = seaborn.jointplot(x="Dropoff Long", y="Dropoff Lat", data=df, s=0.5)
plt.savefig(r'S:\LeeTran\Planning\Technology\Python Projects\Bonita Springs Ultra GUI App\Drop-off Geolocation Patterns as Dots on a Map.jpg', dpi=300,bbox_inches='tight')


major_roads = gpd.read_file(r'C:\Users\xiw\Documents\ArcGIS\Projects\Ultra Ridership Analysis\major_roads.shp')

fig, ax = plt.subplots(figsize = (15,15))
major_roads.plot(ax = ax)