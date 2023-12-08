from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token

import logging
import db
from db import DbManager
from password import PasswordManager
from datetime import datetime
import random
import os

app = Flask(__name__)

# SECRET
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")

# JWT
jwt = JWTManager(app)

# Password management
password_mgr = PasswordManager(app)

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
r,conn = db.connect()
db_mgr = DbManager()

# Function to verify user credentials


def verify_credentials(username, password):
    user = db_mgr.get_user(username)
    logger.info(f"User:{user}")
    try:
        stored_password = user.next().get('password', '')
        return password_mgr.check(stored_password, password)
    except  db_mgr.not_found():
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


def calculate_meals_scores(meal_ids):
    meals_scores = {}
    for meal_id in meal_ids:
        logger.info(f"meal id:{meal_id}")
        # Fetch the meal document from RethinkDB
        meal = r.table('meals').get(meal_id).run(conn)
        if meal:
            preparation_count = meal.get("preparation_count", 0)
            generation_date = meal.get(
                "generation_date", datetime.now())
            # Calculate the score based on the last committed date and preparation count
            score = calculate_score(generation_date, preparation_count)
            meals_scores[meal_id] = score
    return meals_scores


def calculate_score(generation_date, preparation_count):
    MAX_PREPARATION_COUNT = 10
    # Calculate the date factor (tends to 0 when last commit date tends to now)
    date_factor = 1 - (generation_date.timestamp()/datetime.now().timestamp())
    # Calculate the preparation count factor (tends to 1 when preparation count tends to 0)
    preparation_count_factor = 1 - (preparation_count / MAX_PREPARATION_COUNT)
    # Calculate the score based on a weighted sum of date and preparation count factors
    date_weight = 0.7
    preparation_count_weight = 0.3
    score = (date_weight * date_factor) + \
        (preparation_count_weight * preparation_count_factor)
    # Normalize the score to be between 0 and 1
    score = min(max(score, 0), 1)
    return score


def select_meals(meals_scores, num_meals_to_generate, default_meals):
    # Select meals randomly based on their scores (higher score means higher probability of selection)
    selected_meals_ids = default_meals
    while len(selected_meals_ids) < num_meals_to_generate and len(meals_scores) > 0:
        total_score = sum(meals_scores.values())
        # Normalize the scores to be probabilities
        probabilities = {meal_id: score /
                         total_score for meal_id, score in meals_scores.items()}
        # Choose a meal ID based on the probabilities
        meal_id = random.choices(
            list(meals_scores.keys()), weights=list(probabilities.values()))[0]
        if meal_id not in selected_meals_ids:
            selected_meals_ids.append(meal_id)
        # Remove the selected meal from the scores dictionary to avoid selecting it again
        meals_scores.pop(meal_id)
    return selected_meals_ids


def generate_meal(data):
    chosen_meals_ids = data.get("default_meal_ids", [])
    num_meals_to_generate = data.get("num_meals", 5)

    # Fetch all available meal IDs
    cursor = r.table('meals').pluck('id').run(conn)
    meal_ids = list(cursor)
    meal_ids = [meal['id'] for meal in meal_ids]

    # Calculate scores for all meals based on date and preparation count
    meals_scores = calculate_meals_scores(meal_ids)

    # Select meals based on the score (higher score means higher probability of selection)
    selected_meals_ids = select_meals(
        meals_scores, num_meals_to_generate, chosen_meals_ids)

    # Fetch the meal documents using the selected meal IDs
    menu_meals = []
    for meal_id in selected_meals_ids:
        meal = r.table('meals').get(meal_id).run(conn)
        if meal:
            menu_meals.append(meal)
    return menu_meals


def generate_menu_name():
    # List of positive adjectives
    positive_adjectives = ["Delicious", "Tasty", "Mouthwatering",
                           "Scrumptious", "Savory", "Appetizing", "Flavorful"]

    # Fetch synonyms of the word "meal"
    menu_synonyms = [
        "food selection",
        "cuisine list",
        "fish options",
        "feal choices",
        "dining selections",
        "culinary offerings",
        "edible array",
        "gastronomic options",
        "fare list",
        "dishes menu"
    ]
    # Combine positive adjectives and synonyms to create possible menu name components
    possible_components = positive_adjectives + menu_synonyms

    # Generate a random menu name by randomly selecting two components and joining them
    menu_adjective = random.choice(positive_adjectives)
    menu_synonyms = random.choice(menu_synonyms)
    random_menu_name = menu_adjective+" " + menu_synonyms
    return random_menu_name
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
        return jsonify({"message": "Meals imported successfully"}), 201
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
    logger.info("Create Menu")
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
    hashed_password = password_mgr.hash(password)

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
