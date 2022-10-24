import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { UserService } from 'src/app/services/user.service';
import { ToastrService } from 'ngx-toastr';

@Component({
  selector: 'app-print-to-pdf',
  templateUrl: './print-to-pdf.component.html',
  styleUrls: ['./print-to-pdf.component.css']
})
export class PrintToPdfComponent implements OnInit {

  constructor(private router: Router, private userService: UserService, private toastr: ToastrService) { }


  userData: string[] = [];
  UserIds: any = []

  ngOnInit(): void {
  }

  getUser = (data: any) => {
    let payload = {
      "userId": data.empId,
      "name": data.empName,
    }


    this.userService.fetchUserId().subscribe(res =>{
      if(res.status=="success"){
        this.UserIds = res.data;
      }
      else {
        this.toastr.error(res.message);
      }
    })

    this.userService.fetchUserDetailById(payload).
      subscribe(res => {
        if (res.status == "success") {
          this.userData = res.data;
          this.userService.setUserData(this.userData);
        }
        else {
          this.toastr.error(res.message);
        }
      },
      )
  }
}
