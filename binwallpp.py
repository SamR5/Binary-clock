#!/usr/bin/python3
# -*- coding: utf-8 -*-

# add prayer time of the day on the wallpaper


from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import subprocess
import time as t
import os


def time_now():
    """Return the time as (hour, min, sec)"""
    now = datetime.now()
    return str(now.hour).rjust(2, '0') + '-' +\
           str(now.minute).rjust(2, '0') + '-' +\
           str(now.second).rjust(2, '0')

stepx, stepy = 40//2, 40//2
size = 15//2
dx, dy = 1100//2, 540//2

def wallpaper():
    """"""
    img = Image.new("RGB", (1366//2, 768//2), "orange")
    draw = ImageDraw.Draw(img)
    col, row = 1, 1
    for i in time_now():
        for j in i:
            for k in bin(int(j))[2:].zfill(4):
                row += 1
                if k != '1':
                    continue
                draw.rectangle((col*stepx-size+dx, row*stepy-size+dy,
                                col*stepx+size+dx, row*stepy+size+dy),
                                fill="black")
                
            col += 1
            row = 1
    img.save("wallpp.png", quality=10)

def generate_all_walpp():
    path = '/home/sami/bin/binclock/wallpapers/'
    for hour in range(24):
        hour = str(hour).zfill(2)
        for minute in range(60):
            minute = str(minute).zfill(2)
            for second in range(60):
                second = str(second).zfill(2)

                TIME = (hour, minute, second)
                img = Image.new("RGB", (1366//2, 768//2), "orange")
                draw = ImageDraw.Draw(img)
                
                col, row = 1, 1
                for i in TIME:
                    for j in i:
                        for k in bin(int(j))[2:].zfill(4):
                            row += 1
                            if k != '1':
                                continue
                            draw.rectangle((col*stepx-size+dx,
                                            row*stepy-size+dy,
                                            col*stepx+size+dx,
                                            row*stepy+size+dy),
                                           fill="black")
                
                        col += 1
                        row = 1

                img.save(path + '_' + hour + '_' + '-'.join(TIME) + '.png',
                         quality=45)
        print(hour)

def update_wallpaper():
    TIME = time_now()
    path = os.path.join('file:///home/sami/bin/binclock/wallpapers', TIME[:2])
    subprocess.call(str("gsettings set org.gnome.desktop.background " +\
                        "picture-uri " +\
                        os.path.join(path, TIME + '.png')).split(' '))


if __name__ == '__main__':
    while 1:
        t.sleep(1)
        t0 = t.time()
        #update_wallpaper()
        generate_all_walpp()
        print(t.time() - t0)

