import { Component, OnInit } from '@angular/core';
import { MealService } from './meal.service';
import { Subscription } from 'rxjs';
import { SharedService } from '../shared/shared.service';
import { Meal } from './meal.model'
import { FormsModule } from '@angular/forms';
import { AuthenticationService } from '../shared/authentication.service'



@Component({
    selector: 'app-meals',
    templateUrl: './meals.component.html'
})

export class MealsComponent implements OnInit {
    isLoggedIn: boolean = false
    meals: Meal[] = [];
    markdownInput: string = '';
    mealSelection: { [key: string]: boolean } = {};
    private mealSelectionSubscription!: Subscription;
    private isLoggedInSubscription!: Subscription;
    constructor(private mealService: MealService, private sharedService: SharedService, private authenticationService: AuthenticationService) { }
    selectedMeal: Meal = { "id": "", "description": "", "name": "" };
    searchTerm: string = '';
    filteredMeals: Meal[] = [];

    ngOnInit() {
        this.getMeals();
        this.filteredMeals = this.meals; // Initialize filteredMeals with all meals
        this.mealSelectionSubscription = this.sharedService.mealSelection$.subscribe(
            (selection) => {
                console.log("!!!Meals callback:", selection);
                console.log("!!!Meals meals selection:", this.mealSelection);
                this.mealSelection = selection;
            }
        );

        this.isLoggedInSubscription = this.authenticationService.loginStatus$.subscribe(
            (isLoggedIn) => {
                this.isLoggedIn = isLoggedIn;
            }
        );
        console.log("Meals:", this.meals)
        console.log("Filtered meals:", this.filteredMeals)
    }
    // Add a method to update filteredMeals based on searchTerm

    updateFilteredMeals() {
        // Split the search term into words
        const searchWords = this.searchTerm.toLowerCase().split(' ');

        // Filter meals based on search words
        this.filteredMeals = this.meals.filter((meal) => {
            // Check if any of the search words is found in the meal name
            return searchWords.some((word) =>
                meal.name.toLowerCase().includes(word)
            );
        });
    }
    getMeals() {
        this.mealService.getMeals().subscribe((response: any) => {
            this.meals = response;
            console.log("Get meals:", this.meals)
            this.updateFilteredMeals();
            console.log("Filtered meals:", this.filteredMeals)
        });
    }

    createMeals() {
        const mealNames = this.parseMarkdownInput();
        const mealsToCreate = mealNames.map((name) => {
            return new Meal('', name.trim(), ''); // Create a new Meal instance with the provided name
        });
        // Call the createMeal method from the MenuService for each meal
        mealsToCreate.forEach((meal) => {
            this.mealService.createMeal(meal).subscribe(
                (response) => {
                    console.log('Meals Imported successfully:', response);
                    // Refresh the meals list
                    this.getMeals();
                    this.updateFilteredMeals();
                    this.markdownInput = "Enter meals in markdown format"
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

    removeMeal(mealId: string) {
        this.mealService.removeMeal(mealId).subscribe((response) => {
            console.log("Removed with success:", mealId)
            this.getMeals();
        });
    }
}
