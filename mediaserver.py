#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Dmitriy Zabrodin
# =============================================================================


from .app import app, db


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
    }

