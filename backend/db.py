from rethinkdb import RethinkDB
import os
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def connect():
    # RethinkDB configuration
    r = RethinkDB()
    RDB_HOST = "db"  # Replace with your RethinkDB server host
    # RDB_HOST = "5.135.190.86"  # Replace with your RethinkDB server host
    # RDB_HOST = "127.0.0.1"  # Replace with your RethinkDB server host
    RDB_PORT = 28015              # Replace with your RethinkDB server port
    RDB_DB = "meal_me"           # Replace with your RethinkDB database name
    # Replace with your RethinkDB password
    RDB_PASSWORD = os.environ.get("DB_PASSWORD")

    # Connect to RethinkDB
    conn = r.connect(host=RDB_HOST, port=RDB_PORT,
                     db=RDB_DB, password=RDB_PASSWORD)

    # Create tables if they don't exist
    tables = ["meals", "menus", "users"]
    for table in tables:
        try:
            r.table_create(table).run(conn)
            logger.info(f"Table '{table}' created.")
        except r.errors.ReqlOpFailedError:
            logger.info(f"Table '{table}' already exists.")
    return r,conn

class DbManager:
    def __init__(self):
        self.r, self.conn = connect()
    def get_user(self, username):
        return self.r.table('users').filter({'username': username}).run(self.conn)
    def not_found(self):
        self.r.errors.ReqlCursorEmpty