import { Component, OnInit } from '@angular/core';
import { AuthenticationService } from '../shared/authentication.service'
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './logout.component.html',
  styleUrls: ['./logout.component.css'],
})
export class LogoutComponent implements OnInit {
  username: string = '';
  password: string = '';

  constructor(private authenticationService: AuthenticationService, private router: Router) { }


  ngOnInit() {
    this.authenticationService.setStatus(false);
    this.router.navigate(['/']);
  }
}
