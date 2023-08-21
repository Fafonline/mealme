// meal.model.ts

export class Menu {
    id: string;
    name: string;
    meals: Menu[];
    show: boolean;

    constructor(id: string, name: string, meals: Menu[]) {
        this.id = id;
        this.name = name;
        this.meals = meals;
        this.show = false;
    }
}
