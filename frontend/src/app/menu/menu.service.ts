import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, switchMap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root',
})
export class MenuService {
  private baseUrl = 'http://127.0.0.1:5000'; // Replace with your Flask backend URL

  constructor(private http: HttpClient) { }

  createMenu(data: any): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
    });

    // Send an HTTP OPTIONS request first (preflight)
    return this.http.options(`${this.baseUrl}/menu/`, { headers }).pipe(
      switchMap(() => {
        // If preflight request succeeds, send the actual POST request
        return this.http.post(`${this.baseUrl}/menu/`, data, { headers }).pipe(
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

  updateMenu(mealId: string, data: any): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
    });

    // Send an HTTP OPTIONS request first (preflight)
    return this.http.options(`${this.baseUrl}/menu/`, { headers }).pipe(
      switchMap(() => {
        // If preflight request succeeds, send the actual PATCH request
        return this.http.patch(`${this.baseUrl}/menu/${mealId}`, data, { headers }).pipe(
          catchError((error) => {
            // Handle any errors from the PATCH request
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

  commitMenu(menuId: string): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
    });

    // Send an HTTP OPTIONS request first (preflight)
    return this.http.options(`${this.baseUrl}/commit/${menuId}`, { headers }).pipe(
      switchMap(() => {
        // If preflight request succeeds, send the actual POST request
        return this.http.post(`${this.baseUrl}/commit/${menuId}`, {}, { headers }).pipe(
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

  getAllMenus(): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
    });

    // Send a GET request to fetch all menus
    return this.http.get(`${this.baseUrl}/menus`, { headers }).pipe(
      catchError((error) => {
        // Handle any errors from the GET request
        return throwError(error);
      })
    );
  }
}
