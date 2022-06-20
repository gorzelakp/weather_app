import re
import requests
from django.shortcuts import render, redirect
from .models import City
from .forms import CityForm

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=1a4831a0952a9b9ba5a748ef3aa8d85c'

    err_msg = ''
    message = ''
    message_class = '' # kolor wiadomości

    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()
            if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json()
                if r['cod'] == 200:
                    form.save()
                else:
                    err_msg = 'Takie miasto nie istnieje!'
            else:
                err_msg = 'Miasto już zostało dodane!'

    if err_msg:
        message = err_msg
        message_class = 'is-danger'
    else:
        message = 'Dodano miasto pomyślnie!'
        message_class = 'is-success'

    form = CityForm()

    cities = City.objects.all()
    weather_data = []

    for city in cities:
        r = requests.get(url.format(city)).json()

        city_weather = {
            'city': city.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon']
        }
        weather_data.append(city_weather)

    context = {'weather_data': weather_data, 
              'form': form,
              'message': message,
              'message_class': message_class}

    return render(request, 'weather/weather.html', context)

def delete_city(request, city_name):
    City.objects.get(name = city_name).delete()
    return redirect('home')