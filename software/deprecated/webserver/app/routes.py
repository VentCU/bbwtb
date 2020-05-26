import datetime

from app import app
from flask import render_template

_BOOT_TIME = datetime.datetime.now()
_BOOT_TIME_STR = _BOOT_TIME.strftime("%Y-%m-%d %H:%M")

@app.route('/')
@app.route('/index')
def index():
    now = datetime.datetime.now()
    time_str = now.strftime("%Y-%m-%d %H:%M")
    # duration calculation from: 
    # https://stackoverflow.com/questions/5259882/subtract-two-times-in-python
    duration = now - _BOOT_TIME
    # chop microseconds:
    # https://stackoverflow.com/questions/18470627/how-do-i-remove-the-microseconds-from-a-timedelta-object
    duration = duration - datetime.timedelta(microseconds=duration.microseconds)
    print(duration)
    template_data = {
        'title' : 'Hellow word',
        'boot_time' : _BOOT_TIME_STR,
        'time' : time_str,
        'duration' : duration
    }
    # for future reference: the ** unpacks the dict to its items
    return render_template('index.html', **template_data)
    # return 'Hellow word'

