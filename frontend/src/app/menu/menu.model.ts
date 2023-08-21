// meal.model.ts

export class Menu {
    id: string;
    name: string;
    meals: Menu[];

    constructor(id: string, name: string, meals: Menu[]) {
        this.id = id;
        this.name = name;
        this.meals = meals;
    }
}
