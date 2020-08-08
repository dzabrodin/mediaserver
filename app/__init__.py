#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Dmitriy Zabrodin
# =============================================================================

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from ..config import Config


def create_app(test_config=None):
    flask_app = Flask(__name__, instance_relative_config=True)

    if test_config is not None:
        flask_app.config.from_mapping(test_config)
    else:
        flask_app.config.from_object(Config)

    return flask_app


app = create_app()
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bootstrap = Bootstrap(app)
moment = Moment(app)

from . import routes