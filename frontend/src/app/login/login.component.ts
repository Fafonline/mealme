import { Component, OnInit } from '@angular/core';
import { Subscription } from 'rxjs';
import { AuthenticationService } from '../shared/authentication.service'
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'],
})
export class LoginComponent implements OnInit {
  username: string = '';
  password: string = '';

  private eventSubscription!: Subscription;
  isLoggedIn: boolean = false;
  loginFailed: boolean = false;

  constructor(private authenticationService: AuthenticationService, private router: Router) { }

  ngOnInit(): void {
    let accessToken = localStorage.getItem('access_token');
    if (accessToken !== null) {
      console.log("access token present:", accessToken)
      this.authenticationService.setStatus(true);
    }
  }

  login(username: string, password: string): void {
    this.authenticationService.login({ username, password }).subscribe(
      (response) => {
        // Successful login - store the JWT in local storage
        localStorage.setItem('access_token', response.access_token);
        localStorage.setItem('user', username);
        // Redirect to a protected route (e.g., dashboard)
        this.router.navigate(['/']);
        this.authenticationService.setStatus(true);
        this.authenticationService.setUserName(username);
        this.loginFailed = false;
      },
      (error) => {
        // Handle login error
        console.error('Login failed:', error);
        this.loginFailed = true;
        // Show an error message to the user
      }
    );
  }
}
