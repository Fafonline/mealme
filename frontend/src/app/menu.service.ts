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
      .then((response) => {
        // Pre-flight request succeeded, send the actual POST request with the data
        return axios.post(`${this.baseUrl}/menu/`, data, { headers });
      })
      .then((response) => {
        // Actual POST request succeeded, return the response data
        return response.data;
      })
      .catch((error) => {
        // Handle any errors
        throw error;
      });

  }
  commitMenu(data: any) {
    const headers = {
      'Content-Type': 'application/json'
    };
    // return axios.post(`${this.baseUrl}/menu}`, data);
    return axios.options(`${this.baseUrl}/menu/commit`, { headers })
      .then((response) => {
        // Pre-flight request succeeded, send the actual POST request with the data
        return axios.post(`${this.baseUrl}/menu/commit`, data, { headers });
      })
      .then((response) => {
        // Actual POST request succeeded, return the response data
        return response.data;
      })
      .catch((error) => {
        // Handle any errors
        throw error;
      });

  }
}
