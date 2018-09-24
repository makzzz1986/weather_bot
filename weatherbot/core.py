from urllib.request import urlopen as Urlopen
import json

class Bot:
    def __init__(self, **kwargs):
        self._store = kwargs

    def request(self):
        for place in self._store['places'].keys():
            try:
                link = 'http://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&APPID={}'.format(self._store['places'][place].split()[0], self._store['places'][place].split()[1], self._store['OWMTOKEN'])
                with Urlopen(link) as owm_request:
                    owm_answer = json.loads(owm_request.read().decode('utf-8'))
                    print(owm_answer)
                    self._store['forecasts'][place] = owm_answer
            except Exception as e:
                print(e)

    def test(self, response):
        self._store['forecasts']['Parnas'] = response

#{'dt': 1538136000, 'main': {'temp': 280.661, 'temp_min': 280.661, 'temp_max': 280.661, 'pressure': 1004.16, 'sea_level': 1006.94, 'grnd_level': 1004.16, 'humidity': 100, 'temp_kf': 0}, 'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10d'}], 'clouds': {'all': 92}, 'wind': {'speed': 4.05, 'deg': 312.503}, 'rain': {'3h': 0.61}, 'sys': {'pod': 'd'}, 'dt_txt': '2018-09-28 12:00:00'}

    def temp_C(self, temp_K):
        return round(temp_K - 273.15)

    def form_text(self, forecast):
        string = ''
        string += forecast['cod'] + '\n'
        if forecast['cod'] == '200':
            for elem in forecast['list'][:24]:
                string += ' '.join(elem['dt_txt'], self.temp_C(elem['main']['temp']), elem['weather'][0]['description'], round(elem['wind']['speed'])) + '\n'
        else:
            print(forecast[forecast])
        return string

    def send(self):
        response = self.request()
        #print(self._store)
        
        messages = []

        for forecast in self._store['forecasts'].keys():
            messages.append(self.form_text(self._store['forecasts'][forecast]))

        for message in messages:
            link = 'http://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'.format(self._store['TGTOKEN'], self._store['TGCHATID'], message)
            with Urlopen(link) as tg_send:
                #print(tg_send.read().decode('utf-8'))
                tg_answer = json.loads(tg_send.read().decode('utf-8'))
                print(tg_answer)
