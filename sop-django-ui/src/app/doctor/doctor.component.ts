import { Component } from '@angular/core';
import { BaseCtl } from '../base.component';
import { ActivatedRoute } from '@angular/router';
import { ServiceLocatorService } from '../service-locator.service';

@Component({
  selector: 'app-doctor',
  templateUrl: './doctor.component.html',
  styleUrls: ['./doctor.component.css']
})
export class DoctorComponent extends BaseCtl {
  constructor(public locator: ServiceLocatorService, route: ActivatedRoute) {
    super(locator.endpoints.DOCTOR, locator, route);
  }

}
