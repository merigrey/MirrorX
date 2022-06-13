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
        self.grid_anchor(SE)

        self.run_clock()
        self.run_weather()

    def run_clock(self):
        clock = Label(self, font=("courier", self.clock_size, "bold"), bg="black", fg="white")
        clock.grid(row=0, column=2, columnspan=2, sticky=E, pady=5)
        current = time.strftime("%H : %M : %S")
        # current = time.strftime("%H : %M")
        clock.config(text=current)
        self.after(1000, self.run_clock)

    def run_weather(self):
        full_request = self.request_format + 'lat=' + self.lat + '&lon=' + self.long + '&exclude=minutely,hourly&units=imperial&appid=' + self.api_key
        response = requests.get(full_request)
        weather_json = response.json()

        icon = weather_json["current"]["weather"][0]["icon"]
        weather_icon = tkinter.PhotoImage(file='./res/' + icon + '.png')
        display_icon = Label(self, image=weather_icon, borderwidth=0, highlightthickness=0, pady=5, padx=5)
        display_icon.photo = weather_icon
        display_icon.grid(row=1, column=2)

        temp = Label(self, font=("courier", self.title_size, "bold"), bg="black", fg="white")
        temp.config(text=str(int(weather_json["current"]["temp"])) + u'\N{DEGREE SIGN}')
        temp.grid(row=1, column=3, sticky=E)

        conditions = Label(self, font=("courier", self.h2_size, "bold"), bg="black", fg="white")
        conditions.config(text=weather_json["current"]["weather"][0]["description"])
        conditions.grid(row=2, column=2)

        city = Label(self, font=("courier", self.h1_size, "bold"), bg="black", fg="white")
        city.config(text=self.city)
        city.grid(row=2, column=3, sticky=E)

        range_str = str(int(weather_json["daily"][0]["temp"]["min"])) + u'\N{DEGREE SIGN} - ' + str(
            int(weather_json["daily"][0]["temp"]["max"])) + u'\N{DEGREE SIGN}'
        temp_range = Label(self, font=("courier", self.p_size, "bold"), bg="black", fg="white")
        temp_range.config(text=range_str)
        temp_range.grid(row=3, column=2)

        state = Label(self, font=("courier", self.h2_size, "bold"), bg="black", fg="white")
        state.config(text=self.state)
        state.grid(row=3, column=3, sticky=E)

        self.rowconfigure(6, minsize=40)

        # Note: unfortunately, tkinter does not allow PhotoImage population using loops. The garbage collector
        # snatches the images and leaves blank squares.
        forecast_icon_1 = tkinter.PhotoImage(
            file='./res/' + str(weather_json["daily"][1]["weather"][0]["icon"]) + '.png')
        forecast_label_1 = Label(self, image=forecast_icon_1, borderwidth=0, highlightthickness=0, padx=5, pady=5)
        forecast_label_1.photo = forecast_icon_1
        forecast_label_1.grid(row=7, column=0)
        forecast_icon_2 = tkinter.PhotoImage(
            file='./res/' + str(weather_json["daily"][2]["weather"][0]["icon"]) + '.png')
        forecast_label_2 = Label(self, image=forecast_icon_2, borderwidth=0, highlightthickness=0, padx=5, pady=5)
        forecast_label_2.photo = forecast_icon_2
        forecast_label_2.grid(row=7, column=1)
        forecast_icon_3 = tkinter.PhotoImage(
            file='./res/' + str(weather_json["daily"][3]["weather"][0]["icon"]) + '.png')
        forecast_label_3 = Label(self, image=forecast_icon_3, borderwidth=0, highlightthickness=0, padx=5, pady=5)
        forecast_label_3.photo = forecast_icon_3
        forecast_label_3.grid(row=7, column=2)
        forecast_icon_4 = tkinter.PhotoImage(
            file='./res/' + str(weather_json["daily"][4]["weather"][0]["icon"]) + '.png')
        forecast_label_4 = Label(self, image=forecast_icon_4, borderwidth=0, highlightthickness=0, padx=5, pady=5)
        forecast_label_4.photo = forecast_icon_4
        forecast_label_4.grid(row=7, column=3)

        week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        today = datetime.today().weekday() + 1
        i = 0
        while i < 4:
            if today == 7:
                today = 0
            Label(self, font=("courier", self.p_size, "italic"), text=week[today], bg="black", fg="white").grid(row=8,
                                                                                                                column=i)
            min_temp = int(weather_json["daily"][i + 1]["temp"]["min"])
            max_temp = int(weather_json["daily"][i + 1]["temp"]["max"])
            cond = weather_json["daily"][i + 1]["weather"][0]["main"]
            precip = int(weather_json["daily"][i + 1]["pop"] * 100)

            Label(self, font=("courier", self.p_size, "italic"),
                  text=str(min_temp) + u'\N{DEGREE SIGN} - ' + str(max_temp) + u'\N{DEGREE SIGN}', bg="black", fg="white").grid(
                row=9, column=i)
            Label(self, font=("courier", self.p_size, "italic"), text=cond, bg="black", fg="white").grid(row=10,
                                                                                                         column=i)
            Label(self, font=("courier", self.p_size, "italic"), text=str(precip) + '% precip', bg="black",
                  fg="white").grid(row=11, column=i)

            i += 1
            today += 1

        y = 0
        while y < 4:
            self.columnconfigure(y, weight=1, uniform="foo")
            y += 1

        # DO NOT CALL MORE FREQUENTLY THAN 1440ms, OR WILL EXCEED 1000 FREE API CALLS PER DAY
        # self.after(30000, self.run_weather)


if __name__ == '__main__':
    app = Mirror()
    app.mainloop()
