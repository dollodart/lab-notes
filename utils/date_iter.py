from datetime import datetime, timedelta
date1 = '2019-10-01'
date2 = '2019-10-31'
date1 = datetime.strptime(date1, '%Y-%m-%d')
date2 = datetime.strptime(date2, '%Y-%m-%d')
td = (date2 - date1).days
d1 = timedelta(days=1)
date_iter = ((date1 + i * d1).strftime('%Y-%m-%d') for i in range(td))
