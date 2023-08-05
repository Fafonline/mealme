import { Component, OnInit } from '@angular/core';
import { MenuService } from './menu.service';
import { SharedService } from './shared.service';

@Component({
    selector: 'app-menu',
    templateUrl: './menu.component.html',
    styleUrls: ['./menu.component.css']
})
export class MenuComponent implements OnInit {
    menuMeals: { id: string; name: string; description: string }[] = [];
    numMeals: number = 5; // Default value for the number of meals to generate
    mealSelections: { [key: string]: boolean } = {};
    constructor(private menuService: MenuService, private sharedService: SharedService) { }

    ngOnInit() {
    }
    getSelectedMeals(): string[] {
        // Use Object.keys() to get an array of keys from the mealSelections object
        // Use Array.filter() to filter only the keys with true value
        return Object.keys(this.mealSelections).filter((key) => this.mealSelections[key]);
    }
    // Method to handle the button click event
    createNewMenu() {
        const menuData = {
            num_meals: this.numMeals, // Example number of meals to generate,
            "default_meal_ids": this.sharedService.getSelectedMeals().map((meal) => meal.id)
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

    isMealSelected(meal: any) {
        const selectedMeals = this.sharedService.getSelectedMeals();
        return (selectedMeals.some((m) => m.id === meal.id));
    }
    toggleMealSelection(meal: any) {
        if (this.isMealSelected(meal)) {
            this.sharedService.removeSelectedMeal(meal);
            this.mealSelections[meal.id] = false;
        } else {
            this.sharedService.addSelectedMeal(meal);
            this.mealSelections[meal.id] = true;
        }
        const selectedMeals = this.sharedService.getSelectedMeals();
        console.log("Item selected from generated menu:", selectedMeals);
    }
}
