// meal.model.ts

export class Menu {
    id: string;
    name: string;
    meals: Menu[];
    show: boolean;
    generation_date: string;

    constructor(id: string, name: string, meals: Menu[]) {
        this.id = id;
        this.name = name;
        this.meals = meals;
        this.show = false;
        this.generation_date = "";
    }
}
