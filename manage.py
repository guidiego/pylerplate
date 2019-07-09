import os
import bjoern

from flask import render_template_string
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from utils.openapi import register_rules
from sqlalchemy import create_engine

from app import create_app
from database import db

app = create_app()
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

@manager.command
def run():

    @app.route('/redoc/')
    def render_redoc():
        template = '''
            <!DOCTYPE html>
            <html>
            <head>
                <title>ReDoc</title>
                <!-- needed for adaptive design -->
                <meta charset="utf-8"/>
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <link href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700" rel="stylesheet">

                <!--
                ReDoc doesn't change outer page styles
                -->
                
            </head>
            <body>
                <redoc spec-url="/swagger/"></redoc>
                <script src="https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js"> </script>
            </body>
            </html>
        '''

        return render_template_string(template)

    if app.config['FLASK_ENV'] == 'development':
        app.run(
            port=app.config['PORT'],
            host=app.config['HOST'],
        )
    else:
        print('Starting application in Production Mode', flush=True)
        bjoern.run(app, app.config['HOST'], int(app.config['PORT']))

if __name__ == '__main__':
    manager.run()

