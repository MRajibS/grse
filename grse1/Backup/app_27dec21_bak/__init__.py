import jwt
from datetime import timedelta
from flask_cors import CORS, cross_origin
from flasgger import Swagger, swag_from
from flask_sqlalchemy import SQLAlchemy
from Settings.config import app_config
from flask import Flask, request, jsonify, make_response, redirect, session
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from sqlalchemy import or_
from sqlalchemy import desc

db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    app.config['SWAGGER'] = {
        'swagger': '2.0',
        'title': 'GRSE',
        'description': "โ โฏ  ๐ฟ๐๐๐ ๐๐ ๐ ๐ฝ๐ฐ๐พ๐ฟ๐๐๐ ๏ผกโ๐ข ๐๐๐๐๐ ๐๐ ๐๐๐๐๐๐ ๐๐๐๐๐ ๐๐๐ ๐ฑ๐๐๐๐ ๐ฑ๐๐๐๐๐๐๐๐  โค โโฟโ.\
        \n๏ธปใโไธ   ---      ---       ---         ---            ---              ---                ---               ---\n๐ฌ๐๐๐๐๐ : ๐พ๐๐๐๐๐๐๐ ๐ธ๐๐๐๐๐๐๐๐ (โฃ_โข) \n ๏ธปใโไธ   ---      ---       ---         ---            ---              ---                ---               ---"
                       "\n ๐ฎ๐๐๐๐๐๐  : ษชแด แดษด ษชษด๊ฐแดแดแดแดส\n๏ธปใโไธ   ---      ---       ---         ---            ---              ---                ---               ---\n๐๐๐๐๐ : ๐๐๐๐๐๐๐๐๐๐๐.๐๐๐@๐๐๐๐๐.๐๐๐",
        'contact': {
            'Developer': '๐พ๐๐๐๐๐๐๐ ๐ธ๐๐๐๐๐๐๐๐',
            'Email': 'themarinade.ind@@gmail.com',
            'Company': 'IVAN Infotech',
        },

        'schemes': [
            'http'
        ],

        'license': {
            'name': 'private'
        },
        'tags': [
            {
                'name': 'Users',
                'description': 'The basic unit of authentication'
            },
            {
                'name': 'Shifts',
                'description': ''
            },
            {
                'name': 'Subarea',
                'description': ''
            },
            {
                'name': 'Units',
                'description': ''
            },

            {
                'name': 'Admin',
                'description': 'Overall user that moderates the API'
            },

            {
                'name': 'Department',
                'description': ''
            },
            {
                'name': 'Designations',
                'description': ''
            },
        ],

        'specs_route': '/apidocs/'
    }

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    CORS(app)
    swagger = Swagger(app)

    @app.route('/')
    def index():
        return redirect('/apidocs/')

    from app.auth.admin_auth.views import admin_auth
    from app.units.views import units_view
    from app.department.views import Department_View
    from app.designations.views import Designations_View
    from app.shifts.views import Shifts_View
    from app.subarea.views import Subarea_View
    from app.user.views import users_view
    from app.group.views import Group_View
    from app.user_terminals.views import User_terminals_view
    from app.terminals.views import Terminals_view
    from app.group_terminals.views import Group_Terminals_View

    app.register_blueprint(units_view)
    app.register_blueprint(Department_View)
    app.register_blueprint(Shifts_View)
    app.register_blueprint(Subarea_View)
    app.register_blueprint(Designations_View)
    app.register_blueprint(users_view)
    app.register_blueprint(admin_auth)
    app.register_blueprint(Group_View)
    app.register_blueprint(User_terminals_view)
    app.register_blueprint(Terminals_view)
    app.register_blueprint(Group_Terminals_View)

    return app
