from openai import OpenAI
import json
import os
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class MealDecorator:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
        )
        self.response_format = {
            "ingredients":["Ingredient 1","Ingredient 2"],
            "nutriscore":"A"
        }
        self.prompt = """D'apres ce repas:\nName: {}\nDescription: {}\n, 
                            Deduire la composition et la retourner uniquement sous forme de tableau de string Json
                            Donner une estimation du score nutriscore. 
                            au format {}.
                            PAS D'AUTRE TEXTE. 
                            Toujours en francais. 
                            Pas de \' pour les champs JSON mais unique des \".
                            """

    def get_ingredients(self,meal_data):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",  # You can choose another model based on your preferences
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": self.prompt.format(meal_data["name"],meal_data.get("description","Aucune"),self.response_format)}
            ]
        )

        # # Extract the generated ingredient from the response
        generated_ingredient = response.choices[0].message.content
        # Parse the generated ingredient as JSON
        try:
            ingredient_json = json.loads(generated_ingredient)
            logger.info(ingredient_json)
            meal_data.update(ingredient_json)
        except json.JSONDecodeError:
            logger.error("Failed to parse the generated ingredient as JSON.")
        
        return meal_data