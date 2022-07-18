import tkinter
from tkinter import *
import time
from datetime import datetime
import requests
import json
import config
from PIL import Image, ImageTk

class Mirror(Tk):

    def __init__(self):
        super().__init__()
        self.title('MirrorX')
        self.attributes("-fullscreen", True)
        self.state = True
        self.bind("<F12>", self.toggle_fullscreen)
        self.bind("<Escape>", self.close)

        self.cache = json.loads('[]')

        self.clock_size = 70
        self.title_size = 50
        self.h1_size = 35
        self.h2_size = 25
        self.p_size = 15

        self.api_key = config.api_key
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
        # current = time.strftime("%H : %M : %S")
        current = time.strftime("%H : %M")
        clock.config(text=current)
        self.after(1000, self.run_clock)

    def run_weather(self):
        full_request = self.request_format + 'lat=' + self.lat + '&lon=' + self.long + '&exclude=minutely,' \
                                                                                       'hourly&units=imperial&appid=' \
                       + self.api_key
        response = requests.get(full_request)
        weather_json = response.json()

        icon = weather_json["current"]["weather"][0]["icon"]
        small_icon = Image.open('./res/' + icon + '.png')
        weather_icon = ImageTk.PhotoImage(small_icon.resize((300, 300)))
        display_icon = Label(self, image=weather_icon, borderwidth=0, highlightthickness=0, pady=5, padx=5)
        display_icon.image = weather_icon
        display_icon.grid(row=1, column=0, sticky=E)

        temp = Label(self, font=("courier", self.title_size, "bold"), bg="black", fg="white")
        temp.config(text=str(int(weather_json["current"]["temp"])) + u'\N{DEGREE SIGN}')
        temp.grid(row=1, column=3, sticky=E)

        conditions = Label(self, font=("courier", self.h2_size, "bold"), bg="black", fg="white")
        conds = weather_json["current"]["weather"][0]["description"].replace(" ", "\n")
        conditions.config(text=conds)
        conditions.grid(row=1, column=1, columnspan=2)

        city = Label(self, font=("courier", self.h1_size, "bold"), bg="black", fg="white")
        city.config(text=self.city)
        city.grid(row=2, column=3, sticky=E)

        range_str = str(int(weather_json["daily"][0]["temp"]["min"])) + u'\N{DEGREE SIGN} - ' + str(
            int(weather_json["daily"][0]["temp"]["max"])) + u'\N{DEGREE SIGN}'
        temp_range = Label(self, font=("courier", self.h2_size, "bold"), bg="black", fg="white")
        temp_range.config(text=range_str)
        temp_range.grid(row=2, column=1, columnspan=2)

        state = Label(self, font=("courier", self.h2_size, "bold"), bg="black", fg="white")
        state.config(text=self.state)
        state.grid(row=3, column=3, sticky=E)

        # self.rowconfigure(4, minsize=20)

        daily_string = "["
        for i in range(1, 4):
            daily_string += str(weather_json["daily"][i]) + ","
        daily_string += str(weather_json["daily"][4]) + "]"
        daily_string = daily_string.replace("\'", "\"")
        if json.dumps(self.cache) == '[]' or json.loads(daily_string) != self.cache:
            self.cache = json.loads(daily_string)
            self.update_forecast()

        # TODO printing is unequal in the window, when 7" monitor attached resize to equal them out
        for i in range(0, 4):
            self.columnconfigure(i, weight=1, uniform="foo")

        for y in range(0,2):
            self.rowconfigure(y, weight=1, uniform="foo")

        # DO NOT CALL MORE FREQUENTLY THAN 1440ms, OR WILL EXCEED 1000 FREE API CALLS PER DAY
        self.after(600000, self.run_weather)

    def update_forecast(self):
        # Note: unfortunately, tkinter does not allow PhotoImage population using loops. The garbage collector
        # snatches the images and leaves blank squares.
        forecast_icon_1 = tkinter.PhotoImage(
            file='./res/' + str(self.cache[0]["weather"][0]["icon"]) + '.png')
        forecast_label_1 = Label(self, image=forecast_icon_1, borderwidth=0, highlightthickness=0, padx=5, pady=5)
        forecast_label_1.photo = forecast_icon_1
        forecast_label_1.grid(row=5, column=0)
        forecast_icon_2 = tkinter.PhotoImage(
            file='./res/' + str(self.cache[1]["weather"][0]["icon"]) + '.png')
        forecast_label_2 = Label(self, image=forecast_icon_2, borderwidth=0, highlightthickness=0, padx=5, pady=5)
        forecast_label_2.photo = forecast_icon_2
        forecast_label_2.grid(row=5, column=1)
        forecast_icon_3 = tkinter.PhotoImage(
            file='./res/' + str(self.cache[2]["weather"][0]["icon"]) + '.png')
        forecast_label_3 = Label(self, image=forecast_icon_3, borderwidth=0, highlightthickness=0, padx=5, pady=5)
        forecast_label_3.photo = forecast_icon_3
        forecast_label_3.grid(row=5, column=2)
        forecast_icon_4 = tkinter.PhotoImage(
            file='./res/' + str(self.cache[3]["weather"][0]["icon"]) + '.png')
        forecast_label_4 = Label(self, image=forecast_icon_4, borderwidth=0, highlightthickness=0, padx=5, pady=5)
        forecast_label_4.photo = forecast_icon_4
        forecast_label_4.grid(row=5, column=3)

        week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        today = datetime.today().weekday() + 1

        for i in range(0, 4):
            if today == 7:
                today = 0
            Label(self, font=("courier", self.p_size, "italic"), text=week[today], bg="black", fg="white").grid(row=6,
                                                                                                                column=i)
            min_temp = int(self.cache[i]["temp"]["min"])
            max_temp = int(self.cache[i]["temp"]["max"])
            cond = self.cache[i]["weather"][0]["main"]
            precip = int(self.cache[i]["pop"] * 100)
            Label(self, font=("courier", self.p_size, "italic"),
                  text=str(min_temp) + u'\N{DEGREE SIGN} - ' + str(max_temp) + u'\N{DEGREE SIGN}', bg="black",
                  fg="white").grid(
                row=7, column=i)
            Label(self, font=("courier", self.p_size, "italic"), text=cond, bg="black", fg="white").grid(row=8,
                                                                                                         column=i)
            Label(self, font=("courier", self.p_size, "italic"), text=str(precip) + '% precip', bg="black",
                  fg="white").grid(row=9, column=i)
            today += 1

    def toggle_fullscreen(self, event=None):
        self.state = not self.state
        self.attributes("-fullscreen", self.state)

    def close(self, event=None):
        self.destroy()


if __name__ == '__main__':
    app = Mirror()
    app.mainloop()
