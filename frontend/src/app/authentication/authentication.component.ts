import { Component, OnInit } from '@angular/core';
import { AuthenticationService } from '../shared/authentication.service'
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-authentication',
  templateUrl: './authentication.component.html',
  styleUrls: ['./authentication.component.css']
})
export class AuthenticationComponent implements OnInit {

  private isLoggedInSubscription!: Subscription;
  private userNameSubscription!: Subscription;
  isLoggedIn: boolean = false;
  userName: string = "";

  constructor(private authenticationService: AuthenticationService) { }

  ngOnInit() {
    this.isLoggedInSubscription = this.authenticationService.loginStatus$.subscribe(
      (isLoggedIn) => {
        console.log("!!! Is Logged-In:", isLoggedIn);
        this.isLoggedIn = isLoggedIn;
      }
    );
    this.userNameSubscription = this.authenticationService.username$.subscribe(
      (userName) => {
        console.log("!!! UserName:", userName);
        this.userName = userName;
      }
    );
  }
}
