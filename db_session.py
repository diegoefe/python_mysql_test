import db_session_mysql as my

class DB_Session (my.DB_Session_MySQL):
    def __init__(self, username, password, db_id):
		 my.DB_Session_MySQL.__init__(self, username, password, db_id)
    
        

