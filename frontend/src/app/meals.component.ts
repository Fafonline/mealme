import { Component, OnInit } from '@angular/core';
import { MealService } from './meal.service';

@Component({
    selector: 'app-meals',
    templateUrl: './meals.component.html'
})
export class MealsComponent implements OnInit {
    meals: any[] = [];
    markdownInput: string = '';


    constructor(private mealService: MealService) { }

    ngOnInit() {
        this.getMeals();
    }

    getMeals() {
        this.mealService.getMeals().then((response) => {
            this.meals = response.data;
        });
    }

    createMeals() {
        const mealNames = this.parseMarkdownInput();
        const mealsToCreate = mealNames.map((name) => {
            return { name: name.trim() };
        });
        // Call the createMeal method from the MenuService for each meal
        mealsToCreate.forEach((meal) => {
            this.mealService.createMeal(meal).then(
                (response) => {
                    console.log('Meals Imported successfully:', response);
                    // Handle success, if needed (e.g., show a success message)
                },
                (error) => {
                    console.error('Error creating meal:', error);
                    // Handle error, if needed (e.g., show an error message)
                }
            );
        });
    }
    private parseMarkdownInput(): string[] {
        // Split the markdown input into lines
        const lines = this.markdownInput.split('\n');

        // Extract meal names from each line (assuming they start with a hyphen and space)
        const mealNames = lines.map((line) => {
            const match = line.match(/^\s*- (.+)/);
            return match ? match[1] : '';
        });

        // Filter out any empty or whitespace-only names
        return mealNames.filter((name) => name.trim() !== '');
    }
}
