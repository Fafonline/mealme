import { Component, OnInit } from '@angular/core';
import { MealService } from './meal.service';

@Component({
    selector: 'app-meals',
    templateUrl: './meals.component.html'
})
export class MealsComponent implements OnInit {
    meals: any[] = [];

    constructor(private mealService: MealService) { }

    ngOnInit() {
        this.getMeals();
    }

    getMeals() {
        this.mealService.getMeals().then((response) => {
            this.meals = response.data;
        });
    }
}
