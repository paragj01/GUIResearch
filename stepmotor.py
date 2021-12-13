import tkinter as tk
from tkinter import *
from tkinter import ttk

class StepMotor( Frame ):
    def __init__(self):
        tk.Frame.__init__(self)
        self.pack()
        self.master.title("SteperMotor")
        w = Canvas(self, width=200, height=200)
def main():
    StepMotor().mainloop()
if __name__ == '__main__':
    main()
