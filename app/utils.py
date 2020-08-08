import os
import magic
from sqlalchemy.exc import SQLAlchemyError
from . import db
from .models import Directory, File, FileType
from pathlib import Path


EXCLUDE_PREFIXES = ['$RECYCLE.BIN', 'System Volume Information']


def get_type_by_title(title):
    if (_type := db.session.query(FileType).filter_by(title=title).first()) is not None:
        return _type
    _type = FileType(title=title)
    try:
        db.session.add(_type)
        db.session.commit()
        return _type
    except SQLAlchemyError as e:
        db.session.rollback()


def get_db_object(path):
    if os.path.isdir(path):
        try:
            return True, db.session.query(Directory).filter_by(path=path).one()
        except SQLAlchemyError:
            return False, Directory(parent=db.session.query(Directory).filter_by(path=os.path.dirname(path)).first(),
                                    path=path)
    elif os.path.isfile(path):
        try:
            return True, db.session.query(File).filter_by(
                parent=db.session.query(Directory).filter_by(path=os.path.dirname(path)).one(),
                filename=os.path.basename(path)
            ).one()
        except SQLAlchemyError:
            parent = db.session.query(Directory).filter_by(path=os.path.dirname(path)).first()
            if (probable_file_type := magic.from_file(path, mime=True).split('/')[0]) in ('image', 'video'):
                file_type = get_type_by_title(probable_file_type)
                if file_type is not None:
                    return False, File(type=file_type, parent=parent, filename=os.path.basename(path))
    return False, None


def update(dir_object, current_content):
    try:
        for f in dir_object.files:
            if not f.is_exists() or f.name not in current_content:
                db.session.delete(f)

        db.session.commit()

        for filename in current_content:
            db_exists, db_file = get_db_object(os.path.join(dir_object.path, filename))
            if not db_exists:
                db.session.add(db_file)

        db.session.commit()

    except SQLAlchemyError as e:
        db.session.rollback()
        print(e)


def walk_on_tree(path):
    try:
        return db.session.query(Directory).filter_by(path=path).one().path
    except SQLAlchemyError:
        walk_on_tree(os.path.dirname(path))


def scan_tree(path, only_top=False):
    if not os.path.isdir(path):
        return

    top_dir = walk_on_tree(path)

    for parent, _, files in os.walk(top_dir, topdown=True):
        if not any(part in EXCLUDE_PREFIXES for part in Path(parent).parts):
            try:
                exists_in_db, parent_object = get_db_object(parent)
                if not exists_in_db:
                    db.session.add(parent_object)
                    db.session.commit()
                update(parent_object, files)
            except ValueError:
                pass
            except SQLAlchemyError as e:
                db.session.rollback()
                print(e)
        if only_top:
            break
