import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { FormsModule } from '@angular/forms';
import { DoctorComponent } from './doctor/doctor.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { NavbarComponent } from './navbar/navbar.component';
import { FooterComponent } from './footer/footer.component';
import { HttpServiceService } from './http-service.service';
import { ServiceLocatorService } from './service-locator.service';
import { HttpClientModule } from '@angular/common/http';
import { DoctorListComponent } from './doctor/doctor-list.component';

@NgModule({
  declarations: [
    AppComponent,
    DoctorComponent,
    DashboardComponent,
    NavbarComponent,
    FooterComponent,
    DoctorListComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    HttpClientModule,
  ],
  providers: [
    HttpServiceService,
    ServiceLocatorService
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
