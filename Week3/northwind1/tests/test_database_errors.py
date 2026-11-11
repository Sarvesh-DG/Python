from unittest.mock import patch

import pytest
from sqlalchemy.exc import SQLAlchemyError

from app.extensions import commit_or_rollback


def test_commit_failure_rolls_back_and_reraises(app):
    with app.app_context():
        with patch("app.extensions.db.session.commit", side_effect=SQLAlchemyError("failure")):
            with patch("app.extensions.db.session.rollback") as rollback:
                with pytest.raises(SQLAlchemyError):
                    commit_or_rollback()
                rollback.assert_called_once_with()
