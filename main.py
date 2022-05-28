from tkinter import *
import time
import requests
import json

class Mirror(Tk):

    def __init__(self):
        super().__init__()
        self.title('MirrorX')
        self.geometry("600x450")
        self.api_key = 'd792f712718a58df006933a2204b10be'
        self.lat = '47.7601'
        self.long = '-122.2054'
        self.request_format = 'https://api.openweathermap.org/data/2.5/weather?'
        #self.columnconfigure(0, weight=2)

        # self.resizable(0,0) makes not resizable
        self.run_clock()

    def run_clock(self):
        clock = Label(self, font=("courier", 60, "bold"), bg="white")
        clock.grid(row=0, column=0, pady=5, padx=5)
        current = time.strftime("%H : %M : %S")
        clock.config(text=current)
        self.after(1000, self.run_clock())

    def run_weather(self):
        full_request = self.request_format + 'lat=' + self.lat + '&lon=' + self.long + '&appid=' + self.api_key
        response = requests.get(full_request)
        weather_json = response.json()
        visibility = weather_json["visibility"]

        weather_widget = Label(self, font=("courier", 60, "bold"), bg="white")
        weather_widget.grid(row=1, column=0, pady=5, padx=5)
        weather_widget.config(text=visibility)


if __name__ == '__main__':
    app = Mirror()
    app.mainloop()
