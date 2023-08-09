import { Component, OnInit } from '@angular/core';
import { MealService } from './meal.service';
import { Subscription } from 'rxjs';
import { SharedService } from './shared.service';
import { Meal } from './meal.model'
import { MealModalComponent } from './meal-modal/meal-modal.component';

@Component({
    selector: 'app-meals',
    templateUrl: './meals.component.html'
})
export class MealsComponent implements OnInit {
    meals: Meal[] = [];
    markdownInput: string = '';
    mealSelection: { [key: string]: boolean } = {};
    private mealSelectionSubscription!: Subscription;
    constructor(private mealService: MealService, private sharedService: SharedService) { }
    selectedMeal: Meal = { "id": "", "description": "", "name": "" };



    ngOnInit() {
        this.getMeals();
        this.mealSelectionSubscription = this.sharedService.mealSelection$.subscribe(
            (selection) => {
                console.log("!!!Meals callback:", selection);
                console.log("!!!Meals meals selection:", this.mealSelection);
                this.mealSelection = selection;
            }
        );
    }

    getMeals() {
        this.mealService.getMeals().then((response) => {
            this.meals = response.data;
        });
    }

    createMeals() {
        const mealNames = this.parseMarkdownInput();
        const mealsToCreate = mealNames.map((name) => {
            return new Meal('', name.trim(), ''); // Create a new Meal instance with the provided name
        });
        // Call the createMeal method from the MenuService for each meal
        mealsToCreate.forEach((meal) => {
            this.mealService.createMeal(meal).then(
                (response) => {
                    console.log('Meals Imported successfully:', response);
                    // Refresh the meals list
                    this.getMeals();
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
    toggleMealSelection(meal: Meal) {
        this.sharedService.toggleMealSelection(meal);
        console.log("Item selected from existing meals:", this.sharedService.getSelectedMeals());

    }

    // Method to open the edit modal
    openEditModal(meal: Meal) {
        console.log("Clicked on meal:", meal);
        this.sharedService.showMealEditPopup(meal);
    }

    // Method to close the edit modal
    closeEditModal() {
        this.selectedMeal = new Meal('', '', '');
    }

    // Method to update the meal data after editing
    updateMeal(updatedMeal: Meal) {
        // Update the meal data in your meals array or make an API call
        // and close the modal
        this.selectedMeal = new Meal('', '', '');
    }
}
