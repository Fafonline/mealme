import { Component, OnInit } from '@angular/core';
import { Menu } from '../menu/menu.model'
import { MenuService } from '../menu/menu.service';
import { Subscription } from 'rxjs';
import { SharedService } from '../shared/shared.service';


@Component({
  selector: 'app-menu-list',
  templateUrl: './menu-list.component.html',
  styleUrls: ['./menu-list.component.css']
})
export class MenuListComponent implements OnInit {
  menuList: Menu[] = [];

  constructor(private menuService: MenuService, private sharedService: SharedService) { };
  private eventSubscription!: Subscription;

  ngOnInit() {
    // Fetch all menus when the component initializes
    this.fetchAllMenus();
    this.eventSubscription = this.sharedService.event$.subscribe(
      (event) => {
        if (event === "UpdateMenuList") {
          this.fetchAllMenus();
        }
      }
    );
  }
  fetchAllMenus() {
    // Call the getAllMenus method from the MenuService
    this.menuService.getAllMenus().then(
      (menus: any) => {
        this.menuList = menus;
        console.log("All menus:", this.menuList);
      },
      (error) => {
        console.error('Error fetching menus:', error);
        // Handle error, if needed (e.g., show an error message)
      }
    );
  }
  toggleDropDown(menu: any) {
    menu.show = !menu.show;
  }
}
