import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { Meal } from "./meal.model"
@Injectable({
    providedIn: 'root',
})
export class SharedService {
    private mealSelectionSubject = new BehaviorSubject<{ [key: string]: boolean }>({});
    mealSelection$: Observable<{ [key: string]: boolean }> = this.mealSelectionSubject.asObservable();

    private showEditModelSubject = new BehaviorSubject<boolean>(false);
    showEditModel$: Observable<boolean> = this.showEditModelSubject.asObservable();

    private mealToEditSubject = new BehaviorSubject<Meal>(new Meal('', '', ''));
    mealToEdit$: Observable<Meal> = this.mealToEditSubject.asObservable();

    getMealSelection(): { [key: string]: boolean } {
        return this.mealSelectionSubject.getValue();
    }

    getSelectedMeals(): string[] {
        return Object.keys(this.mealSelectionSubject.getValue()).filter((key) => this.mealSelectionSubject.getValue()[key]);
    }

    toggleMealSelection(meal: any): void {
        const currentSelection = this.getMealSelection();
        const updatedSelection = { ...currentSelection, [meal.id]: currentSelection[meal.id] };
        this.mealSelectionSubject.next(updatedSelection);
        console.log("Value after shared service toggle:", this.getMealSelection())
    }
    showMealEditPopup(meal: Meal) {
        console.log("Update showEditModelSubject")
        this.showEditModelSubject.next(true);
        this.mealToEditSubject.next(meal);
    }
}
