from datetime import datetime, timedelta
import os
from pathlib import Path
import pandas as pd
import yaml
from Cheetah.Template import Template
from pypandoc import convert_file
from utils.env import HOME, LABNOTES, SUMMARIES, TEMPLATES
from utils.date_iter import date_iter, date1, date2

# spreadsheet data from summaries
wb = load_workbook('summaries/record.xlsx')
ws1 = wb['Sheet1']
data = [row for row in ws1.values]
df = pd.DataFrame(data[1:], columns=data[0])
df = df[df.columns[~df.columns.isna()]]
df['Date Start'] = pd.to_datetime(df['Date Start'])

# dictionary data from summaries
with open("summaries/record.yaml", "rb") as read_buffer:
    dct = yaml.load(read_buffer, Loader=yaml.Loader)
df2 = pd.DataFrame(dct)
df2['Date Start'] = pd.to_datetime(df2['Date Start'])

# load templates

l = []
for i in 'main', 'section', 'table', 'image':
    with open(f'{TEMPLATES}/{i}.cheetah', 'r') as _:
        l.append(Template.compile(_.read(), baseclass=dict))

main, section, table, image = l

# file extensions
tbs = ['.xlsx', '.ods']
imgs = ['.png', '.jpg', '.jpeg']
# these would be yaml files with the same data structure and keys
specials = ['.xlsx_instr']
ref = {}

document = ''  # string to which templates are concatenated
for d in date_iter:
    ln = Path(f'{LABNOTES}/{d}/lab-notes.md')
    if not ln.exists():
        continue
    # copy the plain text lab notes file
    print(ln)
    contents = convert_file(ln.as_posix(), 'latex')
    from pylatexenc.latexencode import unicode_to_latex
    contents = unicode_to_latex(contents, non_ascii_only=True)
    document += section(date=d, contents=contents).respond()
    # time matching the summary files with the given date for spreadsheets
    check = df['Date Start'] == d
    if check.any():
        document += '\\subsection{Cross-Reference}'
        document += '\n\n{\\footnotesize\n' + df[check].to_latex() + '}'
    # time matching dictionary
    check = df2['Date Start'] == d
    if check.any():
        s = df2[check]
        document += '\\subsection{Cross-Reference}'
        document += '\n\n{\\footnotesize\n' + df2[check].to_latex() + '}'

    # writing tables, images, and special data files

    for fl in ln.parent.iterdir():
        suff = fl.suffix
        if suff == '.md':
            continue
        if suff in tbs:
            wsets = pd.read_excel(
                str(fl),
                sheet_name=None,
                usecols='A:F',
                nrows=80)
            for sname, dfi in wsets.items():
                if len(dfi) > 0:
                    #                    dfi = dfi.dropna(how='all', axis=1)
                    #                    dfi = dfi.dropna(how='all', axis=0)
                    dfi_l = dfi.to_latex()
                    footnotesize = len(dfi.columns) > 6
                    document += table(label=fl.with_suffix('').name,
                                      caption=fl.with_suffix(
                                          '').name + ':' + sname,
                                      footnotesize=footnotesize,
                                      table=dfi_l).respond()
                else:
                    print(
                        f'empty sheet in table {fl} in directory {d} is ignored')
        elif suff in imgs:
            document += image(label=fl.with_suffix('').name,
                              caption=fl.with_suffix('').name,
                              file_name=fl).respond()
        elif suff == '.xlsx_instr':
            from templates.readers import read_xlsx_instr
            dfspec = read_xlsx_instr(str(fl))
            dfl = dfspec.to_latex()
            document += table(label=fl.with_suffix('').name,
                              caption='MFC Calibration',
                              footnotesize=False,
                              table=dfl).respond()
        else:
            print(
                f'Unrecognized file extension {suff} in file {fl} of directory {d} is ignored')
        document += '\\newpage'

index_words = ['Lorem', 'Ipsum']
index_words = set([i.lower() for i in index_words] +
                  [i.capitalize() for i in index_words])
hasindex = True if len(index_words) > 0 else False
with open('log_file.tex', 'w') as write_file:
    for i in index_words:
        document = document.replace(i, f'{i}\\index{{{i}}}')
    write_file.write(
        main(
            date1=date1,
            date2=date2,
            body=document,
            hasindex=hasindex).respond()
    )
