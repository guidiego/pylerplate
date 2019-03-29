import os

class Config():
    PORT=os.getenv('PORT', default=80)
    HOST=os.getenv('HOST', default='0.0.0.0')

    DB_NAME=os.getenv('POSTGRES_DB', default='t4u')
    DB_USER=os.getenv('POSTGRES_USER')
    DB_PASS=os.getenv('POSTGRES_PASSWORD')
    DB_HOST=os.getenv('POSTGRES_HOST')
    DB_PORT=os.getenv('POSTGRES_PORT')

    APP_URL = os.getenv('APP_URL')
    PASSWORD_SECRET=os.getenv('PASSWORD_SECRET')

    SQLALCHEMY_DATABASE_URI = "postgresql://{}:{}@{}:{}/{}".format(
        DB_USER,
        DB_PASS,
        DB_HOST,
        DB_PORT,
        DB_NAME,
    )