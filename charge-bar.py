#!/usr/bin/python3
# python -m pip install plyer
from alive_progress import alive_bar
from time import sleep
from plyer import notification
from datetime import datetime
from alive_progress import alive_bar
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

file = open('time-bar.txt', 'r+')

charge_time = int(file.readline())

with alive_bar(DEFAULT_TIME, manual=True) as bar:
    for i in range(charge_time, DEFAULT_TIME+1):
        sleep(1)
        bar(1 / DEFAULT_TIME * i)
        if i % AUTOSAVE_INTERVAL == 0:
            file.truncate(0)
            file.write(str(i))
            file.close()
            file = open('time-bar.txt', 'r+')

    

file.write('0')

file.close()

log = open('log-bar.txt', 'a')

msg = 'Charging done on {}\n'.format(datetime.now())

print(msg)

log.write(msg)
log.close()

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
    else:
        os.system('shutdown /s /t 1')


charge_time = 120
current_time = 0
