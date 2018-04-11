
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from tkinter import *
from ezprint import p
import pandas as pd
import datetime
import requests
import random
import json
import time


latlon_url = 'https://api.opencagedata.com/geocode/v1/json?q='
latlon_api_key = '&key=784aa1346e1d46c9ad32544372f7316e'
weather_url = 'https://api.darksky.net/forecast/'
weather_api_key = '08d603a88b0d98d0c6b24dfb41f716bc'


def watch():
	city = entry.get()
	latlon = get_latlon(city)
	if latlon == 'no_net':
		entry.delete(0, END)
		entry.insert(0, 'No connection')
	elif latlon == 'no_city':
		entry.delete(0, END)
		entry.insert(0, 'City not found')
	else:
		root.destroy()
		get_weather(latlon[0], latlon[1], city)



def get_weather(latitude, longitude, city):
	r = requests.get(weather_url + weather_api_key + '/' + str(latitude) + ',' + str(longitude)).text
	jsn = json.loads(r)
	temps = []
	times = []
	jsn = jsn['hourly']['data']
	for i in jsn:
		temps.append(fahrenheit_to_celsius(i['temperature']))
		times.append(datetime.datetime.fromtimestamp(int(i['time'])))

	pl = plt.plot(times, temps, label = 'Temperature change', c = 'green', lw = 3.5, marker = 'o', mec = 'red')
	plt.gcf().autofmt_xdate()
	myFmt = mdates.DateFormatter('%H:%M')
	plt.gca().xaxis.set_major_formatter(myFmt)
	plt.legend(handles=[pl[0]])
	plt.xlabel('Hours')
	plt.ylabel('Temperature')
	plt.title(city.capitalize())
	plt.show()


def get_latlon(city):
	try:
		r = requests.get(latlon_url + city + latlon_api_key).text
	except:
		return 'no_net'

	lljsn = json.loads(r)

	try:
		longitude = lljsn['results'][0]['geometry']['lng']
		latitude  = lljsn['results'][0]['geometry']['lat']
		return [latitude, longitude]
	except:
		return 'no_city'


def fahrenheit_to_celsius(temp):
	t = (temp - 32) / 1.8
	return round(t, 2)


def kelvin_to_celsius(temp):
	t = temp - 273.15
	return t


root = Tk()

root.title('Weather') 

label = Label(root, text = 'City name:')
entry = Entry(root, width = 20)
button = Button(root, text = 'Watch weather', command = watch)

label.config(font = ('Arial', 20, 'bold'))
entry.config(font = ('Arial', 20, 'bold'))
button.config(font = ('Arial', 20, 'bold'))

label.grid(column = 0, row = 0)
entry.grid(column = 1, row = 0)
button.grid(column = 1, columnspan = 2)


root.mainloop()