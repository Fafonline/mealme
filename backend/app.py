from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_bcrypt import Bcrypt
import logging
from rethinkdb import RethinkDB
import os

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def add_cors_headers(response):
    # Replace "http://localhost:80" with the actual URL of your Angular application
    # response.headers['Access-Control-Allow-Origin'] = 'http://localhost'
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, PATCH, DELETE, OPTIONS'
    return response


@app.after_request
def after_request(response):
    response = add_cors_headers(response)
    return response


# RethinkDB configuration
r = RethinkDB()
RDB_HOST = "db"  # Replace with your RethinkDB server host
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

# Function to hash and check passwords


def hash_password(password: str) -> str:
    return bcrypt.generate_password_hash(password).decode('utf-8')


def check_password(hashed_password: str, password_to_check: str) -> bool:
    return bcrypt.check_password_hash(hashed_password, password_to_check)

# Function to verify user credentials


def verify_credentials(username, password):
    user = r.table('users').filter({'username': username}).run(conn)
    logger.info(f"User:{user}")
    try:
        stored_password = user.next().get('password', '')
        return check_password(stored_password, password)
    except r.errors.ReqlCursorEmpty:
        return False

# Flask route to handle meal retrieval by ID


@app.route("/meal/<meal_id>", methods=["GET"])
@jwt_required()
def get_meal_by_id(meal_id):
    meal = r.table('meals').get(meal_id).run(conn)
    if meal:
        return jsonify(meal)
    return jsonify({"error": "Meal not found"}), 404

# Flask route to handle meal retrieval


@app.route("/meals", methods=["GET"])
@jwt_required()
def get_meals():
    meals = list(r.table('meals').order_by('name').run(conn))
    return jsonify(meals)

# Flask route to handle meal creation


@app.route("/meal/", methods=["POST"])
@jwt_required()
def create_meal():
    data = request.get_json()
    meal_unique_id = r.uuid().run(conn)
    data["id"] = str(meal_unique_id)
    data["preparation_count"] = 0
    r.table('meals').insert(data).run(conn)
    return jsonify(data), 201

# Flask route to handle meal import


@app.route("/import/", methods=["POST"])
@jwt_required()
def import_meals():
    data = request.get_json()
    logger.info(f"Import:{data}")
    if "meals" in data and isinstance(data["meals"], list):
        imported_meals = []
        for meal_name in data["meals"]:
            # Generate a new unique ID for the meal
            meal_unique_id = r.uuid().run(conn)
            # Create a new meal with the given name
            new_meal = {
                "id": str(meal_unique_id),
                "name": meal_name,
                "preparation_count": 0
            }
            # Insert the new meal into the database
            r.table('meals').insert(new_meal).run(conn)
            imported_meals.append(new_meal)
        return jsonify({"imported_meals": imported_meals}), 201
    return jsonify({"error": "Invalid payload format"}), 400

# Flask route to handle meal update


@app.route("/meal/<meal_id>", methods=["PATCH"])
@jwt_required()
def update_meal(meal_id):
    data = request.get_json()
    r.table('meals').get(meal_id).update(data).run(conn)
    updated_meal = r.table('meals').get(meal_id).run(conn)
    if updated_meal:
        return jsonify(updated_meal)
    return jsonify({"error": "Meal not found"}), 404

# Flask route to handle menu retrieval by ID


@app.route("/menu/<menu_id>", methods=["GET"])
@jwt_required()
def get_menu_by_id(menu_id):
    menu = r.table('menus').get(menu_id).run(conn)
    if menu:
        return jsonify(menu)
    return jsonify({"error": "Menu not found"}), 404

# Flask route to handle menu retrieval


@app.route("/menus", methods=["GET"])
def get_menus():
    menus = list(r.table('menus').filter({'status': 'Committed'}).order_by(
        r.desc('generation_date')).run(conn))
    return jsonify(menus)

# Flask route to handle menu creation


@app.route("/menu/", methods=["POST"])
@jwt_required()
def create_menu():
    data = request.get_json()
    menu_meals = generate_meal(data)
    menu_unique_id = r.uuid().run(conn)
    menu_data = {
        "id": str(menu_unique_id),
        "meals": menu_meals,
        "name": generate_menu_name(),
        "status": "Pending"
    }
    r.table('menus').insert(menu_data).run(conn)
    return jsonify(menu_data), 201

# Flask route to handle menu update


@app.route("/menu/<menu_id>", methods=["PATCH"])
@jwt_required()
def update_menu(menu_id):
    data = request.get_json()
    menu_meals = generate_meal(data)
    menu_data = {
        "id": menu_id,
        "meals": menu_meals
    }
    r.table('menus').get(menu_id).update(menu_data).run(conn)
    updated_menu = r.table('menus').get(menu_id).run(conn)
    if updated_menu:
        return jsonify(updated_menu)
    return jsonify({"error": "Menu not found"}), 404

# Flask route to handle menu commit


@app.route("/commit/<menu_id>", methods=["POST"])
def commit_menu(menu_id):
    commit_date = r.now().run(conn)
    menu = r.table('menus').get(menu_id).run(conn)
    if menu:
        for meal_id in menu["meals"]:
            meal_key = meal_id["id"]
            meal = r.table('meals').get(meal_key).run(conn)
            if meal:
                meal["preparation_count"] = meal.get(
                    "preparation_count", 0) + 1
                meal["last_commit_date"] = commit_date
                r.table('meals').get(meal_key).update(meal).run(conn)
        menu["status"] = "Committed"
        menu["generation_date"] = commit_date
        r.table('menus').get(menu_id).update(menu).run(conn)
        return jsonify(menu), 201
    return jsonify({"error": "Menu not found"}), 404

# Flask route to handle meal deletion


@app.route("/meal/<meal_id>", methods=["DELETE"])
def delete_meal(meal_id):
    r.table('meals').get(meal_id).delete().run(conn)
    return jsonify({"message": "Meal deleted successfully"}), 200

# Flask route to handle user registration


@app.route("/register/", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username", "")
    password = data.get("password", "")

    # Hash the user's password
    hashed_password = hash_password(password)

    # Store the username and hashed password in the database
    user_data = {
        "username": username,
        "password": hashed_password
    }
    r.table('users').insert(user_data).run(conn)
    return jsonify({"message": "User registered successfully"}), 201


@app.route("/login/", methods=["POST"])
def login():
    logger.info("Login ...")
    data = request.get_json()
    username = data.get("username", "")
    password = data.get("password", "")
    # Verify the user's credentials (e.g., username and password)

    if verify_credentials(username, password):
        # Create an access token containing the user's identity (e.g., username)
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
