
import logging
from datetime import datetime
import random
from lib import utils

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class MealSelector:
    def __init__(self,db_mgr):
        self.db_mgr = db_mgr

    def calculate_meals_scores(self, meal_ids):
        meals_scores = {}
        for meal_id in meal_ids:
            # Fetch the meal document from RethinkDB
            meal = self.db_mgr.get_meal(meal_id)
            if meal:
                preparation_count = meal.get("preparation_count", 0)
                generation_date = meal.get(
                    "generation_date", datetime.now())
                # Calculate the score based on the last committed date and preparation count
                score = self.calculate_score(generation_date, preparation_count)
                meals_scores[meal_id] = score
        return meals_scores


    def calculate_score(self, generation_date, preparation_count):
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


    def select_meals(self, meals_scores, num_meals_to_generate, default_meals):
        tracked_ingredients = ["Riz", "Pâte", "Pommes de terre", "Haricot rouges", "Lentilles","Frites","Poulet","Coco"]
        selected_meals_ingredient = []
        selected_meals_ids = default_meals
    
        while len(selected_meals_ids) < num_meals_to_generate and len(meals_scores) > 0:
            total_score = sum(meals_scores.values())
    
            # Normalize the scores to be probabilities
            probabilities = {meal_id: score / total_score for meal_id, score in meals_scores.items()}
    
            # Choose a meal ID based on the probabilities
            meal_id = random.choices(list(meals_scores.keys()), weights=list(probabilities.values()))[0]
    
            if meal_id in selected_meals_ids:
                continue
            
            # Fetch the meal by ID
            selected_meal = self.db_mgr.get_meal(meal_id)
            logger.info("Check selected meal:")
            logger.info(selected_meal["name"])
            # Check if any ingredient in the meal is in the tracked_ingredients list
            meal_ingredients = selected_meal.get("ingredients",[])
            logger.info("Ingredient:")
            logger.info(meal_ingredients)
            found_tracked_ingredient = utils.find_elements_in_array(meal_ingredients, tracked_ingredients)
            logger.info("Found tracked Ingredient:")
            logger.info(found_tracked_ingredient)
            is_rejected = False

            if found_tracked_ingredient:
                # Check the condition to determine whether to reject the meal or not
                is_rejected = reject_tracked_ingredient(found_tracked_ingredient,selected_meals_ingredient)
            if not is_rejected:
                # Add the meal ID to the selected meals if the condition is met
                selected_meals_ids.append(meal_id)
                selected_meals_ingredient = utils.append_without_duplicates(selected_meals_ingredient,found_tracked_ingredient)

            # Remove the selected meal from the scores dictionary to avoid selecting it again
            meals_scores.pop(meal_id)
            logger.info("Selected meals ingredients:")
            logger.info(selected_meals_ingredient)
    
        return selected_meals_ids



    def generate_meals(self,data):
        chosen_meals_ids = data.get("default_meal_ids", [])
        num_meals_to_generate = data.get("num_meals", 5)

        # Fetch all available meal IDs
        cursor = self.db_mgr.get_meals_ids()
        meal_ids = list(cursor)
        meal_ids = [meal['id'] for meal in meal_ids]

        # Calculate scores for all meals based on date and preparation count
        meals_scores = self.calculate_meals_scores(meal_ids)

        # Select meals based on the score (higher score means higher probability of selection)
        selected_meals_ids = self.select_meals(
            meals_scores, num_meals_to_generate, chosen_meals_ids)

        # Fetch the meal documents using the selected meal IDs
        menu_meals = []
        for meal_id in selected_meals_ids:
            meal = self.db_mgr.get_meal(meal_id)
            if meal:
                menu_meals.append(meal)
        return menu_meals

def reject_tracked_ingredient(tracked_ingredient, selected_meals_ingredients):
    found_elements = utils.find_elements_in_array(tracked_ingredient, selected_meals_ingredients)
    if(found_elements):
        return True
    else:
        return False