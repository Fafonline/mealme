from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token

import logging
import random
import os
from lib.db import DbManager
from lib.credentialManager import CredentialManager
from lib.mealSelector import MealSelector
from lib.mealDecorator import MealDecorator

app = Flask(__name__)

# SECRET
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")

# JWT
jwt = JWTManager(app)

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# RethinkDB configuration
db_mgr = DbManager()
# db_mgr.purge_meals()
# Password management
credential_mgr = CredentialManager(app, db_mgr)

# Meal selector
mealSelector = MealSelector(db_mgr)

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

# Function to verify user credentials
def verify_credentials(username, password):
    user = db_mgr.get_user(username)
    logger.info(f"User:{user}")
    try:
        stored_password = user.next().get('password', '')
        return credential_mgr.check(stored_password, password)
    except  db_mgr.not_found():
        return False

# Flask route to handle meal retrieval by ID
@app.route("/meal/<meal_id>", methods=["GET"])
@jwt_required()
def get_meal_by_id(meal_id):
    meal = db_mgr.get_meal(meal_id)
    if meal:
        return jsonify(meal)
    return jsonify({"error": "Meal not found"}), 404

# Flask route to handle meal retrieval
@app.route("/meals", methods=["GET"])
@jwt_required()
def get_meals():
    meals = db_mgr.get_meals_order_by_name()
    print(meals)
    return jsonify(meals)

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
    meal_unique_id = db_mgr.generate_uuid()
    data["id"] = str(meal_unique_id)
    data["preparation_count"] = 0
    db_mgr.insert_data(meal_unique_id,data)
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
            meal_unique_id = db_mgr.generate_uuid()
            # Create a new meal with the given name
            new_meal = {
                "id": str(meal_unique_id),
                "name": meal_name,
                "preparation_count": 0
            }
            # Meal Decorator
            mealDecorator  = MealDecorator()
            new_meal = mealDecorator.get_ingredients(new_meal)
            logger.info(new_meal)
            # Insert the new meal into the database
            db_mgr.insert_data(meal_unique_id,new_meal)
            imported_meals.append(new_meal)
        return jsonify({"message": "Meals imported successfully"}), 201
    return jsonify({"error": "Invalid payload format"}), 400

# Flask route to handle meal update
@app.route("/meal/<meal_id>", methods=["PATCH"])
@jwt_required()
def update_meal(meal_id):
    data = request.get_json()
    db_mgr.update_data(meal_id,data)
    updated_meal = db_mgr.get_meal(meal_id)
    if updated_meal:
        return jsonify(updated_meal)
    return jsonify({"error": "Meal not found"}), 404

# Flask route to handle menu retrieval by ID
@app.route("/menu/<menu_id>", methods=["GET"])
@jwt_required()
def get_menu_by_id(menu_id):
    menu = db_mgr.get_menu(menu_id)
    if menu:
        return jsonify(menu)
    return jsonify({"error": "Menu not found"}), 404

# Flask route to handle menu retrieval
@app.route("/menus", methods=["GET"])
def get_menus():
    menus = db_mgr.get_menus_ordered_by_date()
    return jsonify(menus)

# Flask route to handle menu creation
@app.route("/menu/", methods=["POST"])
@jwt_required()
def create_menu():
    logger.info("Create Menu")
    data = request.get_json()
    menu_meals = mealSelector.generate_meals(data)
    menu_unique_id = db_mgr.generate_uuid()
    menu_data = {
        "id": str(menu_unique_id),
        "meals": menu_meals,
        "name": generate_menu_name(),
        "status": "Pending"
    }
    db_mgr.insert_menu(menu_unique_id,menu_data)
    return jsonify(menu_data), 201

# Flask route to handle menu update
@app.route("/menu/<menu_id>", methods=["PATCH"])
@jwt_required()
def update_menu(menu_id):
    data = request.get_json()
    menu_meals = mealSelector.generate_meals(data)
    menu_data = {
        "id": menu_id,
        "meals": menu_meals
    }
    db_mgr.update_menu(menu_id,menu_data)
    updated_menu = db_mgr.get_menu(menu_id)
    if updated_menu:
        return jsonify(updated_menu)
    return jsonify({"error": "Menu not found"}), 404

# Flask route to handle menu commit
@app.route("/commit/<menu_id>", methods=["POST"])
def commit_menu(menu_id):
    commit_date = db_mgr.get_commit_date()
    menu = db_mgr.get_menu(menu_id)
    if menu:
        for meal_id in menu["meals"]:
            meal_key = meal_id["id"]
            meal = db_mgr.get_meal(meal_key)
            if meal:
                meal["preparation_count"] = meal.get(
                    "preparation_count", 0) + 1
                meal["last_commit_date"] = commit_date
                db_mgr.update_data(meal_key,meal)
        menu["status"] = "Committed"
        menu["generation_date"] = commit_date
        db_mgr.update_menu(menu_id,menu)
        return jsonify(menu), 201
    return jsonify({"error": "Menu not found"}), 404

# Flask route to handle meal deletion
@app.route("/meal/<meal_id>", methods=["DELETE"])
def delete_meal(meal_id):
    db_mgr.delete_meal(meal_id)
    return jsonify({"message": "Meal deleted successfully"}), 200

# Flask route to handle user registration
@app.route("/register/", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username", "")
    password = data.get("password", "")

    # Hash the user's password
    hashed_password = credential_mgr.hash(password)

    # Store the username and hashed password in the database
    user_data = {
        "username": username,
        "password": hashed_password
    }
    db_mgr.insert_user(user_data)
    return jsonify({"message": "User registered successfully"}), 201

# Flask route for login
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

# Flask route for tracked ingredient

@app.route("/tracked_ingredient", methods=["POST"])
def tracked_ingredient():
    data = request.get_json()
    tracked_ingredients = data.get("ingredients")
    db_mgr.set_tracked_ingredients(tracked_ingredients)
    return jsonify({"message: Tracked ingredient imported successfully"})

# Main
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
