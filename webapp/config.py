import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change-in-production'
    DEBUG = True
    HOST = '0.0.0.0'
    PORT = 5002 