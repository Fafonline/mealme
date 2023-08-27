from flask import Flask, request, jsonify
from couchbase.auth import PasswordAuthenticator
from couchbase.cluster import Cluster
from couchbase.options import (ClusterOptions, ClusterTimeoutOptions,
                               QueryOptions)

import secrets
import uuid
from couchbase.n1ql import N1QLQuery
import time
from datetime import datetime
import random


app = Flask(__name__)
# CORS(app, resources={r"/commit/*": {"origins": "*"}})


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


COUCHBASE_MEAL_PREFIX = "meal::"
COUCHBASE_MENU_PREFIX = "menu::"
COUCHBASE_BUCKET = "meal_me"  # Replace with your actual bucket name

def connect_to_couchbase():
 # Couchbase configuration
 COUCHBASE_URL = "couchbase://db"
 COUCHBASE_USER = "guest"
 COUCHBASE_PASSWORD = "password"


 # Initialize Couchbase cluster and authenticate
 authenticator = PasswordAuthenticator(COUCHBASE_USER, COUCHBASE_PASSWORD)
 options = ClusterOptions(authenticator)
 cluster = Cluster(COUCHBASE_URL,options)
 # Connect to the bucket
 bucket = cluster.bucket(COUCHBASE_BUCKET)
 return cluster, bucket

cluster = None
bucket  = None

max_retries = 30
retry_interval = 1  # Retry every 1 second
retry_count = 0
while retry_count < max_retries:
    try:
        cluster, bucket = connect_to_couchbase()
        print("Connected to Couchbase!")
        break  # Connection successful, break out of the loop
    except Exception as e:
        print(f"Failed to connect to Couchbase: {str(e)}")
        retry_count += 1
        time.sleep(retry_interval)

# Check if the connection was successful
if retry_count == max_retries:
    print("Failed to connect to Couchbase after max retries.")
    exit


collection = bucket.default_collection()


def generate_random_id():
    # Generate an 8-character string containing capital letters and numbers
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return ''.join(secrets.choice(alphabet) for _ in range(8))

def format_field_name(name):
    # Convert field name to lowercase and replace spaces with "__"
    return name.lower().replace(" ", "__")


@app.route("/meal/<meal_id>", methods=["GET"])
def get_meal_by_id(meal_id):
    meal_key = COUCHBASE_MEAL_PREFIX + meal_id
    meal = collection.get(meal_key).value
    if meal:
        return jsonify(meal)
    return jsonify({"error": "Meal not found"}), 404

# Route function to get all meals
@app.route("/meals", methods=["GET"])
def get_meals():
    # Fetch all meals from the Couchbase bucket
    query = "SELECT id, name, description FROM `{}` WHERE META().id LIKE 'meal::%' ORDER BY name".format(COUCHBASE_BUCKET)
    result = cluster.query(query)
    meals = [row for row in result]
    
    # Return the meals as an array of JSON documents in the response
    return jsonify(meals)

@app.route("/meal/", methods=["POST"])
def create_meal():
    data = request.get_json()

    # Generate a new unique ID for the meal
    meal_unique_id = generate_random_id()
    data["id"] = meal_unique_id
    data["preparation_count"]=0
    # data["test"]="test"
    meal_key = COUCHBASE_MEAL_PREFIX + meal_unique_id
    collection.insert(meal_key, data)
    return jsonify(data), 201


@app.route("/meal/<meal_id>", methods=["PATCH"])
def update_meal(meal_id):
    data = request.get_json()
    meal_key = COUCHBASE_MEAL_PREFIX + meal_id
    current_meal = collection.get(meal_key).value
    if not current_meal:
        return jsonify({"error": "Meal not found"}), 404

    # Update the current meal document with the new data
    current_meal.update(data)
    collection.replace(meal_key, current_meal)
    return jsonify(current_meal)


@app.route("/menu/<menu_id>", methods=["GET"])
def get_menu_by_id(menu_id):
    menu_key = COUCHBASE_MENU_PREFIX + menu_id
    menu = collection.get(menu_key).value
    if menu:
        return jsonify(menu)
    return jsonify({"error": "Menu not found"}), 404

@app.route("/menus", methods=["GET"])
def get_menus():
    # Fetch all menus from the Couchbase bucket
    query = "SELECT id, name, meals FROM `{}` WHERE META().id LIKE 'menu::%' AND status=\"Committed\" ORDER BY generation_date".format(COUCHBASE_BUCKET)
    result = cluster.query(query)
    menus = [row for row in result]
    
    # Return the menus as an array of JSON documents in the response
    return jsonify(menus)

def generate_meal(data):
    chosen_meals_ids = data.get("default_meal_ids", [])
    num_meals_to_generate = data.get("num_meals", 5)

    # Fetch all available meal IDs using an N1QL query
    query_str = "SELECT RAW id FROM `{}` WHERE META().id LIKE 'meal::%'".format(COUCHBASE_BUCKET)
    meal_ids = [row for row in cluster.query(query_str)]

    # Calculate scores for all meals based on date and preparation count
    meals_scores = calculate_meals_scores(meal_ids)

    # Select meals based on the score (higher score means higher probability of selection)
    selected_meals_ids = select_meals(meals_scores, num_meals_to_generate,chosen_meals_ids)

    # Fetch the meal documents using the selected meal IDs
    menu_meals = []
    for meal_id in selected_meals_ids:
        meal_key = COUCHBASE_MEAL_PREFIX + meal_id
        meal = collection.get(meal_key).value
        if meal:
            menu_meals.append(meal)
    return menu_meals

