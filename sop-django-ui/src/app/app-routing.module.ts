import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { DoctorComponent } from './doctor/doctor.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { NavbarComponent } from './navbar/navbar.component';
import { FooterComponent } from './footer/footer.component';
import { DoctorListComponent } from './doctor/doctor-list.component';

const routes: Routes = [
  {
    path: '',
    pathMatch: 'full',
    redirectTo: 'dashboard'
  },
  {
    path: "doctor",
    component: DoctorComponent
  },
  {
    path: "dashboard",
    component: DashboardComponent
  },
  {
    path: "navbar",
    component: NavbarComponent
  },
  {
    path: "footer",
    component: FooterComponent
  },
  {
    path: "doctorlist",
    component:DoctorListComponent
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes, { useHash: true })],
  exports: [RouterModule]
})
export class AppRoutingModule { }
