from rethinkdb import RethinkDB
import os
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


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

        return r,conn

    def get_user(self, username):
        return self.r.table('users').filter({'username': username}).run(self.conn)
    
    def insert_user(self,user):
            self.r.table('users').insert(user).run(self.conn)

    def get_meal(self,meal_id):
        return self.r.table('meals').get(meal_id).run(self.conn)

    def get_meals_order_by_name(self):
        return list(self.r.table('meals').order_by('name').run(self.conn))

    def not_found(self):
        self.r.errors.ReqlCursorEmpty
    
    def get_meals_ids(self):
        return self.r.table('meals').pluck('id').run(self.conn)
    
    def generate_uuid(self):
        return self.r.uuid().run(self.conn)
    
    def insert_data(self,id,data):
          self.r.table('meals').insert(data).run(self.conn)
    
    def update_data(self,id,data):
        self.r.table('meals').get(id).update(data).run(self.conn)
    
    def get_menu(self,id):
        return self.r.table('menus').get(id).run(self.conn)
    
    def get_menus_ordered_by_date(self):
        return list(self.r.table('menus').filter({'status': 'Committed'}).order_by(
        self.r.desc('generation_date')).run(self.conn))

    def insert_menu(self,id, menu):
            self.r.table('menus').insert(menu).run(self.conn)

    def update_menu(self,id, menu):
        self.r.table('menus').get(id).update(menu).run(self.conn)
    
    def get_commit_date(self):
        return self.r.now().run(self.conn)
    
    def delete_meal(self,id):
        self.r.table('meals').get(id).delete().run(self.conn)
    
    def purge_meals(self):
        return self.r.table("meals").delete().run(self.conn)