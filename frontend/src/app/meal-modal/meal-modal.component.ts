import { Component, Input, Output, EventEmitter, OnInit } from '@angular/core';
import { Meal } from '../meal/meal.model';
import { SharedService } from '../shared/shared.service';
import { Subscription } from 'rxjs';
import { MealService } from '../meal/meal.service';


@Component({
  selector: 'app-meal-modal',
  templateUrl: './meal-modal.component.html',
  styleUrls: ['./meal-modal.component.css'],
})
export class MealModalComponent implements OnInit {
  @Input() meal: Meal = {
    id: '',
    name: '',
    description: '',
    nutriscore: ''
  };
  @Output() cancel: EventEmitter<void> = new EventEmitter<void>();
  @Output() save: EventEmitter<Meal> = new EventEmitter<Meal>();

  editedMeal: Meal = { id: '', name: '', description: '', nutriscore: '' };
  showModal = false;
  private showEditModalSubscrption!: Subscription;
  private mealToEditSubscrption!: Subscription;
  constructor(private sharedService: SharedService, private mealService: MealService) { };

  ngOnInit() {
    console.log("Init Modal Edit")
    this.showEditModalSubscrption = this.sharedService.showEditModel$.subscribe(
      (showEditModal) => {
        console.log("!!!showEditModal:", showEditModal);
        this.showModal = showEditModal;
      }
    );
    this.mealToEditSubscrption = this.sharedService.mealToEdit$.subscribe(
      (mealToEdit) => {
        if (mealToEdit.id !== '') {

          console.log("!!!Meal to edit:", mealToEdit);
          this.mealService.getMealById(mealToEdit.id).subscribe((response) => {
            this.editedMeal = response;
          });
          this.editedMeal = mealToEdit;
        }
      }
    );
  }

  ngOnChanges() {
    // Copy the meal data to the editedMeal object when the input changes
    this.editedMeal = { ...this.meal };
  }

  openModal() {
    this.showModal = true;
  }

  closeModal() {
    this.showModal = false;
  }

  cancelEdit() {
    this.closeModal();
  }

  saveChanges() {
    this.mealService.updateMeal(this.editedMeal).subscribe((response) => {
      console.log('Meal update successfully:', response);
    });
    this.closeModal();
  }
}