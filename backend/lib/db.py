from rethinkdb import RethinkDB
import os
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Add a file handler to log errors to a file
# Change this path to your desired log file location
log_file_path = "rethinkdb_errors.log"
file_handler = logging.FileHandler(log_file_path)
file_handler.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class DbManager:
    def __init__(self):
        self.r, self.conn = self.connect()

    def connect(self):
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

        return r, conn

    def reconnect(self):
        try:
            self.conn.close()
        except RethinkDB.RqlDriverError:
            pass  # Ignore errors when closing the connection

        # Attempt to reconnect
        self.r, self.conn = self.connect()

    def execute_query(self, query):
        try:
            result = query.run(self.conn)
            return result
        except RethinkDB.RqlDriverError as e:
            error_message = f"RethinkDB error: {e}"
            logger.error(error_message)
            logger.warning("Lost connection to RethinkDB. Reconnecting...")
            self.reconnect()
            result = query.run(self.conn)
            return result

    def get_user(self, username):
        return self.execute_query(self.r.table('users').filter({'username': username}))

    def insert_user(self, user):
        self.execute_query(self.r.table('users').insert(user))

    def get_meal(self, meal_id):
        return self.execute_query(self.r.table('meals').get(meal_id))

    def get_meals_order_by_name(self):
        return list(self.execute_query(self.r.table('meals').order_by('name')))

    def not_found(self):
        self.r.errors.ReqlCursorEmpty

    def get_meals_ids(self):
        return self.execute_query(self.r.table('meals').pluck('id'))

    def generate_uuid(self):
        return self.r.uuid().run(self.conn)

    def insert_data(self, id, data):
        self.execute_query(self.r.table('meals').insert(data))

    def update_data(self, id, data):
        self.execute_query(self.r.table('meals').get(id).update(data))

    def get_menu(self, id):
        return self.execute_query(self.r.table('menus').get(id))

    def get_menus_ordered_by_date(self):
        return list(self.execute_query(self.r.table('menus').filter({'status': 'Committed'}).order_by(
            self.r.desc('generation_date'))))

    def insert_menu(self, id, menu):
        self.execute_query(self.r.table('menus').insert(menu))

    def update_menu(self, id, menu):
        self.execute_query(self.r.table('menus').get(id).update(menu))

    def get_commit_date(self):
        return self.execute_query(self.r.now())

    def delete_meal(self, id):
        self.execute_query(self.r.table('meals').get(id).delete())

    def get_tracked_ingredients(self):
        return self.execute_query(self.r.table('tracked_ingredients').pluck('name'))

    def set_tracked_ingredients(self, ingredients):
        self.execute_query(self.r.table('tracked_ingredients').delete())
        for ingredient in ingredients:
            self.execute_query(self.r.table(
                'tracked_ingredients').insert(ingredient))

    def purge_meals(self):
        self.execute_query(self.r.table("meals").delete())
