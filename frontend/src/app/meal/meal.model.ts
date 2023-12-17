// meal.model.ts

export class Meal {
    id: string;
    name: string;
    description: string;
    nutriscore: string;

    constructor(id: string, name: string, description: string, nutriscore: string) {
        this.id = id;
        this.name = name;
        this.description = description;
        this.nutriscore = nutriscore;
    }
}
