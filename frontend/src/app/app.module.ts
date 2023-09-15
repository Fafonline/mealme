import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { MealsComponent } from './meal/meals.component';
import { MenuComponent } from './menu/menu.component';
import { FormsModule } from '@angular/forms';
import { MealModalComponent } from './meal-modal/meal-modal.component';
import { MenuListComponent } from './menu-list/menu-list.component';
import { AuthInterceptor } from './shared/auth.interceptor'
import { LoginComponent } from './login/login.component';
import { RouterModule, Routes } from '@angular/router';
import { AuthenticationComponent } from './authentication/authentication.component';
import { LogoutComponent } from './logout/logout.component';
import { HttpClientModule } from '@angular/common/http'; // Import HttpClientModule
import { HTTP_INTERCEPTORS } from '@angular/common/http';
import { AuthGuard } from './authentication/authentication.guard';


const routes: Routes = [
  { path: 'login', component: LoginComponent },
  { path: 'logout', component: LogoutComponent },
  { path: '', component: MenuComponent, canActivate: [AuthGuard] },
  { path: 'select-meals', component: MealsComponent },
  { path: 'See-all-menus', component: MenuListComponent },
  // Add other routes here if needed
];

@NgModule({
  declarations: [
    AppComponent, MealsComponent, MenuComponent, MealModalComponent, MenuListComponent, LoginComponent, AuthenticationComponent, LogoutComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    RouterModule.forRoot(routes),
    HttpClientModule
  ],
  exports: [RouterModule],
  providers: [{
    provide: HTTP_INTERCEPTORS,
    useClass: AuthInterceptor,
    multi: true,
  },],
  bootstrap: [AppComponent]
})
export class AppModule { }
