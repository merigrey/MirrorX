import tkinter
from tkinter import *
import time
import requests
import json


class Mirror(Tk):

    def __init__(self):
        super().__init__()
        self.title('MirrorX')

        self.clock_size = 80
        self.title_size = 60
        self.h1_size = 40
        self.h2_size = 30
        self.p_size = 20

        self.api_key = 'd792f712718a58df006933a2204b10be'
        self.city = "Bothell"
        self.state = "WA"
        self.lat = '47.7601'
        self.long = '-122.2054'
        self.request_format = 'https://api.openweathermap.org/data/2.5/weather?'

        self.configure(background='black')

        self.run_clock()
        self.run_current_weather()

    def run_clock(self):
        clock = Label(self, font=("courier", self.clock_size, "bold"), bg="black", fg="white")
        clock.grid(row=0, column=3, columnspan=2, sticky=E, pady=5)
        current = time.strftime("%H : %M : %S")
        clock.config(text=current)
        self.after(1000, self.run_clock)

    def run_current_weather(self):
        full_request = self.request_format + 'lat=' + self.lat + '&lon=' + self.long + '&units=imperial&appid=' + self.api_key
        response = requests.get(full_request)
        weather_json = response.json()

        icon = weather_json["weather"][0]["icon"]
        weather_icon = tkinter.PhotoImage(file='./res/' + icon + '.png')
        display_icon = Label(self, image=weather_icon, borderwidth=0, highlightthickness=0, pady=5, padx=5)
        display_icon.photo=weather_icon
        display_icon.grid(row=1, column=3)

        temp = Label(self, font=("courier", self.title_size, "bold"), bg="black", fg="white")
        temp.config(text=str(weather_json["main"]["temp"]) + u'\N{DEGREE SIGN}')
        temp.grid(row=1, column=4, sticky=E)

        conditions = Label(self, font=("courier", self.h2_size, "bold"), bg="black", fg="white")
        conditions.config(text=weather_json["weather"][0]["main"])
        conditions.grid(row=2, column=3)

        city = Label(self, font=("courier", self.h1_size, "bold"), bg="black", fg="white")
        city.config(text=self.city)
        city.grid(row=2, column=4, sticky=E)

        range_str = str(weather_json["main"]["temp_min"]) + u'\N{DEGREE SIGN} - ' + str(weather_json["main"][
            "temp_max"]) + u'\N{DEGREE SIGN}'
        temp_range = Label(self, font=("courier", self.p_size, "bold"), bg="black", fg="white")
        temp_range.config(text=range_str)
        temp_range.grid(row=3, column=3)

        state = Label(self, font=("courier", self.h2_size, "bold"), bg="black", fg="white")
        state.config(text=self.state)
        state.grid(row=3, column=4, sticky=E)


if __name__ == '__main__':
    app = Mirror()
    app.mainloop()
