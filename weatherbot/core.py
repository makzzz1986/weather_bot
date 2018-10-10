from urllib.request import urlopen as Urlopen
import datetime
#import requests
import json
import telegram
from .png import Export_png as export


class Bot:
    def __init__(self, **kwargs):
        self._store = kwargs

    def request(self):
        for place in self._store['places'].keys():
            try:
                link = 'http://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&APPID={}'.format(self._store['places'][place].split()[0], self._store['places'][place].split()[1], self._store['OWMTOKEN'])
                with Urlopen(link) as owm_request:
                    owm_answer = json.loads(owm_request.read().decode('utf-8'))
                    #print(owm_answer)
                    self._store['forecasts'].append({'place_name': place, 'forecast': owm_answer})
            except Exception as e:
                print(e)

    def test(self, response):
        self._store['forecasts']['Parnas'] = response

# Typical one poin of forecast
#{'dt': 1538136000, 'main': {'temp': 280.661, 'temp_min': 280.661, 'temp_max': 280.661, 'pressure': 1004.16, 'sea_level': 1006.94, 'grnd_level': 1004.16, 'humidity': 100, 'temp_kf': 0}, 'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10d'}], 'clouds': {'all': 92}, 'wind': {'speed': 4.05, 'deg': 312.503}, 'rain': {'3h': 0.61}, 'sys': {'pod': 'd'}, 'dt_txt': '2018-09-28 12:00:00'}

    def convert_to_MSK_tz(self, timestamp):
        msk = datetime.datetime.fromtimestamp(timestamp+60*60*3)
        return msk.strftime('%H')
#        return msk.strftime('%Y-%m-%d, %H')

    def temp_C(self, temp_K):
        return str(round(temp_K - 273.15))

    def wind(self, ms):
        if round(ms) > 7:
            return '<i>w</i> '
        elif round(ms) > 16:
            return '<i>W</i> '
        elif round(ms) > 25:
            return '<b><i>W</i>!</b>'
        else:
            return ''

    def lent(self, string):     # get string's length without html tags
        tag = False
        counter = 0
        for ch in string:
            if ch == '<':
                tag = True
            elif ch == '>':
                tag = False
            else:
                if tag == False:
                    counter += 1
        return counter

    def form_line(self, elem):
        line = "at {}: <b>{}</b><i>C°</i>, <b>{}</b> {}\n".format(self.convert_to_MSK_tz(elem['dt']), self.temp_C(elem['main']['temp']), elem['weather'][0]['description'], self.wind(elem['wind']['speed']))
        return ' '*4 + line
        #return ' '*(46-self.lent(line)) + line

    def form_text(self, place):
        string = ''
        string += '<b>Weather for %s</b>\n' % place['place_name']
        if place['forecast']['cod'] == '200':
            day = ''
            for elem in place['forecast']['list'][:13]:
                if day != elem['dt_txt'].split()[0]:
                    day = elem['dt_txt'].split()[0]
                    string += day + ' '*24  + '\n'         # Form date
                string += self.form_line(elem)
        else:
            string += str(place['forecast'])
        return string

    def send(self):
        response = self.request()
        #print(self._store)
        
        bot = telegram.Bot(token=self._store['TGTOKEN'])

#        for place in self._store['forecasts']:
#            bot.send_message(chat_id=self._store['TGCHATID'], text=self.form_text(place), parse_mode=telegram.ParseMode.HTML)

        for place in self._store['forecasts']:
            forecast_png = export(place['forecast'], place['place_name'])
            bot.send_photo(chat_id=self._store['TGCHATID'], photo=open(forecast_png.export(place['place_name']), 'rb'))
