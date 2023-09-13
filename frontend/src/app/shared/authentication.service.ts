import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
@Injectable({
  providedIn: 'root'
})
export class AuthenticationService {
  private loginStatusSubject = new BehaviorSubject<boolean>(false);
  loginStatus$: Observable<boolean> = this.loginStatusSubject.asObservable();

  setStatus(isLoggedIn: boolean) {
    this.loginStatusSubject.next(isLoggedIn)

  }
}
