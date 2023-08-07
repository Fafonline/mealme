import { Component, OnInit } from '@angular/core';
import { MenuService } from './menu.service';
import { SharedService } from './shared.service';
import { Subscription } from 'rxjs';
import { Meal } from './meal.model'

@Component({
    selector: 'app-menu',
    templateUrl: './menu.component.html',
    styleUrls: ['./menu.component.css']
})
export class MenuComponent implements OnInit {
    menuMeals: Meal[] = [];
    numMeals: number = 5; // Default value for the number of meals to generate
    mealSelection: { [key: string]: boolean } = {};
    private mealSelectionSubscription!: Subscription;

    constructor(private menuService: MenuService, private sharedService: SharedService) { }

    ngOnInit() {
        this.mealSelectionSubscription = this.sharedService.mealSelection$.subscribe(
            (selection) => {
                console.log("!!!Menu callback:", selection);
                console.log("!!!Menu meals selection:", this.mealSelection);
                this.mealSelection = selection;
            }
        );
    }

    ngOnDestroy() {
        this.mealSelectionSubscription.unsubscribe();
    }

    getSelectedMeals(): string[] {
        // Use Object.keys() to get an array of keys from the mealSelections object
        // Use Array.filter() to filter only the keys with true value
        return Object.keys(this.mealSelection).filter((key) => this.mealSelection[key]);
    }
    // Method to handle the button click event
    createNewMenu() {
        const menuData = {
            num_meals: this.numMeals, // Example number of meals to generate,
            "default_meal_ids": this.sharedService.getSelectedMeals()
        };
        console.log("Menu Data:", menuData);
        // Call the createMenu method from the MenuService
        this.menuService.createMenu(menuData).then(
            (response) => {
                console.log('Menu created successfully:', response);

                // Extract the meals array from the API response
                const mealsArray = response?.meals;
                // Update the menuMeals array with the meal names
                this.menuMeals = mealsArray?.map((meal: any) => ({
                    id: meal.id,
                    name: meal.name,
                    description: meal.description,
                }));
            },
            (error) => {
                console.error('Error creating menu:', error);
                // Handle error, if needed (e.g., show an error message)
            }
        );
    }
    commitMenu() {
        // Get the IDs of the meals in the generated menu that are selected
        const selectedMealsIds = this.menuMeals
            .map((meal) => meal.id);

        console.log("Commit menu wit ids:", selectedMealsIds);

        const data = {
            meal_ids: selectedMealsIds
        };
        // Call the commit_menu service with the selected meal IDs
        this.menuService.commitMenu(data).then(
            (response) => {
                console.log('Menu committed successfully:', response);
                // Handle success, if needed (e.g., show a success message)
                this.menuMeals = [];
            },
            (error) => {
                console.error('Error committing menu:', error);
                // Handle error, if needed (e.g., show an error message)
            }
        );
    }

    toggleMealSelection(meal: any) {
        this.sharedService.toggleMealSelection(meal);
        console.log("Item selected from menu:", this.sharedService.getSelectedMeals());
    }
}
