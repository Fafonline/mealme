from flask import Flask, request, jsonify
from couchbase.auth import PasswordAuthenticator
from couchbase.cluster import Cluster
from couchbase.options import (ClusterOptions, ClusterTimeoutOptions,
                               QueryOptions)
import secrets
import uuid
from couchbase.n1ql import N1QLQuery
import time

app = Flask(__name__)

def add_cors_headers(response):
    # Replace "http://localhost:80" with the actual URL of your Angular application
    # response.headers['Access-Control-Allow-Origin'] = 'http://localhost'
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
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
    query = "SELECT id, name, description FROM `{}` WHERE META().id LIKE 'meal::%'".format(COUCHBASE_BUCKET)
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


@app.route("/menu/", methods=["POST"])
def create_menu():
    data = request.get_json()
    chosen_meals_ids = data.get("default_meal_ids", [])
    num_meals_to_generate = data.get("num_meals", 5)

    # Fetch all available meal IDs using an N1QL query
    query_str = "SELECT RAW id FROM `{}` WHERE META().id LIKE 'meal::%'".format(COUCHBASE_BUCKET)
    meal_ids = [row for row in cluster.query(query_str)]

    # Pick a random meal ID and add it to chosen_meals_ids if not already present
    while len(chosen_meals_ids) < num_meals_to_generate:
        random_meal_id = secrets.choice(meal_ids)
        if random_meal_id not in chosen_meals_ids:
            chosen_meals_ids.append(random_meal_id)

    # Fetch the meal documents using the chosen meal IDs
    menu_meals = []
    for meal_id in chosen_meals_ids:
        meal_key = COUCHBASE_MEAL_PREFIX + meal_id
        meal = collection.get(meal_key).value
        if meal:
            menu_meals.append(meal)

    # Generate a new unique ID for the menu
    menu_unique_id = generate_random_id()
    menu_data = {"id": menu_unique_id, "meals": menu_meals}

    # Insert the new menu document into Couchbase
    menu_key = COUCHBASE_MENU_PREFIX + menu_unique_id
    collection.upsert(menu_key, menu_data)
    return jsonify(menu_data), 201


@app.route("/menu/<menu_id>", methods=["PATCH"])
def update_menu(menu_id):
    data = request.get_json()
    menu_key = COUCHBASE_MENU_PREFIX + menu_id
    current_menu = collection.get(menu_key).value
    if not current_menu:
        return jsonify({"error": "Menu not found"}), 404

    # Update the current menu document with the new data
    current_menu.update(data)
    collection.replace(menu_key, current_menu)
    return jsonify(current_menu)

if __name__ == "__main__":
    app.run(debug=True)