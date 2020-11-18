"""

Templated Excel sheets often are in a form which is convenient for
the user to interact with but not ideal to be read directly as a
dataframe. Hence these reader functions allow templated excel sheets to
be manipulated into dataframes. This can include removing columns (e.g.,
unnecessary columns or computational columns not exposed to the user),
removing (summary rows or comment rows), and transposing.

"""
import pandas as pd
from time import time


def read_ReagentTemplate(fname):
    df = pd.read_excel(fname, sheet_name='Reagents', usecols='A:F', nrows=80)
    dft = df.transpose()
    dft.columns = dft.iloc[0]
    dft = dft.drop('Alias')
    dft['Amount'] = dft['Amount'].astype(float)
    return dft


udct = {
    'Volume': 'mL',
    'Time': 's',
    'Measured Rate': 'sccm',
    'Setpoint': 'sccm'}


def read_xlsx_instr(filename, verbose=False, usecols='A:E', skipfooter=80):
    l = tuple()
    t0 = time()
    dfs = pd.read_excel(filename, sheet_name=None)
    if verbose:
        print(f'{time() - t0} time to read file')
    t0 = time()

    for mfc, df in dfs.items():
        df = df[['Volume', 'Time', 'Measured Rate', 'Setpoint']]
        try:
            x = df.iloc[0]
            assert x.to_dict() == udct
            df = df.drop(0)
            df = df.dropna()
            df['MFC'] = mfc
            l += (df,)
        except IndexError:
            print(f'No data for {mfc}')
            pass
        except AssertionError:
            raise Exception(f"do not support units other than {udct}\n"
                            f"got {x}")
    if verbose:
        print(f'{time() - t0} time to process file')

    return pd.concat(l)
