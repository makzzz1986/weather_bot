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
#api['list'] = api['list']
#api['list'] = api['list'][:13]
#api['list'] = api['list'][:30]

#for point in api['list']:
#    print(round(point['main']['temp']-273))

temps = [ round(t['main']['temp']-273) for t in api['list'] ]

dates = []
for date in [ d['dt'] for d in api['list'] ]:
    dates.append(convert_to_MSK_tz(date))


texts = [ tx['weather'][0]['description'] for tx in api['list'] ]

textposition = []
counter = 0
for t in temps[:-1]:
    if temps[counter+1] > t:   # if next temp will be higher than current, text should be lower
        textposition.append('bottom left')
    else:
        textposition.append('top left')
    counter += 1 
#print(textposition)


temp_min = min(temps)

#                'x': 0.03 + api['list'].index(ico)*0.0735,
#                'x': 0.03 + api['list'].index(ico)*0.91/len(api['list']),
# x 0.955 for 13 units
# x 0.91 for 40 units
# Generate list with dicts
images_ico = [ {'sizex': 0.1, 
                'sizey': 0.1, 
                'x': 0.03 + count*0.91/len(api['list']),
                'y': 1 + 0.06*(count%2),
                'xref': 'paper', 
                'yref': 'paper', 
                'xanchor': 'left',
                'yanchor': 'bottom',
                'source': 'http://openweathermap.org/img/w/{}.png'.format(api['list'][count]['weather'][0]['icon'])} for count in range(len(api['list'])) ]
print(images_ico)

# Try annotations
annotations = [{'xref': 'x',
                'yref': 'y',
                'showarrow': True,
                'arrowhead': 0,
                'ax': -5,
                'ay': 20,
                'textangle': 90,
                'x': dates[count],
                'y': temps[count],
                'text': texts[count]} for count in range(len(api['list']))]
#print(annotations)

#    msk_tz = convert_to_MSK_tz(date)
#    if last_date != msk_tz.split()[1]:
#        last_date = msk_tz.split()[1]
#        dates.append(msk_tz)
#    else:
#        dates.append(msk_tz.split()[0] + ' '*10)

#print(dates)
#print(temps)

#data = [{'x':dates, 
#         'y':temps, 
#         'text':texts, 
#         'textposition': textposition,
#         'mode':'lines+markers+text'}]

data = [{'x':dates, 
         'y':temps, 
         'mode':'lines+markers+text'}]

layout = go.Layout(title='Прогнозец',
                   images=images_ico, 
                   annotations=annotations,
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

fig = go.Figure(data=data, layout=layout)

pio.write_image(fig, 'chart.png')

