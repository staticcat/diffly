import os

basedir = os.path.realpath(os.path.dirname(__file__))
database_dir = os.path.join(basedir, "db", "diffly.db")

DATABASE_URI = 'sqlite:///' + database_dir
SQLALCHEMY_DATABASE_URI = DATABASE_URI
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
SQLALCHEMY_TRACK_MODIFICATIONS = False
