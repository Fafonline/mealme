// meal.model.ts

export class Menu {
    id: string;
    name: string;
    meals: string[];

    constructor(id: string, name: string, meals: string[]) {
        this.id = id;
        this.name = name;
        this.meals = meals;
    }
}
