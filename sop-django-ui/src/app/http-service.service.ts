import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class HttpServiceService {

  constructor(private httpClient: HttpClient) { }

  post(endpoint: any, bean: any, callback: any) {
    return this.httpClient.post(endpoint, bean).subscribe((data: any) => {
      callback(data);
    })
  }

  get(endpoint: any, callback: any) {
    return this.httpClient.get(endpoint).subscribe((data: any) => {
      callback(data);
    })
  }

}
