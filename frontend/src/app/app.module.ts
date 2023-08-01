import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { MealsComponent } from './meals.component';
import { MenuComponent } from './menu.component';
import { FormsModule } from '@angular/forms'; // Import the FormsModule


@NgModule({
  declarations: [
    AppComponent, MealsComponent, MenuComponent
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
