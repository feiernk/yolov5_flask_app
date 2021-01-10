import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'yolov5_secret_keys'
    DEBUG = True
    YOLOV5_DIR = r'D:\github\yolov5'


