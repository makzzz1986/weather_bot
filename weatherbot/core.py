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

    def send(self):
        response = self.request()
        print(self._store)
        #link = 'http://api.telegram.org/bot608334828:AAGA4osnMNtdgvx324sCu2KcaHfKMbf1tUs/sendMessage?chat_id=-1001216274719&text=222'
        #with Urlopen(link) as tg_send:
            #print(tg_send.read().decode('utf-8'))
            #tg_answer = json.loads(tg_send.read().decode('utf-8'))
            #print(tg_answer)
