from date_iter import date_iter
from env import LABNOTES
from pathlib import Path
name_part = ''
file_extension = 'jpg'

for d in date_iter:
    try:
        p = Path(f'{LABNOTES}/{d}')
        for file in p.iterdir():
            file = str(file)
            if name_part in file and file.endswith(file_extension):
                print('↓' * 72)
                print(d)
                print(file)
                print('↑' * 72)
            else:
                continue
    except FileNotFoundError:
        pass
