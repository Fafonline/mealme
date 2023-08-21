import { Component, OnInit } from '@angular/core';
import { SharedService } from '../shared/shared.service';
import { Subscription } from 'rxjs';



@Component({
  selector: 'app-menu-modal',
  templateUrl: './menu-modal.component.html',
  styleUrls: ['./menu-modal.component.css'],
})
export class MenuModalComponent implements OnInit {
  showMenuModal = false;
  menuToShow: any;
  private showMenuModalSubscrption!: Subscription;
  private menuToShowSubscrption!: Subscription;
  constructor(private sharedService: SharedService) { };

  ngOnInit() {
    console.log("Init Modal Edit")
    this.showMenuModalSubscrption = this.sharedService.showMenuModel$.subscribe(
      (showMenuModal) => {
        console.log("!!!showMenuModal:", showMenuModal);
        this.showMenuModal = showMenuModal;
      }
    );
    this.menuToShowSubscrption = this.sharedService.menuToShow$.subscribe(
      (menuToShow) => {
        console.log("Menu to show:", menuToShow)
        this.menuToShow = menuToShow;
        if (this.menuToShow.name === '' || this.menuToShow.name === undefined) {
          this.menuToShow.name = "No name"
        }
      }
    );
  }

  ngOnChanges() {

  }

  openModal() {
    this.showMenuModal = true;
  }

  closeModal() {
    this.showMenuModal = false;
  }
}