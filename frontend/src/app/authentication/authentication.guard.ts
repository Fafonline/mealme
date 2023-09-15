import { Injectable } from '@angular/core';
import { CanActivate, Router } from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class AuthGuard implements CanActivate {
  constructor(private router: Router) { }

  canActivate(): boolean {
    // Check if the user is logged in (JWT is in local storage)
    if (localStorage.getItem('access_token')) {
      return true; // Allow access to the route
    } else {
      // Redirect to the login page if not logged in
      this.router.navigate(['/login']);
      return false; // Prevent access to the route
    }
  }
}