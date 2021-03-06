import json
import matplotlib.pyplot as plt
import matplotlib.image as img

import os
import datetime
import math

class Export_png:
    def __init__(self, forecast, title=''):
        self.forecast = forecast
        self.title = title

    def get_wind_chill(self, temp, wind_speed):
        wind_temp = round(33+(0.478+0.237*math.sqrt(wind_speed)-0.0124*wind_speed)*(temp-33), 1)
        if wind_temp > temp:
            wind_temp = temp  # sometimes we can get wind chill little bit warmer
        return wind_temp
    
    
    def fill_cond(self, string, texts, wind_chill):
        lst = []
        for count in range(len(self.forecast['list'])):
            if string in texts[count]:
                lst.append(wind_chill[count])
            else:
                lst.append(min(wind_chill))
        return lst


    def convert_to_MSK_tz(self, timestamp):
        msk = datetime.datetime.fromtimestamp(timestamp+60*60*3)
        days= {'Monday': 'Пн',
               'Tuesday': 'Вт',
               'Wednesday': 'Ср',
               'Thursday': 'Чт',
               'Friday': 'Пт',
               'Saturday': 'Сб',
               'Sunday': 'Вс'}
        return msk.strftime('%H')+' '+days[msk.strftime('%A')]
    
    def export(self, png_filename):
        temps = [ round(t['main']['temp']-273, 1) for t in self.forecast['list'] ]
        wind_chill = [ self.get_wind_chill(temps[count], self.forecast['list'][count]['wind']['speed']*3.6) for count in range(len(self.forecast['list'])) ]
        
        maxlevel = [ max(temps) for z in range(len(self.forecast['list'])) ]
        zerolevel = [ min(wind_chill) for z in range(len(self.forecast['list'])) ]
        underzerolevel = [ min(wind_chill)-3 for z in range(len(self.forecast['list'])) ]
        zerolevel_point = min(zerolevel)
        underzerolevel_point = min(underzerolevel)
        
        texts = [ tx['weather'][0]['description'] for tx in self.forecast['list'] ]
        
        dates = []
        for date in [ d['dt'] for d in self.forecast['list'] ]:
            dates.append(self.convert_to_MSK_tz(date))
        
        images_src = [icon['weather'][0]['description'] for icon in self.forecast['list']]
        
        rains = self.fill_cond('rain', texts, wind_chill)
        snows = self.fill_cond('snow', texts, wind_chill)
        clear_sky = self.fill_cond('clear sky', texts, wind_chill)
        clouds = self.fill_cond('clouds', texts, wind_chill)
        
        # PLOT
        
        fig, graph = plt.subplots()
        graph.plot(dates, underzerolevel, 'w', dates, zerolevel, 'g', dates, temps, 'g', dates, snows, '#CCFFFF', dates, clouds, '#CCFFFF', dates, clear_sky, '#CCFFFF', dates, wind_chill, 'g', dates, maxlevel, 'w')
        graph.grid(True)
        graph.set_xlabel('Дни')
        graph.set_ylabel('Цельсии')
        
        for tick in graph.get_xticklabels():  # rotate X labels
            tick.set_rotation(285)
        
        for count in range(len(self.forecast['list'])):
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
        fig.suptitle(self.title, fontsize=14, y=1)
        #plt.show()
        plt.savefig(os.path.join(os.getcwd(), png_filename))
        
        return os.path.join(os.getcwd(), png_filename+'.png')
