import json
import matplotlib.pyplot as plt
import matplotlib.image as img

import os
import datetime
import math


def get_wind_chill(temp, wind_speed):
    wind_temp = round(33+(0.478+0.237*math.sqrt(wind_speed)-0.0124*wind_speed)*(temp-33), 1)
    if wind_temp > temp:
        wind_temp = temp  # sometimes we can get wind chill little bit warmer
    #res = round(3.12+0.6215*temp-11.37*wind_speed**0.16+0.3965*temp*wind_speed**0.16)
    #res2 = round(33+(0.478+0.237*math.sqrt(wind_speed)-0.0124*wind_speed)*(temp-33))
    #print(temp, wind_speed, res, res2)
    return wind_temp


def fill_cond(string):
    lst = []
    for count in range(len(api['list'])):
        if string in texts[count]:
            lst.append(wind_chill[count])
        else:
            lst.append(min(wind_chill))
    return lst


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

temps = [ round(t['main']['temp']-273, 1) for t in api['list'] ]
wind_chill = [ get_wind_chill(temps[count], api['list'][count]['wind']['speed']*3.6) for count in range(len(api['list'])) ]

maxlevel = [ max(temps) for z in range(len(api['list'])) ]
zerolevel = [ min(wind_chill) for z in range(len(api['list'])) ]
underzerolevel = [ min(wind_chill)-3 for z in range(len(api['list'])) ]
zerolevel_point = min(zerolevel)
underzerolevel_point = min(underzerolevel)

texts = [ tx['weather'][0]['description'] for tx in api['list'] ]

dates = []
for date in [ d['dt'] for d in api['list'] ]:
    dates.append(convert_to_MSK_tz(date))

images_src = [icon['weather'][0]['description'] for icon in api['list']]

rains = fill_cond('rain')
snows = fill_cond('snow')
clear_sky = fill_cond('clear sky')
clouds = fill_cond('clouds')

#for count in range(len(api['list'])):
#    if 'rain' in texts[count]:
#        rains.append(temps[count])
#    else:
#        rains.append(min(temps))


# PLOT

fig, graph = plt.subplots()
graph.plot(dates, underzerolevel, 'w', dates, zerolevel, 'g', dates, temps, 'g', dates, snows, '#CCFFFF', dates, clouds, '#CCFFFF', dates, clear_sky, '#CCFFFF', dates, wind_chill, 'g', dates, maxlevel, 'w')
graph.grid(True)
graph.set_xlabel('Дни')
graph.set_ylabel('Цельсии')

for tick in graph.get_xticklabels():  # rotate X labels
    tick.set_rotation(285)

for count in range(len(api['list'])):
    graph.text(dates[count], 
               underzerolevel_point, 
               texts[count], 
               {
                'ha': 'center', 
                'va': 'bottom', 
                'color': '#404040'
               },
                bbox={
                'boxstyle': 'round',
                'facecolor': 'wheat',
                'alpha': 0.5 
               },
                rotation=270)

# Draw vertical lines at the end of day
for date in dates:
    if date.split()[0] == '00':
        graph.axvline(x=date)


graph.fill_between(dates, temps, wind_chill, where=wind_chill<temps, facecolor='#FFFFFF')
graph.fill_between(dates, wind_chill, zerolevel, where=zerolevel<wind_chill, facecolor='#CCFFFF')

graph.fill_between(dates, zerolevel, rains, where=rains>zerolevel, facecolor='#80BFFF')
graph.fill_between(dates, zerolevel, snows, where=snows>zerolevel, facecolor='#FFFFFF')
graph.fill_between(dates, zerolevel, clouds, where=clouds>zerolevel, facecolor='#A6A6A6')
#graph.fill_between(dates, zerolevel, clouds, where=clouds>zerolevel, facecolor='#C2D6D6')
graph.fill_between(dates, zerolevel, clear_sky, where=clear_sky>zerolevel, facecolor='#FFFF80')

fig.set_figwidth(12)
fig.tight_layout()
#plt.show()
plt.savefig('chart_plt.png')
