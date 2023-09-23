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
    this.menuService.getAllMenus().subscribe(
      (menus: any) => {
        this.menuList = menus;
        console.log("All menus:", this.menuList);
      },
      (error: any) => {
        console.error('Error fetching menus:', error);
        // Handle error, if needed (e.g., show an error message)
      }
    );
  }
  toggleDropDown(menu: any) {
    menu.show = !menu.show;
  }
  exportMenu(menu: any) {
    // Create the menu content in the desired format
    const menuContent = this.generateMenuContent(menu);

    // Create a Blob containing the menu content
    const blob = new Blob([menuContent], { type: 'text/plain' });

    // Create an anchor element for downloading
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    const filename = `menu_${menu.name}_${new Date().toISOString().slice(0, 10)}.md`.replace(/\//g, '-').replace(/\s/g, '_');

    // Set the download attribute with the file title
    a.setAttribute('download', filename);

    // Create an event to trigger the click event on the anchor element
    const clickEvent = new MouseEvent('click', {
      view: window,
      bubbles: true,
      cancelable: false,
    });

    // Dispatch the click event on the anchor element
    a.dispatchEvent(clickEvent);

    // Clean up by revoking the Blob URL
    URL.revokeObjectURL(a.href);
  }

  generateMenuContent(menu: any): string {
    // Define the format for the menu content
    let creationDate = new Date().toISOString().slice(0, 10);
    let menuContent = `# ${menu.name} - ${creationDate}\n`.replace(/\//g, '-');
    // Add the creation_date field with the current date
    menuContent += '---\n';
    menuContent += `creation_date: ${creationDate}\n`
    menuContent += '---\n';

    menu.meals.forEach((meal: any, index: number) => {
      menuContent += `- [ ] ${meal.name}\n`;
    });

    menuContent += '---\n';
    menuContent += '#mealme\n';

    return menuContent;
  }
}
