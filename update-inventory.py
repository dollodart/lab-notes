"""

Allowing the student to specify by any way (mass/volume/mole) in the template, the total use is updated.

"""
import matplotlib.pyplot as plt
import pandas as pd
from utils.env import LABNOTES, SUMMARIES
from utils.date_iter import date_iter
from templates.readers import read_ReagentTemplate
from pathlib import Path

prefixes = {'u': 1e-6, 'm': 1e-3, '': 1, 'k': 1e3}
units = {'L': 'volume', 'g': 'mass', 'mol': 'number'}
dmag = {}
for kp, vp in prefixes.items():
    for ku, vu in units.items():
        dmag[kp + ku] = (vu, vp)

# merge inventory on chemical data needed for updating the use
inv = pd.read_excel(f'{SUMMARIES}/inventory.xlsx', sheet_name='Inventory')
cd = pd.read_excel(f'{SUMMARIES}/inventory.xlsx', sheet_name='Chemical Data')
tdf = pd.merge(
    cd,
    inv,
    how='inner',
    left_on='Name',
    right_on='Consumable Name')
tdf = tdf.set_index('ID')

# iterate through all uses
dfs = []
for d in date_iter:
    try:
        p = Path(f'{LABNOTES}/{d}')
        for i in p.iterdir():
            if str(i.name).startswith('ReagentTemplate'):
                df = read_ReagentTemplate(str(i))
                df['Date'] = d
                dfs.append(df)
    except FileNotFoundError as e:
        continue

df = pd.concat(dfs, ignore_index=True)
r = pd.merge(
    df,
    tdf,
    how='inner',
    left_on='ID',
    right_index=True,
    suffixes=(
        'Use',
        'Capacity'))

# convert the student report units to the units used for capacity

amount = []
for k, s in r.iterrows():
    uu = s.loc['UnitUse']
    uc = s.loc['UnitCapacity']
    du, factor = dmag[uu]
    dc, factorc = dmag[uc]

    assert cd.iloc[0]['Molar Mass'] == 'g/mol'
    assert cd.iloc[0]['Standard Conditions Density'] == 'g/mL'

    if du == 'volume':
        factor /= 1000
    if dc == 'volume':
        factorc *= 1000

    if du == 'volume' and dc == 'number':
        factor *= s.loc['Standard Conditions Density'] / s.loc['Molar Mass']
    elif du == 'volume' and dc == 'mass':
        factor *= 1. / s.loc['Standard Conditions Density']
    elif du == 'number' and dc == 'volume':
        factor *= s.loc['Molar Mass'] / s.loc['Standard Conditions Density']
    elif du == 'number' and dc == 'mass':
        factor *= s.loc['Molar Mass']
    elif du == 'mass' and dc == 'volume':
        factor *= 1. / s.loc['Standard Conditions Density']
    elif du == 'mass' and dc == 'number':
        factor *= 1. / s.loc['Molar Mass']
    print(uu, uc, factor/factorc)
    amount.append(s.loc['AmountUse'] * factor / factorc)

r['AmountUse'] = amount
# r['UnitUse'] = r['UnitCapacity'] # unnecessary

r2 = r.groupby('ID').agg('sum')
inv = inv.set_index('ID')
inv['Use'] = r2['AmountUse']

# use openpyxl to preserve the formatting and only substitute the data
# https://openpyxl.readthedocs.io/en/stable/pandas.html
with pd.ExcelWriter(f'{SUMMARIES}/inventory.xlsx') as writer:
    inv.to_excel(writer, sheet_name='Inventory')
    cd.to_excel(writer, sheet_name='Chemical Data', index=False)

for n, gr in r.groupby('Name'):
    plt.figure()
    plt.plot(gr['Date'], gr['AmountUse'].cumsum())
    plt.title(n)
    plt.show()
