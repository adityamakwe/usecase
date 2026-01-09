import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class EndpointServiceService {

  constructor() { }

  public SERVER_URL = "http://localhost:8000/orsapi";
  public DOCTOR = this.SERVER_URL + "/Doctor";
}