def generate_menu_name():
    # List of positive adjectives
    positive_adjectives = ["Delicious", "Tasty", "Mouthwatering", "Scrumptious", "Savory", "Appetizing", "Flavorful"]

    # Fetch synonyms of the word "meal"
    menu_synonyms =  [
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
    random_menu_name = " ".join(random.sample(possible_components, 2))
    return random_menu_name


@app.route("/menu/", methods=["POST"])
def create_menu():
    data = request.get_json()
    menu_meals = generate_meal(data)
    # Generate a new unique ID for the menu
    menu_unique_id = generate_random_id()
    menu_data = {"id": menu_unique_id, "meals": menu_meals, "name": generate_menu_name(), "status": "Pending"}
    # Insert the new menu document into Couchbase
    menu_key = COUCHBASE_MENU_PREFIX + menu_unique_id
    collection.upsert(menu_key, menu_data)
    return jsonify(menu_data), 201
    
@app.route("/menu/<menu_id>", methods=["PATCH"])
def update_menu(menu_id):
    data = request.get_json()
    menu_meals = generate_meal(data)
    menu_data = {"id": menu_id, "meals": menu_meals}
    # Insert the new menu document into Couchbase
    menu_key = COUCHBASE_MENU_PREFIX + menu_id
    collection.upsert(menu_key, menu_data)
    return jsonify(menu_data), 201

def calculate_meals_scores(meal_ids):
    meals_scores = {}
    for meal_id in meal_ids:
        meal_key = COUCHBASE_MEAL_PREFIX + meal_id
        meal = collection.get(meal_key).value
        if meal:
            preparation_count = meal.get("preparation_count", 0)
            generation_date = meal.get("generation_date", datetime.now().timestamp())
            # Calculate the score based on the last committed date and preparation count
            score = calculate_score(generation_date, preparation_count)
            meals_scores[meal_id] = score
    return meals_scores

def calculate_score(generation_date, preparation_count):
    MAX_PREPARATION_COUNT = 10
    # Calculate the date factor (tends to 0 when last commit date tends to now)
    date_factor = 1 - (datetime.now().timestamp() - generation_date)
    # Calculate the preparation count factor (tends to 1 when preparation count tends to 0)
    preparation_count_factor = 1 - (preparation_count / MAX_PREPARATION_COUNT)
    # Calculate the score based on a weighted sum of date and preparation count factors
    date_weight = 0.7
    preparation_count_weight = 0.3
    score = (date_weight * date_factor) + (preparation_count_weight * preparation_count_factor)
    # Normalize the score to be between 0 and 1
    score = min(max(score, 0), 1)
    return score

def select_meals(meals_scores, num_meals_to_generate, default_meals):
    # Select meals randomly based on their scores (higher score means higher probability of selection)
    selected_meals_ids = default_meals
    while len(selected_meals_ids) < num_meals_to_generate and len(meals_scores) > 0:
        total_score = sum(meals_scores.values())
        # Normalize the scores to be probabilities
        probabilities = {meal_id: score / total_score for meal_id, score in meals_scores.items()}
        # Choose a meal ID based on the probabilities
        meal_id = random.choices(list(meals_scores.keys()), weights=list(probabilities.values()))[0]
        selected_meals_ids.append(meal_id)
        # Remove the selected meal from the scores dictionary to avoid selecting it again
        meals_scores.pop(meal_id)
    return selected_meals_ids

@app.route("/commit/<menu_id>", methods=["POST"])
def commit_menu(menu_id):
# @app.route("/commit/", methods=["POST"])
# def commit_menu():
    menu_key = COUCHBASE_MENU_PREFIX + menu_id
    menu = collection.get(menu_key).value
    if menu:
        # Fetch the corresponding meals for each meal ID and update the preparation_count
        for meal_id in menu["meals"]:
            meal_key = COUCHBASE_MEAL_PREFIX + meal_id["id"]
            meal = collection.get(meal_key).value
            if meal:
                meal["preparation_count"] = meal.get("preparation_count", 0) + 1
                meal["last_commit_date"] = datetime.now().isoformat()
                collection.upsert(meal_key, meal)
            menu["status"] = "Committed"
        # Insert the new menu document into Couchbase
        collection.upsert(menu_key, menu)
        return jsonify(menu),201
    return jsonify({"error": "Menu not found"}), 404

@app.route("/meal/<meal_id>", methods=["DELETE"])
def delete_meal(meal_id):
    meal_key = COUCHBASE_MEAL_PREFIX + meal_id
    try:
        collection.remove(meal_key)
        return jsonify({"message": "Meal deleted successfully"}), 200
    except Exception as e:
        print(f"Failed to delete meal: {str(e)}")
        return jsonify({"error": "Failed to delete meal"}), 500

if __name__ == "__main__":
    app.run(debug=True)