from tkinter import *
import time

class Mirror(Tk):


    def __init__(self):
        super().__init__()
        self.title('MirrorX')
        self.geometry("600x450")
        #self.columnconfigure(0, weight=2)

        # self.resizable(0,0) makes not resizable
        # self.set_up_widgets()
        self.run_widgets()

    def run_widgets(self):
        clock = Label(self, font=("courier", 60, "bold"), bg="white")
        clock.grid(row=0, column=0, pady=5, padx=5)
        current = time.strftime("%H : %M : %S")
        clock.config(text=current)
        self.after(1, self.run_widgets)

if __name__ == '__main__':
    app = Mirror()
    app.mainloop()
