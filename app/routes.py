import os
from natsort import natsorted
from flask import request, render_template, redirect, send_from_directory, url_for
from sqlalchemy.exc import SQLAlchemyError
from . import app
from .models import db, Directory, File, FileType
from .utils import scan_tree


@app.route('/')
def show_folder():
    data = {
        'self': None,
        'root': False,
        'directories': [],
        'files': {},
    }
    try:
        d = db.session.query(Directory).filter_by(id=request.args.get('folder_id', None, int)).one()
    except SQLAlchemyError:
        data['directories'] = db.session.query(Directory).filter(Directory.parent_id.is_(None)).all()
        data['root'] = True
    else:
        data['self'] = d
        data['self_id'] = d.id
        data['parent'] = d.parent
        data['directories'] = d.directories.order_by('path').all()
        for f in db.session.query(File).group_by('type_id'):
            data['files'].setdefault(db.session.query(FileType).filter(FileType.id == f.type_id).first().title, [])\
                .extend(list(natsorted(db.session.query(File).filter(File.parent_id == d.id, File.type_id == f.type_id),
                                       key=lambda file: file.filename)))
    return render_template('folder.html', data=data)


@app.route('/icon')
def show_folder_icon():
    return send_from_directory(app.static_folder, 'folder.png')


@app.route('/file/<int:file_id>')
def show_file(file_id):
    f = File.query.get_or_404(file_id)
    data = {
        'self': f,
        'root': False,
        'directories': [],
        'files': {},
    }
    return render_template('file.html', data=data)


@app.route('/file/<int:file_id>/preview')
def show_preview(file_id):
    f = File.query.get_or_404(file_id)
    return send_from_directory(*os.path.split(f.path))


@app.route('/<int:folder_id>/rescan')
def rescan_folder(folder_id):
    d = Directory.query.get_or_404(folder_id)
    scan_tree(d.path)
    return redirect(d.url_for())


@app.route('/<int:folder_id>/rmtree')
def db_rmtree(folder_id):
    d = Directory.query.get_or_404(folder_id)
    parent = d.parent
    try:
        db.session.delete(d)
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        print(e)
    else:
        if parent is not None:
            scan_tree(parent.path, only_top=True)
            return redirect(parent.url_for())
        else:
            return redirect(url_for('show_folder', folder_id=None))
