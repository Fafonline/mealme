import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
    providedIn: 'root',
})
export class SharedService {
    private selectedMealsSubject = new BehaviorSubject<any[]>([]);
    selectedMeals$ = this.selectedMealsSubject.asObservable();

    constructor() { }

    getSelectedMeals() {
        let selectedMeals = this.selectedMealsSubject.getValue();
        return this.selectedMealsSubject.getValue();
    }

    addSelectedMeal(meal: any) {
        const currentMeals = this.selectedMealsSubject.getValue();
        this.selectedMealsSubject.next([...currentMeals, meal]);
    }

    removeSelectedMeal(meal: any) {
        const currentMeals = this.selectedMealsSubject.getValue();
        const updatedMeals = currentMeals.filter((m) => m.id !== meal.id);
        this.selectedMealsSubject.next(updatedMeals);
    }
}
