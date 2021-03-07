import os
basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or "postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}".format(
        user = 'postgres',
        password = 'postgres',
        host = 'localhost',
        port = '5432',
        dbname = 'postgres'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or "you-will-never-guess"

    # Flask needs this if we use the 'render_template_string()' method
    SERVER_NAME = '127.0.0.1:5000'
