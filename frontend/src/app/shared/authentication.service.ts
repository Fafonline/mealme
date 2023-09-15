import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { BehaviorSubject, Observable, throwError } from 'rxjs';
import { catchError, switchMap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class AuthenticationService {
  private loginStatusSubject = new BehaviorSubject<boolean>(false);
  loginStatus$: Observable<boolean> = this.loginStatusSubject.asObservable();
  private baseUrl = 'http://127.0.0.1:5000'; // Replace with your login API URL

  constructor(private http: HttpClient) { }

  setStatus(isLoggedIn: boolean) {
    this.loginStatusSubject.next(isLoggedIn)
  }


  login(credentials: { username: string, password: string }): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json'
    });

    // Send an HTTP OPTIONS request first (preflight)
    return this.http.options(`${this.baseUrl}/login/`, { headers }).pipe(
      switchMap(() => {
        // If preflight request succeeds, send the actual POST request
        return this.http.post(`${this.baseUrl}/login/`, credentials, { headers }).pipe(
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
}
