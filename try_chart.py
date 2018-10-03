import json

import plotly.offline as offline
#from plotly.offline import iplot, init_notebook_mode
import plotly.graph_objs as go
import plotly.io as pio

import os
import datetime


def convert_to_MSK_tz(timestamp):
    msk = datetime.datetime.fromtimestamp(timestamp+60*60*3)
    return msk.strftime('%H %A')
    #return msk.strftime('%H %Y-%M-%d')

with open('result.txt', 'r') as result:
    api = json.loads(result.read())

#for point in api['list']:
#    print(round(point['main']['temp']-273))

temps = [ round(t['main']['temp']-273) for t in api['list'] ]
dates = []
last_date = ''

for date in [ d['dt'] for d in api['list'] ]:
    msk_tz = convert_to_MSK_tz(date)
    if last_date != msk_tz.split()[1]:
        last_date = msk_tz.split()[1]
        dates.append(msk_tz)
    else:
        dates.append(msk_tz)
        #dates.append(msk_tz.split()[0] + ' '*10)

print(dates)
print(temps)

data = [{'x':dates, 'y':temps, 'mode':'lines'}]
#data = [go.Scatter(x=dates, y=temps, mode='lines')]

layout = go.Layout(title='Прогнозец', xaxis={'title': 'Dates', 'ticks': 'outside', 'showticklabels': True, 'tickangle': 75}, yaxis={'title': 'Celsium'})

fig = go.Figure(data=data, layout=layout)

pio.write_image(fig, 'chart.png')

