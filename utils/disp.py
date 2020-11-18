from date_iter import date_iter
from env import LABNOTES
for d in date_iter:
    try:
        with open(f'{LABNOTES}/{d}/lab-notes.md') as _:
            file = _.read()
        print('↓' * 72)
        print(d)
        print(file)
        print('↑' * 72)
    except FileNotFoundError:
        pass
