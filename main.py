
#start
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


def watch(arg = None):
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
		get_weather(latlon[0], latlon[1], latlon[2])


def get_weather(latitude, longitude, city):
	r = requests.get(weather_url + weather_api_key + '/' + str(latitude) + ',' + str(longitude)).text
	jsn = json.loads(r)

	temps = []
	times = []
	winds = []
	windstimes = []

	if v.get() == 1:
		jsn = jsn['hourly']['data']

		for i in jsn:
			temps.append(fahrenheit_to_celsius(i['temperature']))
			times.append(datetime.datetime.fromtimestamp(int(i['time'])))
			winds.append(i['windSpeed'])

		pl1 = plt.plot(times, temps, label = 'Temperature change', c = 'green', lw = 3.5, marker = 'o', mec = 'red')
		pl2 = plt.plot(times, winds, label = 'Wind speed change', c = 'blue', lw = 0.5)
		plt.gcf().autofmt_xdate()
		myFmt = mdates.DateFormatter('%d.%m %H:%M')
		plt.gca().xaxis.set_major_formatter(myFmt)
		plt.legend(handles=[pl1[0], pl2[0]])
		plt.xlabel('Hours')
		plt.ylabel('Temperature/Wind speed')
		plt.title(city)
		plt.show()
	elif v.get() == 2:
		jsn = jsn['daily']['data']
		
		for i in jsn:
			winds.append(i['windSpeed'])
			times.append(datetime.datetime.fromtimestamp(int(i['time'])))
			t = fahrenheit_to_celsius( round((i['temperatureMin'] + i['temperatureMax']) / 2, 2) )
			temps.append(t)

		pl1 = plt.plot(times, temps, label = 'Average temperature change', c = 'green', lw = 3.5, marker = 'o', mec = 'red')
		pl2 = plt.plot(times, winds, label = 'Wind speed change', c = 'blue', lw = 0.5)
		plt.gcf().autofmt_xdate()
		myFmt = mdates.DateFormatter('%d.%m.%y')
		plt.gca().xaxis.set_major_formatter(myFmt)
		plt.legend(handles=[pl1[0], pl2[0]])
		plt.xlabel('Days')
		plt.ylabel('Average temperature/Wind speed')
		plt.title(city)
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
		c = lljsn['results'][0]['formatted']
		return [latitude, longitude, c]
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

root.resizable(0, 0)

root.config(bg = '#1FA7E1')
root.config()

v = IntVar()

radio1 = Radiobutton(root, text="48 Hours", variable=v, value=1, fg='white')
radio2 = Radiobutton(root, text="Week", variable=v, value=2, fg='white')

radio1.config(bg = '#1FA7E1')
radio2.config(bg = '#1FA7E1')

radio1.select()

main_menu = Menu(root)
root.config(menu=main_menu)
file_menu = Menu(main_menu)
main_menu.add_cascade(label="Settings", menu=file_menu)
file_menu.add_command(label="Exit", command=root.destroy)

label = Label(root, text = 'City name:', bg='#1FA7E1', fg='white')
entry = Entry(root, width = 20)
button = Button(root, text = 'Watch weather', command = watch)

root.bind('<Return>', watch)

label.config(font = ('Arial', 15, 'bold'))
entry.config(font = ('Arial', 15, 'bold'))
button.config(font = ('Arial', 15, 'bold'))

radio1.grid(column = 0, row = 1)
radio2.grid(column = 1, row = 1)

label.grid(column = 0, row = 0)
entry.grid(column = 1, row = 0)
button.grid(column = 1, columnspan = 2)

root.mainloop()