import { Injectable } from '@angular/core';
import axios from 'axios';
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
      'Content-Type': 'application/json'
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

  updateMenu(mealId: string, data: any) {
    const headers = {
      'Content-Type': 'application/json'
    };
    return axios.options(`${this.baseUrl}/menu/`, { headers })
      .then((response: { data: any; }) => {
        // Pre-flight request succeeded, send the actual POST request with the data
        return axios.patch(`${this.baseUrl}/menu/${mealId}`, data, { headers });
      })
      .then((response: { data: any; }) => {
        // Actual POST request succeeded, return the response data
        return response.data;
      })
      .catch((error: { data: any; }) => {
        // Handle any errors
        throw error;
      });
  }
  commitMenu(menuId: string) {
    const headers = {
      'Content-Type': 'application/json'
    };
    return axios.options(`${this.baseUrl}/commit/${menuId}`, { headers })
      .then((response: { data: any; }) => {
        // Pre-flight request succeeded, send the actual POST request with the data
        return axios.post(`${this.baseUrl}/commit/${menuId}`, {}, { headers });
      })
      .then((response: { data: any; }) => {
        // Actual POST request succeeded, return the response data
        return response.data;
      })
      .catch((error: { data: any; }) => {
        // Handle any errors
        throw error;
      });
  }
  // commitMenu(menuId: string, data: any) {
  //   const headers = {
  //     'Content-Type': 'application/json'
  //   };
  //   return axios.options(`${this.baseUrl}/commit/`, { headers })
  //     .then((response: { data: any; }) => {
  //       // Pre-flight request succeeded, send the actual POST request with the data
  //       return axios.post(`${this.baseUrl}/commit/${menuId}`, data, { headers });
  //     })
  //     .then((response: { data: any; }) => {
  //       // Actual POST request succeeded, return the response data
  //       return response.data;
  //     })
  //     .catch((error: { data: any; }) => {
  //       // Handle any errors
  //       throw error;
  //     });

  // }
  getAllMenus() {
    const headers = {
      'Content-Type': 'application/json'
    };

    return axios.get(`${this.baseUrl}/menus`, { headers })
      .then((response) => {
        // Request succeeded, return the response data
        return response.data;
      })
      .catch((error) => {
        // Handle any errors
        throw error;
      });
  }
}
