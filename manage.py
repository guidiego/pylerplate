from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from utils.openapi import register_rules

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
        port=app.config['PORT'],
        host=app.config['HOST'],
    ) 

if __name__ == '__main__':
    manager.run()

