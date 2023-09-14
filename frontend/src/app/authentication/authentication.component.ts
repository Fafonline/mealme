import { Component, OnInit } from '@angular/core';
import { AuthenticationService } from '../shared/authentication.service'
import { SharedService } from '../shared/shared.service'
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-authentication',
  templateUrl: './authentication.component.html',
  styleUrls: ['./authentication.component.css']
})
export class AuthenticationComponent implements OnInit {

  private isLoggedInSubscription!: Subscription;
  isLoggedIn: boolean = false;

  constructor(private authenticationService: AuthenticationService, private sharedService: SharedService) { }

  ngOnInit() {
    this.isLoggedInSubscription = this.authenticationService.loginStatus$.subscribe(
      (isLoggedIn) => {
        console.log("!!! Is Logged-In:", isLoggedIn);
        this.isLoggedIn = isLoggedIn;
      }
    );
  }
}
