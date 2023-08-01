import { Component, OnInit } from '@angular/core';
import { MenuService } from './menu.service';

@Component({
    selector: 'app-menu',
    templateUrl: './menu.component.html'
})
export class MenuComponent implements OnInit {
    menuMeals: { id: string; name: string; description: string }[] = [{ "id": "LKLKJLKJ", "name": "Couascous", "description": "Delicious" }];

    constructor(private menuService: MenuService) { }

    ngOnInit() {
        this.createNewMenu();
    }

    // Method to handle the button click event
    createNewMenu() {
        // Replace this with the data for the new menu
        const menuData = {
            num_meals: 5, // Example number of meals to generate
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
}
