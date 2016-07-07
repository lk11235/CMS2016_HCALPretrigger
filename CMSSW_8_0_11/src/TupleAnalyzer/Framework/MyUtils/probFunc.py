
from math import factorial,sqrt

def binoError(selectEvent,allEvent):
    return sqrt(selectEvent*(1-selectEvent/allEvent))/allEvent if allEvent != 0. else 0.
