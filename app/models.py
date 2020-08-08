import os
from datetime import datetime
from flask import url_for
from . import db


class Directory(db.Model):
    __tablename__ = 'directories'

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('directories.id'))
    parent = db.relationship('Directory',
                             backref=db.backref('directories', cascade="save-update, merge, delete", lazy='dynamic'),
                             remote_side=[id])
    path = db.Column(db.String(255), unique=True, nullable=False)
    removed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, nullable=False, index=True, default=datetime.utcnow)

    @property
    def name(self):
        return os.path.basename(self.path)

    def url_for(self):
        return url_for('show_folder', folder_id=self.id)

    def is_exists(self):
        return os.path.isdir(self.path)


class FileType(db.Model):
    __tablename__ = 'file_types'

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    title = db.Column(db.String(255), unique=True, nullable=False)


class File(db.Model):
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('directories.id'), nullable=False)
    parent = db.relationship('Directory', backref=db.backref('files', cascade="save-update, merge, delete", lazy='dynamic'))
    type_id = db.Column(db.Integer, db.ForeignKey('file_types.id'), nullable=False)
    type = db.relationship('FileType', backref=db.backref('files', cascade="save-update, merge, delete", lazy='dynamic'))
    filename = db.Column(db.String(255), nullable=False)
    removed = db.Column(db.Boolean, default=False)
    updated_at = db.Column(db.DateTime, nullable=False, index=True, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, nullable=False, index=True, default=datetime.utcnow)

    @property
    def path(self):
        return os.path.join(self.parent.path, self.filename)

    @property
    def name(self):
        return self.filename

    @property
    def stem(self):
        return os.path.splitext(self.filename)[0]

    @property
    def suffix(self):
        return os.path.splitext(self.filename)[1]

    def url_for(self):
        return url_for('show_file', file_id=self.id)

    def url_for_preview(self):
        return url_for('show_preview', file_id=self.id)

    def is_exists(self):
        return os.path.isfile(self.path)
