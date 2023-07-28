import { Injectable } from '@angular/core';
import axios from 'axios';

@Injectable({
    providedIn: 'root'
})
export class MealService {
    private baseUrl = 'http://backend:5000'; // Replace with your Flask backend URL

    getMeals() {
        return axios.get(`${this.baseUrl}/meals/`);
    }

    getMealById(mealId: string) {
        return axios.get(`${this.baseUrl}/meal/${mealId}`);
    }

    createMeal(data: any) {
        return axios.post(`${this.baseUrl}/meal/`, data);
    }

    // Add other API calls for updating and deleting meals if needed
}
