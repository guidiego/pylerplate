from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from utils.openapi import register_rules
from sqlalchemy import create_engine

from app import app
from database import db

from modules.user.api import UserResource

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

@manager.command
def run():
    register_rules(app, [
        UserResource
    ])

    app.run(
        debug=app.config['DEBUG'],
        port=app.config['PORT'],
        host=app.config['HOST'],
    ) 

@manager.command
def create_database():
    postgres_url = app.config['SQLALCHEMY_DATABASE_URI']
    db_name = app.config['DB_NAME']
    
    url_without_db = postgres_url.split('/{}'.format(db_name))[0]

    print(url_without_db)
    engine = create_engine(url_without_db)
    conn = engine.connect()
    conn.execute('create database {}'.format(db_name))
    conn.close()

if __name__ == '__main__':
    manager.run()

