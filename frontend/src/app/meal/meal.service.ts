import { Injectable } from '@angular/core';
import { Meal } from './meal.model'
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, switchMap } from 'rxjs/operators';


@Injectable({
    providedIn: 'root'
})
export class MealService {
    private baseUrl = 'http://127.0.0.1:5000'; // Replace with your Flask backend URL

    constructor(private http: HttpClient) { }


    getMeals(): Observable<Meal[]> {
        const headers = new HttpHeaders({
            'Content-Type': 'application/json',
        });
        return this.http.get<Meal[]>(`${this.baseUrl}/meals`, { headers }).pipe(
            catchError((error) => {
                // Handle any errors from the GET request
                return throwError(error);
            })
        );
    }



    getMealById(mealId: string): Observable<Meal> {
        const headers = new HttpHeaders({
            'Content-Type': 'application/json',
        });
        return this.http.get<Meal>(`${this.baseUrl}/meal/${mealId}`, { headers }).pipe(
            catchError((error) => {
                // Handle any errors from the GET request
                return throwError(error);
            })
        );
    }

    createMeal(data: Meal): Observable<any> {
        const headers = new HttpHeaders({
            'Content-Type': 'application/json',
        });
        // Send an HTTP OPTIONS request first (preflight)
        return this.http.options(`${this.baseUrl}/meal/`, { headers }).pipe(
            switchMap(() => {
                // If preflight request succeeds, send the actual POST request
                return this.http.post(`${this.baseUrl}/meal/`, data, { headers }).pipe(
                    catchError((error) => {
                        // Handle any errors from the POST request
                        return throwError(error);
                    })
                );
            }),
            catchError((error) => {
                // Handle any errors from the preflight request
                return throwError(error);
            })
        );
    }

    updateMeal(data: Meal): Observable<any> {
        const headers = new HttpHeaders({
            'Content-Type': 'application/json',
        });
        // Send an HTTP OPTIONS request first (preflight)
        return this.http.options(`${this.baseUrl}/meal/`, { headers }).pipe(
            switchMap(() => {
                // If preflight request succeeds, send the actual POST request
                return this.http.patch(`${this.baseUrl}/meal/${data.id}`, data, { headers }).pipe(
                    catchError((error) => {
                        // Handle any errors from the POST request
                        return throwError(error);
                    })
                );
            }),
            catchError((error) => {
                // Handle any errors from the preflight request
                return throwError(error);
            })
        );
    }

    removeMeal(mealId: string): Observable<any> {
        const headers = new HttpHeaders({
            'Content-Type': 'application/json',
        });
        // Send an HTTP OPTIONS request first (preflight)
        return this.http.options(`${this.baseUrl}/meal/`, { headers }).pipe(
            switchMap(() => {
                // If preflight request succeeds, send the actual POST request
                return this.http.delete(`${this.baseUrl}/meal/${mealId}`, { headers }).pipe(
                    catchError((error) => {
                        // Handle any errors from the POST request
                        return throwError(error);
                    })
                );
            }),
            catchError((error) => {
                // Handle any errors from the preflight request
                return throwError(error);
            })
        );
    }

    // Add other API calls for updating and deleting meals if needed
}
