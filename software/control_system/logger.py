''' 
@file software/control_system/logger.py
test program for python native logging

author: William Xie
'''
from datetime import datetime
import logging

class LoggerInit:

    def __init__(self, name):
        self.filename = datetime.now().strftime("%Y%m%d%H%M%S")
        self.format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        self.header_date = datetime.now().strftime("%Y/%m/%d, %H:%M:%S")
        self.header = f"VentCU Log for {self.header_date}\n"

        logging.basicConfig(level=logging.DEBUG, format=self.format,
                            handlers=[
                                logging.StreamHandler(),
                                logging.FileHandler(f'logs/{self.filename}.log')
                            ])
        logger = logging.getLogger('ventilator.py')
        logger.info(f'{self.header}')

if __name__ == "__main__":
    logger = LoggerInit("test")