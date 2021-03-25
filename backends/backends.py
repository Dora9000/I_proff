
from .create_session import create_session, close_session
from .create_db import create_db, close_db


def setup_backends(app):
    app.on_startup.append(create_session)
    app.on_cleanup.append(close_session)

    app.on_startup.append(create_db)
    app.on_cleanup.append(close_db)

