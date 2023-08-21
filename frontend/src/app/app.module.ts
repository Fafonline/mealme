import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { MealsComponent } from './meal/meals.component';
import { MenuComponent } from './menu/menu.component';
import { FormsModule } from '@angular/forms';
import { MealModalComponent } from './meal-modal/meal-modal.component';
import { MenuModalComponent } from './menu-modal/menu-modal.component';

@NgModule({
  declarations: [
    AppComponent, MealsComponent, MenuComponent, MealModalComponent, MenuModalComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
