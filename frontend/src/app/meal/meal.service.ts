import { Injectable } from '@angular/core';
import axios from 'axios';
import { Meal } from './meal.model'

@Injectable({
    providedIn: 'root'
})
export class MealService {
    private baseUrl = 'http://127.0.0.1:5000'; // Replace with your Flask backend URL

    getMeals() {
        let response = axios.get(`${this.baseUrl}/meals`);
        console.log(response);
        return response;
    }

    getMealById(mealId: string) {
        return axios.get(`${this.baseUrl}/meal/${mealId}`);
    }

    createMeal(data: Meal) {
        return axios.post(`${this.baseUrl}/meal/`, data);
    }

    updateMeal(data: Meal) {
        return axios.patch(`${this.baseUrl}/meal/${data.id}`, data);
    }
    removeMeal(mealId: string) {
        return axios.delete(`${this.baseUrl}/meal/${mealId}`);
    }
    // Add other API calls for updating and deleting meals if needed
}
