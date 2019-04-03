import os
from flask import render_template_string
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
        '''.format(
            app.config['HOST'], app.config['PORT']
        )

        return render_template_string(template)

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

    engine = create_engine(url_without_db)
    conn = engine.connect()
    conn.execute('create database {}'.format(db_name))
    conn.close()


@manager.command
def create_module(module_name):
    api = '''
from flask import request, make_response
from flask_apispec import MethodResource

from modules.{low_name}.models import {capitalized}
from modules.{low_name}.schemas import {capitalized}Schema
from utils.openapi import api
from utils import http_status

class {capitalized}Resource(MethodResource):
    base_url = '/{low_name}'
    default_tag = '{capitalized}'

    @staticmethod
    @api(
        path='/',
        methods=['POST'],
        use_kwargs={capitalized}Schema(),
        marshal_with={capitalized}Schema(),
        description='Create an {capitalized}'
    )
    def create_{low_name}s(**kwargs):
        data = request.get_json()
        {low_name}_obj = {capitalized}Schema(strict=True).load(data)
        {low_name}_obj.data.save(flush=True, commit=True)

        permission = {capitalized}Permission.set_common({low_name}_obj.data.id)
        permission.save(flush=True, commit=True)

        return {capitalized}Schema(many=False).dump({low_name}_obj.data).data
        

    @staticmethod
    @api(
        path='/',
        marshal_with={capitalized}Schema(many=True),
        description='Get all {capitalized}s'
    )
    def get_{low_name}s():
        return {capitalized}Schema(many=True).dump({capitalized}.get_all()).data

    @staticmethod
    @api(
        path='/<int:id>',
        marshal_with={capitalized}Schema(many=False),
        description='Get an {capitalized}'
    )
    def get_{low_name}(id):
        return {capitalized}Schema(many=False).dump({capitalized}.get(id)).data

    @staticmethod
    @api(
        path='/<int:id>',
        methods=['DELETE'],
        description='Delete an {capitalized}'
    )
    def delete_{low_name}(id):
        {low_name} = {capitalized}.get(id)
        {low_name}.delete()
        return make_response('', http_status.HTTP_204_NO_CONTENT)

    @staticmethod
    @api(
        path='/<int:{low_name}_id>',
        methods=['PUT'],
        use_kwargs={capitalized}Schema(exclude=['password']),
        marshal_with={capitalized}Schema(many=False),
        description='Update an {capitalized}'
    )
    def update_{low_name}(**kwargs):
        {low_name}_id = request.view_args.get('{low_name}_id')
        {low_name}_obj = {capitalized}Schema(strict=True).load(
            kwargs, instance={capitalized}.get({low_name}_id), partial=True
        )

        {low_name}_obj.data.save(flush=True, commit=True, pre_save=False)

        return {capitalized}Schema(many=False).dump({low_name}_obj.data).data
    '''.format(low_name=module_name, capitalized=module_name.capitalize())

    models = '''
import enum

from app import bcrypt
from database import db

class {capitalized}(db.Model):
    __tablename__ = '{low_name}'
    '''.format(low_name=module_name, capitalized=module_name.capitalize())

    schemas = '''
from utils.marshmallow import BaseSchema
from .models import {capitalized}

class {capitalized}Schema(BaseSchema):
    class Meta:
        model = {capitalized}
    '''.format(capitalized=module_name.capitalize())

    module_path = './modules/{}'.format(module_name)
    os.mkdir(module_path)

    for (name, template) in [('api', api), ('models', models), ('schemas', schemas)]:
        with open('{}/{}.py'.format(module_path, name), 'w') as f:
            f.write(template)

if __name__ == '__main__':
    manager.run()

