
# Bonita Spring Ultra Mobility-On-Demand GUI App Development

The app is basically analyzing *Ultra MoD (Mobility On Demand) Data*'s perfomance daily, monthly, annually and with customizing the specific date range. 
The **purpose** of developing this app is to check over Ultra MoD service perfomance, such as passengers' requests type, seat completion, number of trips, peak trip request during the day by the time of wekkday & weekend.



## File Format

This project is used by the following file formats:

- **ultra data excel file**, which is downloaded from *Ultra Dashboard (copy right from LeeTran)*


## Deployment

To deploy this project run, the following modules are needed to be imported as belows.

```bash
import os
import pandas as pd
import datetime
from datetime import timedelta, datetime
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
```

To convert .py into .exe, copy the following command onto your Anaconda Prompt
```bash
auto-py-to-exe
```


## Repository Structure

#### Update key notes:

- (1) customtkinter couldn't work on .ipynb
- (2) detect the most last 30-days daily trip, monthly trips & customizing the specific date range
- (3) constraint all images into the same size
- (4) change the range of the x-axis with datetimes and remove back (2022 Oct data is special)


| File Name | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `Ultra GUI_11-21-2022` | `.py` | **Required**. It is the main file, updated to 3rd version |

#### Other supplementary files description

```http
Since Ultra data includes private passenger information, ultra data excel file cannot be shared over here.
```

| File Name | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `x-axis datetime change`      | `.py` | **Test file** for the purpose of verifying seaborn image x-axis|
| `geopandas_9-7-2022`      | `.py` | **Test file** for the purpose of spatial analysis|
| `file_path_trial_Ultra GUI_8-19-2022`      | `.py` | **Test file** for the purpose of testing whether it would work after changing path|



## Author

- [@xw0413happy](https://github.com/xw0413happy)


## 🚀 About Me
I took 2 python classes during my M.S. degree-seeking program (Civil Engineering), now I am a computer language amateur, strong desire to learn more.


## 🛠 Skills
Python, R, SQL, ArcGIS, Nlogit, Stata, Power BI, Javascript, HTML, CSS, Synchro, Vissim, AutoCAD, Tableau, VBA


## Acknowledgements

 - [LeeTran Ultra](https://www.leegov.com/leetran/about-leetran/current-projects/ultra)
 - [LeeTran Ultra/Uber](https://www.leegov.com/leetran/ultra/ultra-uber)

