import { Component, OnInit } from '@angular/core';
import { MenuService } from './menu.service';
import { SharedService } from '../shared/shared.service';
import { Subscription } from 'rxjs';
import { Meal } from '../meal/meal.model'
import { Menu } from './menu.model'


@Component({
    selector: 'app-menu',
    templateUrl: './menu.component.html',
    styleUrls: ['./menu.component.css']
})
export class MenuComponent implements OnInit {
    menuMeals: Meal[] = [];
    menuId: undefined;
    generateButtonLabel = "Hungry? Click here to get your meal!";
    numMeals: number = 5; // Default value for the number of meals to generate
    mealSelection: { [key: string]: boolean } = {};
    private mealSelectionSubscription!: Subscription;
    private menuMealsSubscription!: Subscription;
    selectedDuration: string = 'week'; // Default selected duration


    constructor(private menuService: MenuService, private sharedService: SharedService) { }

    ngOnInit() {
        this.mealSelectionSubscription = this.sharedService.mealSelection$.subscribe(
            (selection) => {
                console.log("!!!Menu callback:", selection);
                console.log("!!!Menu meals selection:", this.mealSelection);
                this.mealSelection = selection;
            }
        );
        this.menuMealsSubscription = this.sharedService.menuMeals$.subscribe(
            (menuMeals) => {
                this.menuMeals = menuMeals;
            }
        );
    }
    computeNumberOfMeals(): number {
        switch (this.selectedDuration) {
            case 'weekend':
                return 2; // 2 meals for weekend
            case 'week':
                return 7; // 1 meal per working day
            case 'twoWeeks':
                return 14; // 2 weeks * 5 working days
            case 'month':
                return 28; // 4 weeks * 5 working days
            default:
                return 0;
        }
    }
    ngOnDestroy() {
        this.mealSelectionSubscription.unsubscribe();
        this.menuMealsSubscription.unsubscribe();
    }

    getSelectedMeals(): string[] {
        // Use Object.keys() to get an array of keys from the mealSelections object
        // Use Array.filter() to filter only the keys with true value
        return Object.keys(this.mealSelection).filter((key) => this.mealSelection[key]);
    }
    updateMenuModel(response: any) {
        console.log("Update Menu model")
        // Extract the meals array from the API response
        const mealsArray = response?.meals;
        // Update the menuMeals array with the meal names
        this.menuMeals = mealsArray?.map((meal: any) => ({
            id: meal.id,
            name: meal.name,
            description: meal.description,
        }));
        this.menuId = response.id;
        if (this.menuId !== undefined) {
            this.generateButtonLabel = "Yummy? Try again!"
        }
        this.sharedService.setMenuMeals(this.menuMeals)
    }
    // Method to handle the button click event
    createNewMenu() {
        const numMeals = this.computeNumberOfMeals();
        const menuData = {
            num_meals: numMeals, // Example number of meals to generate,
            "default_meal_ids": this.sharedService.getSelectedMeals()
        };
        console.log("Menu Data:", menuData);
        if (this.menuId === undefined) {
            // Call the createMenu method from the MenuService
            this.menuService.createMenu(menuData).subscribe(
                (response: any) => {
                    console.log('Menu created successfully:', response);
                    this.updateMenuModel(response);
                },
                (error: any) => {
                    console.error('Error creating menu:', error);
                    // Handle error, if needed (e.g., show an error message)
                }
            );
        }
        else {
            this.menuService.updateMenu(this.menuId, menuData).subscribe(
                (response) => {
                    console.log('Menu Updated successfully:', response);
                    this.updateMenuModel(response);
                },
                (error) => {
                    console.error('Error Updating menu:', error);
                    // Handle error, if needed (e.g., show an error message)
                }
            );
        }
    }
    commitMenu() {
        // Get the IDs of the meals in the generated menu that are selected
        const selectedMealsIds = this.menuMeals
            .map((meal) => meal.id);

        console.log("Commit menu ", this.menuId);
        // Call the commit_menu service with the selected meal IDs
        this.menuService.commitMenu(String(this.menuId)).subscribe(
            (response) => {
                console.log('Menu committed successfully:', response);
                // Handle success, if needed (e.g., show a success message)
                this.menuMeals = [];
                this.generateButtonLabel = "Hungry? Click here to get your meal!"
                this.menuId = undefined
                this.sharedService.sendEvent("UpdateMenuList")
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
