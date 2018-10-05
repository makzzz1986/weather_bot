import plotly.offline as offline
import plotly.graph_objs as go
import plotly.io as pio

import os
import datetime

class Export_png:
    def __init__(self, forecast):
        # change days to observe
        #forecast['list'] = forecast['list'][:13]
        #forecast['list'] = forecast['list'][:30]
        self.forecast = forecast

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
        temps = [ round(t['main']['temp']-273) for t in self.forecast['list'] ]
        
        dates = []
        for date in [ d['dt'] for d in self.forecast['list'] ]:
            dates.append(self.convert_to_MSK_tz(date))
        
        
        texts = [ tx['weather'][0]['description'] for tx in self.forecast['list'] ]
        
#        textposition = []
#        counter = 0
#        for t in temps[:-1]:
#            if temps[counter+1] > t:   # if next temp will be higher than current, text should be lower
#                textposition.append('bottom left')
#            else:
#                textposition.append('top left')
#            counter += 1 
        #print(textposition)
        
        # x 0.955 for 13 units
        # x 0.91 for 40 units
        # Generate list with dicts
        images_ico = [ {'sizex': 0.1, 
                        'sizey': 0.1, 
                        'x': 0.03 + count*0.91/len(self.forecast['list']),
                        'y': 1 + 0.06*(count%2),
                        'xref': 'paper', 
                        'yref': 'paper', 
                        'xanchor': 'left',
                        'yanchor': 'bottom',
                        'source': 'http://openweathermap.org/img/w/{}.png'.format(self.forecast['list'][count]['weather'][0]['icon'])} for count in range(len(self.forecast['list'])) ]
        #print(images_ico)
        
        # Try annotations
        annotations = [{'xref': 'paper',
                        'yref': 'paper',
                        'showarrow': False,
                        'arrowhead': 0,
                        'textangle': 90,
                        'x': 0.04 + count*0.945/len(self.forecast['list']),
                        'y': 0,
                        'text': texts[count]} for count in range(len(self.forecast['list']))]
        #print(annotations)
        
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
                                      title='Градусы Цельсия',
                                      ticks='outside',
                                      tickwidth=2, 
                                      showgrid=True,
                                      showline=True, 
                                      gridcolor='#bdbdbd',
                                      gridwidth=1,
                                      mirror='ticks'
                                      ))
        
        fig = go.Figure(data=data, layout=layout)
        
        png_path = '/tmp/%s.png' % png_filename
        pio.write_image(fig, png_path)
        return png_path
