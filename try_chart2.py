import json
import matplotlib.pyplot as plt

import os
import datetime


def convert_to_MSK_tz(timestamp):
    msk = datetime.datetime.fromtimestamp(timestamp+60*60*3)
    days= {'Monday': 'Пн',
           'Tuesday': 'Вт',
           'Wednesday': 'Ср',
           'Thursday': 'Чт',
           'Friday': 'Пт',
           'Saturday': 'Сб',
           'Sunday': 'Вс'}
    return msk.strftime('%H')+' '+days[msk.strftime('%A')]

with open('result.txt', 'r') as result:
    api = json.loads(result.read())

temps = [ round(t['main']['temp']-273) for t in api['list'] ]

texts = [ tx['weather'][0]['description'] for tx in api['list'] ]

dates = []
for date in [ d['dt'] for d in api['list'] ]:
    dates.append(convert_to_MSK_tz(date))

# PLOT

fig, graph = plt.subplots()
graph.plot(dates, temps)
graph.grid(True)
graph.set_xlabel('Дни')
graph.set_ylabel('Цельсии')


fig.tight_layout()
#plt.show()
plt.savefig('chart_plt.png')
