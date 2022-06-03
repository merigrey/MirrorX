import tkinter
from tkinter import *
import time
from datetime import datetime
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
        self.request_format = 'https://api.openweathermap.org/data/3.0/onecall?'

        self.configure(background='black')

        self.run_clock()
        self.run_weather()

    def run_clock(self):
        clock = Label(self, font=("courier", self.clock_size, "bold"), bg="black", fg="white")
        clock.grid(row=0, column=3, columnspan=2, sticky=E, pady=5)
        current = time.strftime("%H : %M : %S")
        clock.config(text=current)
        self.after(1000, self.run_clock)

    def run_weather(self):
        full_request = self.request_format + 'lat=' + self.lat + '&lon=' + self.long + '&exclude=minutely,hourly&units=imperial&appid=' + self.api_key
        response = requests.get(full_request)
        weather_json = response.json()

        print(json.dumps(weather_json))

        icon = weather_json["current"]["weather"][0]["icon"]
        weather_icon = tkinter.PhotoImage(file='./res/' + icon + '.png')
        display_icon = Label(self, image=weather_icon, borderwidth=0, highlightthickness=0, pady=5, padx=5)
        display_icon.photo = weather_icon
        display_icon.grid(row=1, column=3)

        temp = Label(self, font=("courier", self.title_size, "bold"), bg="black", fg="white")
        temp.config(text=str(weather_json["current"]["temp"]) + u'\N{DEGREE SIGN}')
        temp.grid(row=1, column=4, sticky=E)

        conditions = Label(self, font=("courier", self.h2_size, "bold"), bg="black", fg="white")
        conditions.config(text=weather_json["current"]["weather"][0]["description"])
        conditions.grid(row=2, column=3)

        city = Label(self, font=("courier", self.h1_size, "bold"), bg="black", fg="white")
        city.config(text=self.city)
        city.grid(row=2, column=4, sticky=E)

        range_str = str(weather_json["daily"][0]["temp"]["min"]) + u'\N{DEGREE SIGN} - ' + str(weather_json["daily"][0]["temp"]["max"]) + u'\N{DEGREE SIGN}'
        temp_range = Label(self, font=("courier", self.p_size, "bold"), bg="black", fg="white")
        temp_range.config(text=range_str)
        temp_range.grid(row=3, column=3)

        state = Label(self, font=("courier", self.h2_size, "bold"), bg="black", fg="white")
        state.config(text=self.state)
        state.grid(row=3, column=4, sticky=E)

        week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        today = datetime.today().weekday()
        i = 0
        while i < 4:
            d1 = Label(self, font=("courier", self.h2_size, "bold"), bg="black", fg="white")
            d1.config(text=week[today+1])
            d1.grid(row=6, column=1)
        # d2 = Label(self, font=("courier", self.h2_size, "bold"), bg="black", fg="white")
        # d2.config(text=week[today+2])
        # d2.grid(row=6, column=2)
        # d3 = Label(self, font=("courier", self.h2_size, "bold"), bg="black", fg="white")
        # d3.config(text=week[today+3])
        # d3.grid(row=6, column=3)
        # d4 = Label(self, font=("courier", self.h2_size, "bold"), bg="black", fg="white")
        # d4.config(text=week[today+4])
        # d4.grid(row=6, column=4)
        # d4 = Label(self, font=("courier", self.h2_size, "bold"), bg="black", fg="white")
        # d4.config(text=week[today+5])
        # d4.grid(row=6, column=5)


        # DO NOT CALL MORE FREQUENTLY THAN 1440ms, OR WILL EXCEED 1000 FREE API CALLS PER DAY
        #self.after(30000, self.run_weather)




if __name__ == '__main__':
    app = Mirror()
    app.mainloop()
