import { Injectable } from '@angular/core';
import axios from 'axios';

@Injectable({
  providedIn: 'root',
})
export class MenuService {
  private baseUrl = 'http://127.0.0.1:5000'; // Replace with your Flask backend URL
  createMenu(data: any) {
    const headers = {
      'Content-Type': 'application/json'
    };
    // return axios.post(`${this.baseUrl}/menu}`, data);
    return axios.options(`${this.baseUrl}/menu/`, { headers })
      .then((response: { data: any; }) => {
        // Pre-flight request succeeded, send the actual POST request with the data
        return axios.post(`${this.baseUrl}/menu/`, data, { headers });
      })
      .then((response: { data: any; }) => {
        // Actual POST request succeeded, return the response data
        return response.data;
      })
      .catch((error: { data: any; }) => {
        // Handle any errors
        throw error;
      });
  }
  updateMenu(mealId: string, data: any) {
    const headers = {
      'Content-Type': 'application/json'
    };
    return axios.options(`${this.baseUrl}/menu/`, { headers })
      .then((response: { data: any; }) => {
        // Pre-flight request succeeded, send the actual POST request with the data
        return axios.patch(`${this.baseUrl}/menu/${mealId}`, data, { headers });
      })
      .then((response: { data: any; }) => {
        // Actual POST request succeeded, return the response data
        return response.data;
      })
      .catch((error: { data: any; }) => {
        // Handle any errors
        throw error;
      });
  }
  commitMenu(menuId: string) {
    const headers = {
      'Content-Type': 'application/json'
    };
    return axios.options(`${this.baseUrl}/commit/${menuId}`, { headers })
      .then((response: { data: any; }) => {
        // Pre-flight request succeeded, send the actual POST request with the data
        return axios.post(`${this.baseUrl}/commit/${menuId}`, {}, { headers });
      })
      .then((response: { data: any; }) => {
        // Actual POST request succeeded, return the response data
        return response.data;
      })
      .catch((error: { data: any; }) => {
        // Handle any errors
        throw error;
      });
  }
  // commitMenu(menuId: string, data: any) {
  //   const headers = {
  //     'Content-Type': 'application/json'
  //   };
  //   return axios.options(`${this.baseUrl}/commit/`, { headers })
  //     .then((response: { data: any; }) => {
  //       // Pre-flight request succeeded, send the actual POST request with the data
  //       return axios.post(`${this.baseUrl}/commit/${menuId}`, data, { headers });
  //     })
  //     .then((response: { data: any; }) => {
  //       // Actual POST request succeeded, return the response data
  //       return response.data;
  //     })
  //     .catch((error: { data: any; }) => {
  //       // Handle any errors
  //       throw error;
  //     });

  // }
  getAllMenus() {
    const headers = {
      'Content-Type': 'application/json'
    };

    return axios.get(`${this.baseUrl}/menus`, { headers })
      .then((response) => {
        // Request succeeded, return the response data
        return response.data;
      })
      .catch((error) => {
        // Handle any errors
        throw error;
      });
  }
}
