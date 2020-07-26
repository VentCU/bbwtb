''' 
@file software/control_system/logger.py
describes two classes, Logger and LoggerManager, of which
Logger is held by individual classes (alarms, ui_controller_interface,
and ventilator_controller) and LoggerManager handles each logger

author: William Xie
'''
from datetime import datetime

class Logger:

    def init(self, name):
        pass

class LoggerManager:

    def __init__(self):
        self.name = datetime.now().strftime("%Y%m%d%H%M%S")
        self.log = open(f"logs/{self.name}.log", 'w')
        self.header_date = datetime.now().strftime("%Y/%m/%d, %H:%M:%S")
        self.header = f"VentCU Log for {self.header_date}\n"
        
        self.log.write(self.header)

    def add_logger(self, Logger):
        pass

if __name__ == "__main__":
    logger_manager = LoggerManager()