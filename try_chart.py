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

# change days to observe
api['list'] = api['list'][:13]

#for point in api['list']:
#    print(round(point['main']['temp']-273))

temps = [ round(t['main']['temp']-273) for t in api['list'] ]

dates = []
last_date = ''
for date in [ d['dt'] for d in api['list'] ]:
    dates.append(convert_to_MSK_tz(date))


texts = [ tx['weather'][0]['main'] for tx in api['list'] ]
temp_min = min(temps)

# Generate list with dicts
images_ico = [ {'sizex': 0.1, 
                'sizey': 0.1, 
                'x': 0.03 + api['list'].index(ico)*0.0735,
                'y': 1 + api['list'].index(ico)*0,
                'xref': 'paper', 
                'yref': 'paper', 
                'xanchor': 'left',
                'yanchor': 'bottom',
                'source': 'http://openweathermap.org/img/w/{}.png'.format(ico['weather'][0]['icon'])} for ico in api['list'] ]
#print(images_ico)

#    msk_tz = convert_to_MSK_tz(date)
#    if last_date != msk_tz.split()[1]:
#        last_date = msk_tz.split()[1]
#        dates.append(msk_tz)
#    else:
#        dates.append(msk_tz.split()[0] + ' '*10)

#print(dates)
#print(temps)

data = [{'x':dates, 'y':temps, 'text':texts, 'mode':'lines+markers+text'}]
#data = [{'x':dates[:24], 'y':temps[:24], 'mode':'lines+markers'}]

layout = go.Layout(title='Прогнозец',
                   images=images_ico, 
                   xaxis=dict(
                              title='Время и дни', 
                              ticks='outside', 
                              showticklabels=True,
                              tickangle=75,
                              tickwidth=2, 
                              showgrid=True, 
                              showline=True,
                              gridcolor='#bdbdbd',
                              gridwidth=1, 
                              mirror='ticks'
                              ), 
                   yaxis=dict(
                              title='Градусы цельсия',
                              ticks='outside',
                              tickwidth=2, 
                              showgrid=True,
                              showline=True, 
                              gridcolor='#bdbdbd',
                              gridwidth=1,
                              mirror='ticks'
                              ))

#layout = go.Layout(title='Прогнозец', 
#                   xaxis=dict(
#                              title='Время и дни', 
#                              ticks='outside', 
#                              showticklabels=True,
#                              tickangle=75,
#                              tickwidth=2, 
#                              showgrid=True, 
#                              showline=True,
#                              gridcolor='#bdbdbd',
#                              gridwidth=1, 
#                              mirror='ticks'
#                              ), 
#                   yaxis=dict(
#                              title='Градусы цельсия',
#                              ticks='outside',
#                              tickwidth=2, 
#                              showgrid=True,
#                              showline=True, 
#                              gridcolor='#bdbdbd',
#                              gridwidth=1,
#                              mirror='ticks'
#                              ))
#layout = go.Layout(title='Прогнозец', xaxis={'title': 'Dates', 'ticks': 'outside', 'showticklabels': True, 'tickangle': 75}, yaxis={'title': 'Celsium'})

fig = go.Figure(data=data, layout=layout)

pio.write_image(fig, 'chart.png')

