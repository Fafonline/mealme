import { Component, OnInit } from '@angular/core';
import { Subscription } from 'rxjs';
import { AuthenticationService } from '../shared/authentication.service'
import { SharedService } from '../shared/shared.service'
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

  constructor(private authenticationService: AuthenticationService, private sharedService: SharedService, private router: Router) { }


  ngOnInit() {
    this.eventSubscription = this.sharedService.event$.subscribe(
      (event) => {
        if (event === "LoginRequest") {
          console.log("Request Login");
          this.login();
        }
      }
    );
  }

  login() {
    // Perform your authentication logic here
    if (this.username === 'guest' && this.password === 'password') {
      this.authenticationService.setStatus(true);
      alert('Login successful!');
      // Redirect to the dashboard or another page upon successful login
      // Use Angular Router for navigation
      this.router.navigate(['/']);
    } else {
      alert('Login failed. Please check your credentials.');
    }
  }
}
