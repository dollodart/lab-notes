from date_iter import date_iter
from env import LABNOTES
import re

pattern = 'observation'

for d in date_iter:
    try:
        with open(f'{LABNOTES}/{d}/lab-notes.md', 'r') as _:
            lines = _.readlines()
        for line in lines:
            if re.match(pattern, line) is not None:
                print('↓' * 72)
                print(d)
                print(line)
                print('↑' * 72)
    except FileNotFoundError as e:
        pass
