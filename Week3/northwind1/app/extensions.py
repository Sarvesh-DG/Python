from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

db = SQLAlchemy()


def commit_or_rollback():
    """Commit the current unit of work and clear the session on failure."""
    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        raise
