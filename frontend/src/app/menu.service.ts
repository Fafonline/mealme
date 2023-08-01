import { Injectable } from '@angular/core';
import axios from 'axios';

@Injectable({
  providedIn: 'root',
})
export class MenuService {
  private baseUrl = 'http://127.0.0.1:5000'; // Replace with your Flask backend URL

  createMenu(data: any) {
    return axios.post(`${this.baseUrl}/menu}`, data);
  }
}
