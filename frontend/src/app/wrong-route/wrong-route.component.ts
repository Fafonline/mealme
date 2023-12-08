import { Component } from '@angular/core';
import { CanActivate, Router } from '@angular/router';

@Component({
  selector: 'app-wrong-route',
  templateUrl: './wrong-route.component.html',
  styleUrls: ['./wrong-route.component.css']
})
export class WrongRouteComponent {
  constructor(private router: Router) {
    console.log("Wrong route. Go to login")
    this.router.navigate(['/login']);
  }
}
