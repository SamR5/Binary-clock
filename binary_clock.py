#!/usr/bin/python3
# -*- coding: utf-8 -*-

# a binary clock


import tkinter as tk
from datetime import datetime, date
import time as t


def time_now():
    """Return the time as (hour, min, sec)"""
    now = datetime.now()
    return (str(now.hour).rjust(2, '0'),
            str(now.minute).rjust(2, '0'),
            str(now.second).rjust(2, '0'))

class BinClock():
    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(self.master, width=43, height=38,
                                bg="#661156", bd=0, highlightthickness=0)
        self.canvas.bind("<Button-1>", self.day_notification)
        self.canvas.pack()
        self.refresh()
        
        self.master.overrideredirect(True)
    
    def refresh(self):
        """"""
        self.canvas.delete(tk.ALL)
        row, col = 1, 1
        for i in time_now():
            for digit in i:
                for k in bin(int(digit))[2:].zfill(4):
                    row += 1
                    C, R = col*7-3, row*8-8
                    if k == '0':
                        self.canvas.create_rectangle(C, R, C, R,
                                                     fill="white", outline="")
                        continue
                    self.canvas.create_oval(C-2, R-2, C+2, R+2,
                                            fill="white", outline="white")
                    """ Big size
                    self.canvas.create_oval(col*40-15, row*40-15-40,
                                            col*40+15, row*40+15-40,
                                            fill="green")
                    """
                    
                col += 1
                row = 1
        self.master.after(1000, self.refresh)

    def day_notification(self, event):
        """"""
        self.notifMaster = tk.Tk()
        mydate = str(datetime.today().strftime('%d-%m-%y'))
        self.notif = tk.Label(self.notifMaster, text=mydate, bg="#808688",
                              fg="white")
        self.notif.pack()
        self.notifMaster.overrideredirect(True)
        self.notifMaster.geometry("+1+660")
        self.notifMaster.after(2500, self.notifMaster.destroy)


if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(width=False, height=False)
    
    clock = BinClock(root)
    #root.geometry("+1084+24") # for big
    root.geometry("+2+680")
    root.mainloop()

