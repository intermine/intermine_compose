from flask import logging

class CustomLogger(object):
    handle = None
    
    def init_app(self, app):
        self.handle = logging.create_logger(app)

custom_logger = CustomLogger()