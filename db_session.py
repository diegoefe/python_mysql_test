import os

if os.environ.has_key("USE_DUMMY"):
    from db_session_dummy import Dummy as db
else:
    from db_session_mysql import DB_Session_MySQL as db


class DB_Session (db):
    def __init__(self, username, password, db_id):
		 db.__init__(self, username, password, db_id)

