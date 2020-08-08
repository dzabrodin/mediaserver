#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Dmitriy Zabrodin
# =============================================================================

import sys
import os

if sys.version_info[0] < 3:
    sys.stderr.write("You need Python 3 or later to run this script!\n")
    sys.exit(1)

project_path = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'EZLXO0sZHmhi9MeClw1A')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///' + os.path.join(project_path, 'db.sqlite'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BOOTSTRAP_SERVE_LOCAL = True
