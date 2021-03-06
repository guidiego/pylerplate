import os

class Config():
    PORT=os.getenv('PORT', default=80)
    HOST=os.getenv('HOST', default='0.0.0.0')

    FLASK_DEBUG=os.getenv('FLASK_DEBUG', default=False)
    FLASK_ENV=os.getenv('FLASK_ENV', default=False)

    DB_NAME=os.getenv('POSTGRES_DB', default='t4u')
    DB_USER=os.getenv('POSTGRES_USER')
    DB_PASS=os.getenv('POSTGRES_PASSWORD')
    DB_HOST=os.getenv('POSTGRES_HOST')
    DB_PORT=os.getenv('POSTGRES_PORT')

    APP_URL = os.getenv('APP_URL')
    REQUEST_AUTHOR_ID = os.getenv('REQUEST_AUTHOR_ID')
    REDIS_URL = os.getenv('REDIS_URL')

    if FLASK_ENV == 'test':
        SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    else:
        SQLALCHEMY_DATABASE_URI = "postgresql://{}:{}@{}:{}/{}".format(
            DB_USER,
            DB_PASS,
            DB_HOST,
            DB_PORT,
            DB_NAME,
        )