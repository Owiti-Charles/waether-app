from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=Api Key'
    
    form = CityForm()
    error = ''
    message = ''
    message_class = ''
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['name']
            saved_cities = City.objects.filter(name = new_city).count()
            if saved_cities == 0:
                response = requests.get(url.format(new_city)).json()  
                if response['cod'] == 200:
                    form.save()
                else: 
                    error = 'Town does not exist'
            else:
                error = 'City Already Exists'
        if error:
            message = error
            message_class = 'is-danger'
        else:
            message = 'City Added Perfectly '
            message_class = 'is-success'
    cities = City.objects.all() 
    cities = cities[::-1]
    print(cities)
    data = []
    for city in cities: 
        respo = requests.get(url.format(city)).json()  
        town_weather = {
            'city': city.name,
            'temperature': round((respo['main']['temp']-32)*0.5556) ,
            'description': respo['weather'][0]['description'],
            'icon': respo['weather'][0]['icon'] ,
        }
        
        data.append(town_weather)

    params = {
        'data':data,
        'form':form,
        'message':message,
        'message_class':message_class,
    }
    print(data)
    return render(request, 'weather/weather.html', params)
