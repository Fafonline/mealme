import { Component, OnInit } from '@angular/core';
import { MenuService } from './menu.service';

@Component({
    selector: 'app-menu',
    templateUrl: './menu.component.html',
    styleUrls: ['./menu.component.css']
})
export class MenuComponent implements OnInit {
    menuMeals: { id: string; name: string; description: string }[] = [];
    numMeals: number = 5; // Default value for the number of meals to generate
    selectedMeals: string[] = [];

    constructor(private menuService: MenuService) { }

    ngOnInit() {
    }

    // Method to handle the button click event
    createNewMenu() {
        const menuData = {
            num_meals: this.numMeals, // Example number of meals to generate,
            "default_meal_ids": this.selectedMeals
        };
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
    // Function to handle the click event when a meal is selected or deselected
    onMealSelected(mealId: string) {
        // Check if the mealId is already in the selectedMeals list
        const index = this.selectedMeals.indexOf(mealId);

        // If the mealId is not in the list, add it
        if (index === -1) {
            this.selectedMeals.push(mealId);
        } else {
            // If the mealId is already in the list, remove it
            this.selectedMeals.splice(index, 1);
        }
        console.log("Selected Meals:", this.selectedMeals);
    }
}
