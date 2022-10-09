from asyncore import read
from django.shortcuts import render
import json
import urllib


def weather(request):
    if request.method == 'POST':
        city = request.POST['city']
        res = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q=' +
                                     city+'&appid=c68698a6f06480ea06fbe74a0df6d803').read()
        json_data = json.loads(res)
        data = {
            'city': city,
            'country': str(json_data['sys']['country']),
            'coordinate': str(json_data['coord']['lon']) + ' | ' + str(json_data['coord']['lat']),
            'temp': str(json_data['main']['temp']) + 'k',
            'pressure': str(json_data['main']['pressure']),
            'humidity': str(json_data['main']['humidity']),
        }
    else:
        data = {}
    return render(request, 'weather.html', data)
