import datetime
from termcolor import colored


def now():
    return colored("[" + datetime.datetime.now().strftime("%H:%M:%S") + "]", 'white')
