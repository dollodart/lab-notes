"""

Look at calibration data over time, possible instrument or sensor drift.

"""

import pandas as pd
from utils.env import LABNOTES, SUMMARIES
from utils.date_iter import date_iter
from templates.readers import read_xlsx_instr
from pathlib import Path
import matplotlib.pyplot as plt
from scipy.stats import linregress
from time import time

dfs = []
for d in date_iter:
    try:
        p = Path(f'{LABNOTES}/{d}')
        for i in p.iterdir():
            if str(i.name).endswith('xlsx_instr'):
                df = read_xlsx_instr(str(i), verbose=True)
                df['Date'] = d
                dfs.append(df)
                print(f'data instrument calibration on {d} found')
    except (FileNotFoundError, ZeroDivisionError) as e:
        continue

df = pd.concat(dfs, ignore_index=True)
for n, gr in df.groupby('MFC'):
    xy = []
    for nn, ggr in gr.groupby('Date'):
        # scipy linregress throws exceptions on non-built-in object types
        x = list(float(x) for x in ggr['Setpoint'].values)
        y = list(float(x) for x in ggr['Measured Rate'].values)
        if len(ggr) > 1:
            s, i, r, p, std = linregress(x, y)
            xy.append((nn, s, i, r))
        else:
            print(f'date {nn} no data')

    x, s, i, r = zip(*xy)
    fig, axs = plt.subplots(nrows=3, ncols=1, sharex=True)
    axs[0].plot(x, s)
    axs[0].set_ylabel('Calibration Slope')
    axs[1].plot(x, i)
    axs[1].set_ylabel('Calibration Intercept')
    axs[2].plot(x, r)
    axs[2].set_ylabel('Calibration $R^2$')
plt.show()
