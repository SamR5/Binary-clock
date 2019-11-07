#!/usr/bin/python3
# -*- coding: utf-8 -*-

# a binary clock


import tkinter as tk
from datetime import datetime, date
import time as t


class Circle():
    def __init__(self, minRad, maxRad):
        self.minRad = minRad
        self.maxRad = maxRad
        self.radius = 0
        self.isShrinking = False

    def update(self):
        if self.isShrinking:
            if self.radius > self.minRad:
                self.radius -= GROWING_FACTOR
        else:
            if self.radius < self.maxRad:
                self.radius += GROWING_FACTOR


def time_now():
    """Return the time as (hour, min, sec)"""
    bina = lambda value: bin(int(value))[2:].zfill(4)
    now = datetime.now()
    H = str(now.hour).rjust(2, '0')
    M = str(now.minute).rjust(2, '0')
    S = str(now.second).rjust(2, '0')
    ##
    H = [bina(H[0]), bina(H[1])]
    M = [bina(M[0]), bina(M[1])]
    S = [bina(S[0]), bina(S[1])]
    return H + M + S


class BinClock():
    def __init__(self, master):
        self.master = master
        self.lastPosition = None # last cursor position
        self.canvas = tk.Canvas(self.master, width=WIDTH+2*HRZ_MARGIN,
                                height=HEIGHT+2*VRT_MARGIN,
                                bg="#661156", bd=0, highlightthickness=0)
        self.canvas.bind("<Button-1>", self.date_notification)
        self.canvas.bind("<Button-3>", self.update_last_position)
        self.canvas.bind("<Button3-Motion>", self.right_click_motion)
        self.canvas.pack()
        self.circles = dict()
        self.init_circles()
        self.refresh()
        self.draw()

        self.master.overrideredirect(True)

    def init_circles(self):
        for r in range(4):
            for c in range(6):
                self.circles[(r, c)] = Circle(1, min(R, C)/2 - 2)

    def update_last_position(self, event=None):
        self.lastPosition = (event.x, event.y)

    def right_click_motion(self, event=None):
        currentPos = list(map(int, self.master.geometry().split('+')[1:]))
        currentPos[0] += event.x - self.lastPosition[0]
        currentPos[1] += event.y - self.lastPosition[1]
        self.master.geometry('+'+str(currentPos[0])+'+'+str(currentPos[1]))
        #self.lastPosition = currentPos

    def refresh(self):
        """"""
        for ind, i in enumerate(time_now()):
            for ind2, j in enumerate(i):
                if j == '1':
                    self.circles[(ind2, ind)].isShrinking = False
                else:
                    self.circles[(ind2, ind)].isShrinking = True
                self.circles[(ind2, ind)].update()
        self.master.after(100, self.refresh)

    def draw(self):
        """"""
        self.canvas.delete(tk.ALL)
        for (row, col), c in self.circles.items():
            centerR, centerC = R*(row+0.5)+VRT_MARGIN, C*(col+0.5)+HRZ_MARGIN
            if c.radius < 2:
                self.canvas.create_rectangle(centerC, centerR,
                                             centerC, centerR,
                                    fill="white", outline="white")
            else:
                self.canvas.create_oval(centerC-c.radius, centerR-c.radius,
                                        centerC+c.radius, centerR+c.radius,
                                        fill="white", outline="white")
        self.master.after(50, self.draw)

    def get_position(self):
        return [self.master.winfo_rootx(), self.master.winfo_rooty(),
                self.master.winfo_width(), self.master.winfo_height()]

    def find_date_position(self):
        datePos = [0, 0]
        currentPos = self.get_position()
        if currentPos[1] < 21:
            datePos[1] = currentPos[1] + currentPos[3]
        else:
            datePos[1] = currentPos[1] - 21
        if currentPos[0] < 0:
            datePos[0] = 0
        else:
            datePos[0] = currentPos[0]
        return datePos

    def date_notification(self, event):
        """"""
        self.notifMaster = tk.Tk()
        mydate = str(datetime.today().strftime('%d-%m-%y'))
        self.notif = tk.Label(self.notifMaster, text=mydate, bg="#808688",
                              fg="white")
        self.notif.pack()
        self.notifMaster.overrideredirect(True)
        datePos = self.find_date_position()
        self.notifMaster.geometry('+' + '+'.join(map(str, datePos)))
        self.notifMaster.after(2000, self.notifMaster.destroy)


WIDTH, HEIGHT = 240, 160 #43, 38
R, C = HEIGHT/4, WIDTH/6
VRT_MARGIN = 5
HRZ_MARGIN = 5
GROWING_FACTOR = 3

if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(width=False, height=False)
    clock = BinClock(root)
    root.geometry("+20+580")
    root.mainloop()

