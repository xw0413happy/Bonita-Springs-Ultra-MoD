
# Probing Check GUI Desktop App

The app is basically analyzing *two separate files* to check over each other and generate a text document probe check report. 
The **purpose** of developing this app is to target which fixed route buses are not probed and which dates are their last time probing.



## File Format

This project is used by the following file formats:

- **probing summary csv file**, which is downloaded from *GenFare*
- **daily operation log folder**, which is provided by *LeeTran Operdation Department*


## Deployment

To deploy this project run, the following modules are needed to be imported as belows.

```bash
import pandas as pd
import os
import math
import datetime
from datetime import datetime
from contextlib import redirect_stdout
import tkinter as tk
import tkinter.font as font
from tkinter import filedialog
from PIL import Image, ImageTk
```

To convert .py into .exe, copy the following command onto your Anaconda Prompt
```bash
auto-py-to-exe
```



## Repository Structure

#### Update key notes:


- (1) only pick up 3-digit Bus number
- (2) remove text in stand-by list 
- (3) remove '/' and ' / " from stand_by_list


| File Name | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `ProbeCheck_V4` | `.py` | **Required**. It is the main file, updated to 4th version |

#### Other supplementary files description

```http
All uploaded .xlsm files are used for testing.
```

| File Name | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `test for opt logs hurr ian`      | `.py` | **Test file** |




## Author

- [@xw0413happy](https://github.com/xw0413happy)


## 🚀 About Me
I took 2 python classes during my M.S. degree-seeking program (Civil Engineering), now I am a computer language amateur, strong desire to learn more.


## 🛠 Skills
Python, R, SQL, ArcGIS, Nlogit, Stata, Power BI, Javascript, HTML, CSS, Synchro, Vissim, AutoCAD, Tableau, VBA


## Acknowledgements

 - [LeeTran](https://www.leegov.com/leetran/how-to-ride/maps-schedules)
 - [Learn more about how to loop over images by using Python Tkinter](https://www.youtube.com/watch?v=NoTM8JciWaQ&t=565s)
 - [Genfare](https://www.genfare.com/products/)

