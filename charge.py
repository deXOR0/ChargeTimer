#!/usr/bin/python3
# python -m pip install plyer
from plyer import notification
from datetime import datetime
from better_terminal import *
import time
import os
import sys
import argparse

parser = argparse.ArgumentParser(
    description='Program to time your wireless headset charging')

parser.add_argument('-s', '--shutdown', dest='shutdown', action='store_true')

args = parser.parse_args()

if args.shutdown:
    print('Shutdown Mode')
else:
    print('Timer Mode')

DEFAULT_TIME = 13500
AUTOSAVE_INTERVAL = 60

with open('time.txt', 'r') as file:
    charge_time = int(file.readline().strip())

def format_time(seconds):
    hrs = seconds // 3600
    minutes = (seconds - (hrs * 3600)) // 60
    seconds = seconds % 60
    return '{:02d} hour(s) {:02d} minute(s) {:02d} second(s)'.format(hrs, minutes, seconds)


def calculate_percentage(seconds):
    global DEFAULT_TIME
    return ((DEFAULT_TIME - time_left) / DEFAULT_TIME) * 100


time_left = charge_time

while time_left >= 0:
    time.sleep(1)
    percentage = calculate_percentage(time_left)
    time_string = f'{percentage:.1f}% - {format_time(time_left)}, until fully charged'
    cut_off_index = int(len(time_string) * (percentage / 100))
    done = time_string[:cut_off_index]
    not_done = time_string[cut_off_index:]
    print(colored(done, 'white', 'on_green'), end='')
    print(not_done)
    time_left -= 1
    if time_left % AUTOSAVE_INTERVAL == 0:
        with open('time.txt', 'w') as file:
            file.write(str(time_left))

with open('time.txt', 'w') as file:
    file.write(str(DEFAULT_TIME))

with open('log.txt', 'a') as log:
    msg = 'Charging done on {}\n'.format(datetime.now())
    print(msg)
    log.write(msg)

notification.notify(
    title='SteelSeries Arctis 1',
    message='Battery is full, please unplug the charger from the headset',
    # e.g. 'C:\\icon_32x32.ico'
    app_icon=os.path.join(os.getcwd(), 'ss.ico'),
    timeout=10,  # seconds
)

if args.shutdown:
    if sys.platform == 'linux' or sys.platform == 'linux2':
        os.system('shutdown now')
    elif sys.platform == 'darwin':
        os.system('pmset sleepnow')
    else:
        os.system('shutdown /s /t 1')
