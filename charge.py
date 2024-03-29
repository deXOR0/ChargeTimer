#!/usr/bin/python3
# python -m pip install plyer
from plyer import notification
from datetime import datetime
from better_terminal import *
from progress.bar import ChargingBar
from datetime import timedelta
import time
import os
import sys
import argparse

parser = argparse.ArgumentParser(
    description='Program to time your wireless headset charging')

parser.add_argument('-s', '--shutdown', dest='shutdown', action='store_true')

args = parser.parse_args()

class ChargeBar(ChargingBar):
    suffix = 'Battery %(percent).1f%% - Remaining %(time_left)s'
    elapsed = 0

    @property
    def time_left(self):
        return timedelta(seconds=self.elapsed)

if args.shutdown:
    print('Shutdown Mode')
else:
    print('Timer Mode')

DEFAULT_TIME = 13500
AUTOSAVE_INTERVAL = 60

with open('time.txt', 'r') as file:
    charge_time = int(file.readline().strip())

time_left = DEFAULT_TIME - charge_time

bar = ChargeBar('Charging', max=DEFAULT_TIME)

for i in range(time_left):
    bar.next()

for i in range(time_left, DEFAULT_TIME):
    time.sleep(1)
    bar.elapsed = DEFAULT_TIME - i
    bar.next()
    if i % AUTOSAVE_INTERVAL == 0:
        with open('time.txt', 'w') as file:
            file.write(str(DEFAULT_TIME - i))   

bar.finish()

print("")

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
