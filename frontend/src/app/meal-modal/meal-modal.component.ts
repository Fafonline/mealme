import { Component, Input, Output, EventEmitter, OnInit } from '@angular/core';
import { Meal } from '../meal.model';
import { SharedService } from '../shared.service';
import { Subscription } from 'rxjs';

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
  };
  @Output() cancel: EventEmitter<void> = new EventEmitter<void>();
  @Output() save: EventEmitter<Meal> = new EventEmitter<Meal>();

  editedMeal: Meal = { id: '', name: '', description: '' };
  showModal = false;
  private showEditModalSubscrption!: Subscription;
  constructor(private sharedService: SharedService) { };

  ngOnInit() {
    console.log("Init Modal Edit")
    this.showEditModalSubscrption = this.sharedService.showEditModel$.subscribe(
      (showEditModal) => {
        console.log("!!!showEditModal:", showEditModal);
        this.showModal = showEditModal;
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
    this.closeModal();
  }
}