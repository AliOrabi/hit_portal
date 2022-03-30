from flask import current_app as app
from app.models import User
from app import db
from app.logger import log

TEST_USERS_NUMBER = 20


def init_db(add_test_data: bool = False):
    """fill database by initial data

    Args:
        add_test_data (bool, optional): will add test data if set True. Defaults to False.
    """
    log(log.INFO, "Add admin account: %s", app.config["ADMIN_USER"])
    User(
        username=app.config["ADMIN_USER"],
        password=app.config["ADMIN_PASS"],
    ).save(False)
    if add_test_data:
        log(log.INFO, "Generate test data")
        for i in range(TEST_USERS_NUMBER):
            User(username=f"user_{i}", password="pass").save(False)

    db.session.commit()
