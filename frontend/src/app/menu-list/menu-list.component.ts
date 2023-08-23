import { Component, OnInit } from '@angular/core';
import { Menu } from '../menu/menu.model'
import { MenuService } from '../menu/menu.service';


@Component({
  selector: 'app-menu-list',
  templateUrl: './menu-list.component.html',
  styleUrls: ['./menu-list.component.css']
})
export class MenuListComponent implements OnInit {
  menuList: Menu[] = [];

  constructor(private menuService: MenuService) { };

  ngOnInit() {
    // Fetch all menus when the component initializes
    this.fetchAllMenus();
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
