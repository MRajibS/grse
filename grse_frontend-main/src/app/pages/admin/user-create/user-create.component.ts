import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { NgxSpinnerService } from 'ngx-spinner';
import { ToastrService } from 'ngx-toastr';
import { AdminService } from 'src/app/services/admin.service';
import { AdminLayoutComponent } from '../../layouts/admin/admin.component';
import * as Global from 'src/app/globals';
import { ActivatedRoute, Router } from '@angular/router';
import swal from 'sweetalert2';

@Component({
  selector: 'app-admin-user-create',
  templateUrl: './user-create.component.html',
  styleUrls: ['./user-create.component.css']
})
export class AdminUserCreateComponent implements OnInit {
  userForm: FormGroup;
  scanFingerprintForm: FormGroup;
  scanFacedataForm: FormGroup;
  scanCardForm: FormGroup;
  authenticationCombinationForm: FormGroup;

  alpeta_user_id: any;
  alpeta_face_data: any;
  apleta_card_data: any;

  alpeta_fingerprint_data: any[];
  alpeta_fingerprint_temp: any;

  departmentMaster: any[];
  designationMaster: any[];
  shiftMaster: any[];
  vendorMaster: any[];
  fingerMaster: any[];
  terminalMaster: any[];
  genderMaster: any[];
  maritalStatusMaster: any[];

  authenticationCombinationMaster: any[];
  userAuthenticationCombination: any[];
  authenticationModeMaster: any[];

  PageType = {
    'slug': "",
    'name': "",
    'key': "",
    'role_id': 0,
  }

  constructor(
    public AdminLayoutComponent: AdminLayoutComponent,
    private adminService: AdminService,
    public formBuilder: FormBuilder,
    private toastr: ToastrService,
    private spinner: NgxSpinnerService,
    private router: Router,
    private activatedRoute: ActivatedRoute
  ) {
    // this.userForm = formBuilder.group({
    //   "employee_code": [null, Validators.compose([Validators.required])],
    //   "first_name": [null, Validators.compose([Validators.required])],
    //   "middle_name": [null, Validators.compose([])],
    //   "last_name": [null, Validators.compose([Validators.required])],
    //   "phone": [null, Validators.compose([Validators.required, Validators.pattern("^[0-9]*$"), Validators.minLength(10), Validators.maxLength(10)])],
    //   "email": [null, Validators.compose([Validators.required, Validators.email])],

    //   "department_id": [null, Validators.compose([Validators.required])],
    //   "designation_id": [null, Validators.compose([Validators.required])],
    //   "shift_id": [null, Validators.compose([Validators.required])],
    //   "vendor_id": [null],

    //   "password": [null, Validators.compose([Validators.required, Validators.pattern("^[0-9]*$"), Validators.minLength(8), Validators.maxLength(20)])],
    //   "password_confirmation": [null, Validators.compose([Validators.required, Validators.pattern("^[0-9]*$"), Validators.minLength(8), Validators.maxLength(20)])],
    //   "alpeta_password": [null, Validators.compose([Validators.required, Validators.pattern("^[0-9]*$"), Validators.minLength(8), Validators.maxLength(10)])],

    //   "address": [null, Validators.compose([Validators.required])],
    //   "dob": [null, Validators.compose([Validators.required])],
    //   "employment_start_date": [null, Validators.compose([Validators.required])],
    //   "employment_end_date": [null, Validators.compose([Validators.required])],
    //   "gender": [null, Validators.compose([Validators.required])],
    //   "marital_status": [null, Validators.compose([Validators.required])],
    //   "nationality": [null, Validators.compose([Validators.required])],

    //   "pf_no": [null],
    //   "esi_no": [null],
    // });

    this.userForm = formBuilder.group({
      "employee_code": [null, Validators.compose([Validators.required])],
      "full_name": [null],
      "phone": [null],
      "email": [null],

      "department_id": [null],
      "costcntr": [null],
      "designation_id": [null],
      "shift_id": [null],
      "vendor_id": [null],

      "password": [null, Validators.compose([Validators.pattern("^[0-9]*$"), Validators.minLength(8), Validators.maxLength(20)])],
      "password_confirmation": [null, Validators.compose([Validators.pattern("^[0-9]*$"), Validators.minLength(8), Validators.maxLength(20)])],
      "alpeta_password": ['11111111', Validators.compose([Validators.required, Validators.pattern("^[0-9]*$"), Validators.minLength(8), Validators.maxLength(10)])],

      "address": [null],
      "dob": [null],
      "employment_start_date": [null],
      "employment_end_date": [null],
      "employment_separation_date": [null],
      "gender": [null],
      "marital_status": [null],
      "nationality": [null],
      "employment_type": [null],
      "pf_no": [null],
      "esi_no": [null],
    });

    this.scanFacedataForm = formBuilder.group({
      "terminal_id": [null, Validators.compose([Validators.required])],
    });

    this.scanCardForm = formBuilder.group({
      "terminal_id": [null, Validators.compose([Validators.required])],
    });

    this.scanFingerprintForm = formBuilder.group({
      "alpeta_figerprint_id": [null, Validators.compose([Validators.required])],
      "terminal_id": [null, Validators.compose([Validators.required])],
    });

    this.authenticationCombinationForm = formBuilder.group({
      "authentication_mode": [null, Validators.compose([Validators.required])],
    });

    this.departmentMaster = [];
    this.designationMaster = [];
    this.shiftMaster = [];
    this.vendorMaster = [];
    this.fingerMaster = [];
    this.terminalMaster = [];

    this.alpeta_user_id = null;
    this.alpeta_face_data = null;
    this.apleta_card_data = null;

    this.alpeta_fingerprint_data = [];
    this.alpeta_fingerprint_temp = null;

    this.userAuthenticationCombination = [
      { "value": "CD", "description": "Card" },
      { "value": "FAW", "description": "Face" },
    ]

    this.authenticationCombinationMaster = [
      { "value": "FP", "description": "Fingerprint" },
      { "value": "PW", "description": "Password" },
    ]

    this.authenticationModeMaster = [
      { "value": "AND", "description": "AND" },
      { "value": "OR", "description": "OR" },
    ]

    this.genderMaster = [
      { "value": "M", "description": "Male" },
      { "value": "F", "description": "Female" },
    ]

    this.maritalStatusMaster = [
      { "value": "single", "description": "Single" },
      { "value": "married", "description": "Married" },
    ]

    switch (activatedRoute.snapshot.url[0]?.path) {
      case 'employees':
        this.PageType = {
          'slug': "employees",
          'name': "Employees",
          'key': "employee",
          'role_id': 3,
        }
        break;

      case 'contractlabour':
        this.PageType = {
          'slug': "contractlabour",
          'name': "Contract Labour",
          'key': "contractlabour",
          'role_id': 2,
        }
        break;
    }

    this.authenticationCombinationForm.patchValue({
      'authentication_mode': { "value": "AND", "description": "AND" }
    })
  }

  async ngOnInit() {
    setTimeout(() => {
      this.AdminLayoutComponent.loadPageTitle("Manage " + this.PageType.name, "", [
        { 'url': '/admin/' + this.PageType.slug, 'name': this.PageType.name },
        { 'url': 'active', 'name': 'Register' },
      ])
    })

    await this.getUserCreateMaster();


    let employee_code = "";
    this.activatedRoute.queryParams.subscribe(
      params => employee_code = params.employee_code
    )

    if (employee_code) {
      this.userForm.patchValue({
        'employee_code': employee_code
      })

      this.fetchEmployeeDetailsFromEmployeeCode();
      $('[formControlName="employee_code"]').attr("readonly", 'true');
    }
  }

  getUserCreateMaster() {
    return new Promise((resolve, reject) => {
      this.spinner.show();
      this.adminService.getUserCreateMaster().subscribe(res => {
        if (res.status == 'success') {
          this.departmentMaster = [];
          res.master.department.forEach((element: any) => {
            this.departmentMaster.push({
              'id': element.id,
              'costcntr': element.costcntr,
              'description': element.shop_name + " (" + element.costcntr + ")",
            })
          });

          this.designationMaster = [];
          res.master.designation_masters.forEach((element: any) => {
            this.designationMaster.push({
              'id': element.id,
              'description': element.code,
            })
          });

          this.shiftMaster = [];
          res.master.shift_masters.forEach((element: any) => {
            this.shiftMaster.push({
              'id': element.id,
              'description': element.name + " (" + element.code + ")",
            })
          });

          // this.vendorMaster = [];
          // res.master.vendors.forEach((element: any) => {
          //   this.vendorMaster.push({
          //     'id': element._id,
          //     'description': element.name,
          //   })
          // });

          this.fingerMaster = [];
          res.master.fingerprint_master.forEach((element: any) => {
            this.fingerMaster.push({
              'id': element._id,
              'alpeta_value': element.alpeta_value,
              'description': element.name,
            })
          });

          this.terminalMaster = [];
          if (res.master?.AvailableTerminalList?.treminals?.TerminalList instanceof Array) {
            res.master.AvailableTerminalList.treminals.TerminalList.forEach((element: any) => {
              this.terminalMaster.push({
                'id': element.ID,
                'description': element.Name,
              })
            });
          }

          // this.alpeta_user_id = res.master?.ApletaUserID?.user_id?.dmUserInfo?.ID ?? "";
        } else if (res.status == 'val_error') {
          this.toastr.error(Global.showValidationMessage(res.errors));
        } else {
          this.toastr.error(res.message);
        }

        this.spinner.hide();
        resolve(true);
      }, (err) => {
        this.toastr.error(Global.showServerErrorMessage(err));
        this.spinner.hide();
        resolve(true);
      });
    });
  }

  createUser(event: any) {
    this.userForm.markAllAsTouched();
    setTimeout(function () {
      Global.scrollToQuery(".form-control.is-invalid.ng-invalid")
    }, 100);

    if (this.userForm.valid) {
      if (this.alpeta_fingerprint_data.length < 1) {
        $('#open-fingerprint-modal').click();
        this.toastr.warning("Scan the fingerprint before creating the user")
        return;
      }

      if (!this.alpeta_face_data) {
        $('#open-facedata-modal').click();
        this.toastr.warning("Scan the face before creating the user")
        return;
      }

      if (!this.apleta_card_data) {
        $('#open-card-modal').click();
        this.toastr.warning("Scan the card before creating the user")
        return;
      }

      if (!this.validateAuthenticationCombination(true)) {
        $('#open-authcombination-modal').click();
        return;
      }

      event.target.classList.add('btn-loading');

      this.adminService.createUser({
        "role_id": this.PageType.role_id,
        'alpeta_user_id': this.alpeta_user_id,
        'employee_id': this.userForm.value.employee_code,

        'full_name': this.userForm.value.full_name ?? "",
        'phone': this.userForm.value.phone ?? "",
        'email': this.userForm.value.email ?? "",

        'costcntr': this.userForm.value.department_id?.costcntr ?? "",
        'designation_id': this.userForm.value.designation_id?.id ?? "",
        'shift_id': this.userForm.value.shift_id?.id ?? "",
        'vendor_id': this.userForm.value.vendor_id?.id ?? "",

        'password': this.userForm.value.password ?? "",
        'password_confirmation': this.userForm.value.password_confirmation ?? "",
        'alpeta_password': this.userForm.value.alpeta_password ?? "",

        'address': this.userForm.value.address ?? "",
        'dob': this.userForm.value.dob ?? "",
        'employment_start_date': this.userForm.value.employment_start_date ?? "",
        'employment_end_date': this.userForm.value.employment_end_date ?? "",
        'employment_separation_date': this.userForm.value.employment_separation_date ?? "",
        'gender': this.userForm.value.gender?.value ?? "",
        'marital_status': this.userForm.value.marital_status?.value ?? "",
        'nationality': this.userForm.value.nationality ?? "",
        'employment_type': this.userForm.value.employment_type ?? "",
        'pf_no': this.userForm.value.pf_no ?? "",
        'esi_no': this.userForm.value.esi_no ?? "",

        'alpeta_fingerprint_data': JSON.stringify(this.alpeta_fingerprint_data),
        'alpeta_face_data': JSON.stringify(this.alpeta_face_data),
        'alpeta_card_data': JSON.stringify(this.apleta_card_data),

        'is_deleted': 0,
        'status': 'active',
        'last_update_date': "",
        'last_updated_by': "",
        'profile_picture': "",

        'AuthInfo': JSON.stringify({
          'authentication_combination': this.userAuthenticationCombination,
          'authentication_mode': this.authenticationCombinationForm.value.authentication_mode?.value ?? "",
        })
      }).subscribe(res => {
        if (res.status == 'success') {
          swal.fire({
            title: res.message,
            html: '<p class="m-1">Employee ID: <b>' + this.userForm.value.employee_code + '</b></p>\
            <p class="m-1">Full Name: <b>'+ this.userForm.value.full_name ?? 'N/A' + '</b></p>',
            icon: 'success',
            confirmButtonText: 'OKAY',
          })
          // this.toastr.success(res.message);
          this.router.navigate(['/admin/' + this.PageType.slug + '/list']);
        } else if (res.status == 'val_error') {
          this.toastr.error(Global.showValidationMessage(res.errors));
        } else {
          this.toastr.error(res.message);
        }

        event.target.classList.remove('btn-loading');
      }, (err) => {
        event.target.classList.remove('btn-loading');
        this.toastr.error(Global.showServerErrorMessage(err));
      });
    }
  }

  fingerSelected(finger_id: any) {
    // alert(finger_id)
    if (!this.checkFingerCaptured(finger_id)) {
      this.scanFingerprintForm.patchValue({
        "alpeta_figerprint_id": this.fingerMaster.find((obj: any) => {
          return obj.alpeta_value == finger_id ?? null
        }) ?? null,
      })
    } else {
      swal.fire({
        title: 'Are you sure want to remove?',
        text: 'You will not be able to recover this data!',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Yes, remove it!',
        cancelButtonText: 'No, keep it'
      }).then((result) => {
        if (result.value) {
          this.alpeta_fingerprint_data = this.alpeta_fingerprint_data.filter(function (value, index, arr) {
            return value.FingerID != finger_id
          });
        } else if (result.dismiss === swal.DismissReason.cancel) {
          swal.fire(
            'Cancelled',
            'Your data is safe :)',
            'error'
          )
        }
      })
    }
  }

  checkFingerCaptured(finger_id: any) {
    let fp_data = this.alpeta_fingerprint_data.find((obj: any) => {
      return obj.FingerID == finger_id ?? null
    })

    if (fp_data) {
      return true;
    } else {
      return false;
    }
  }

  scanFingerPrint(event: any) {
    this.scanFingerprintForm.markAllAsTouched();
    setTimeout(function () {
      Global.scrollToQuery(".form-control.is-invalid.ng-invalid")
    }, 100);

    if (this.scanFingerprintForm.valid) {
      this.alpeta_fingerprint_temp = null;
      this.toastr.info("Please put the " + this.scanFingerprintForm.value.alpeta_figerprint_id.description + " on the device")

      event.target.classList.add('btn-loading');

      this.adminService.scanUserFingerprint({
        'alpeta_user_id': this.alpeta_user_id,
        'alpeta_figerprint_id': this.scanFingerprintForm.value.alpeta_figerprint_id.alpeta_value,
        'terminal_id': this.scanFingerprintForm.value.terminal_id.id,
      }).subscribe(res => {
        // res = {
        //   "dmFPImage": {
        //     "ConvImage1": "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",
        //     "ConvImage2": "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",
        //     "FingerID": this.scanFingerprintForm.value.alpeta_figerprint_id.alpeta_value,
        //     "Template1": "VU5JT04EWgADMPwQBFrGGA7Lc4K0T1CatIJZlBHkFn7+85oI3rgU8c60VFgrUMEXH6eQGTzKpjknY8VrDPw6BE4PVIgvKxQnelSXiRMQiLF34olNrsi/ytMYscry65UNP2A6dfYzGNNlvImEB9rc8PwhWouw5In/YWhEuc0hAjC2cATd0Mjoiwm+lpxG2+xZ26p1Bob2Hp3+OK1lGvVFvMduzspDaPsdrIJvz2wwPDP7SuWJeIHu2XExlgupUeLNA8AypdgY+LsFpk2n/5iB8qjfcgyiWaIR7D3cDJr8X15WU8Y71ASae2dBwR0c02t3dM3UU9L+jBLpv9CpuKQtVT0m2lWNp1o3y1Rrvpj7A0SiMX5JlqfVRYe4XJ9nhW4PfUvpHVHWxnhp20G3Pt1xwrLAAnsaYeLcC4WkPsGQAlPQTCaiecRL0O1tZpzisgWeq4Zg0DLwUL3XTsWtZtN83hSPIWMc5Q1x6rpEGzVezdknJAeIpBp3Wp/l1UNbBA6+UB1zzmXs5HkIpGZ8qQi97A==",
        //     "Template2": "VU5JT04EWgADMGgQBF3JFL1f9vAb2W5mCnxl7XTNTEFvi3onH6oQXTrk2D84xidp+4a1eDnNy/ei+ApQoF4wvo57i0U7adSh5N+3LgZYp/WxsNc8zH8T+lPseWOAvNR+5FSwHFwG0xodL6Yq7RaB52Z5kDTjM2v0U0lSzLrZsMc4fyIYnV/oPZ7Yh4WAI7xCCtlLO72zpk/K2Au/Gb8KIakS/CNzUUQkE4kAUqzsOaLwmFMC7pL5/jwm+MNlR0rPvQKqfwd5fxvbpw1qscvSfCDbxYllrZks/lhklYANROY2T/XbC8xfG8VEOBa2kFOUGyS/l7movzIHzI57NQqZkJCt+qf015QYHruiS/LtiPEtjkeQTcqHn98Xf+W5ZhgJ4n5+K3KmP5uV0KQTZLrmfuKwwTc6Iw2PJyoMOPfpHUWWw2znqu/q2ukep/X51Y9VbxUcfbYu8gs9CQehXkgtoHaZIL807IrWbhrwinEms53ADnnMaOxMKgIa/HrFt1mfeHbgMuWY2WIUlVmSexczFA==",
        //     "TotalSize": 74752,
        //     "UserID": this.alpeta_user_id
        //   },
        //   "message": "Fingerprint captured successfully.",
        //   "status": "success"
        // };

        if (res.status == 'success') {
          this.toastr.success(res.message);
          this.alpeta_fingerprint_temp = res.dmFPImage;
          this.alpeta_fingerprint_data.push(res.dmFPImage);
          this.scanFingerprintForm.get('alpeta_figerprint_id')?.reset();
        } else if (res.status == 'val_error') {
          this.toastr.error(Global.showValidationMessage(res.errors));
        } else {
          this.toastr.error(res.message);
        }

        event.target.classList.remove('btn-loading');
      }, (err) => {
        event.target.classList.remove('btn-loading');
        this.toastr.error(Global.showServerErrorMessage(err));
      });
    }
  }

  scanFaceData(event: any) {
    this.alpeta_face_data = null;
    this.scanFacedataForm.markAllAsTouched();
    setTimeout(function () {
      Global.scrollToQuery(".form-control.is-invalid.ng-invalid")
    }, 100);

    if (this.scanFacedataForm.valid) {
      event.target.classList.add('btn-loading');

      this.adminService.scanUserFacedata({
        'terminal_id': this.scanFacedataForm.value.terminal_id.id,
      }).subscribe(res => {
        // res = {
        //   "UserFaceWTInfo": [
        //     {
        //       "TemplateData": "AAAAAEtxQUFBQUFBQUFBTUJBQUF3c0RBUE5MUTBEMkJnQUM4Z1lBQVBJR0FnRHdBQUFBQWdZQUF2S0dnb0QyQmdJQTlvYUFnUFlHQWdEeUJnQUM5NHVCZ3ZhR2dJRDJSa0pDOWdZQ0F2S0dnSUwzQ3dNQTg0dUJndmNMQXdMekN3TUE4Z1lBQVB1TGdZRDBBQUFBQXdzQkF2Y0xBd0wyQmdJQzhnWUFBdmJHd3NMMEFBQUFBNHVCZ1BiR3dzTDJCZ0FBOHdzQkFQWUdBQUQzQ3dFQTlnWUNBdklHQWdMeUJnQUE5c2JDd3ZhR2dvTDBBQUFBQUFBQUFBSUdBQUR6Q3dFQytzYkN3UFlHQUFMeUJnSUM5Z1lBQXZZR0FnRDJSa0pDOXdzREF2WUdBQUR6eThQQTlnWUNBUFFBQUFBQ0JnQUM5Z1lBQXZlTGdZTDJCZ0FDOWdZQUFQTkxRMEwySmlBaSt3c0RBdkpHUWtMMkJnQUErNHVEZ1BjTEFRTDJ4c0xBOWdZQ0F2TUxBd0x6eThQQTlnWUNBdllHQUFMemk0T0E5Z1lBQVBhR2dJTDJCZ0lBODB0RFF2Y0xBd0x5QmdBQzh3c0RBdk9MZ1lEMEFBQUFBaVlnSVBnQUFBQUNCZ0lBOGlZZ0lQc0xBUUwySmlBZytnWUFBUE1MQXdEeUJnQUE5NHVEZ1BZR0FnRHlSa0pBOXNiQXdQcUdnSUQyQmdJQzh3c0RBdklHQWdEMkJnQUE5NHVCZ1BZR0FnRHpDd01DOW9hQ2d2WUdBQUR5QmdBQzhnWUNBdklHQWdEemk0R0M5b2FBZ1BZR0FnRHlCZ0lDOWdZQUFQY0xBd0x5aG9DQzlnWUFBdlFBQUFBQ0JnQUE5d3NEQVBNTEFRTDJSa0JDKzR1QmdQY0xBUUQzaTRPQTlvYUFnUFlHQUFEekN3TUM4d3NCQXZZR0FBRDJCZ0FBOG1aZ1l2dUxnNEwyQmdJQThzYkN3dllHQUFMemk0R0M5d3NEQXZJR0FnTHlCZ0FBOTR1Qmd2WUdBQUx6aTRHQzk0dUJndmNMQXdEeUJnQUE5a1pDUXZjTEF3RHdBQUFBQXNiQ3dQYUdnb0wyQmdBQzhvYUFndllHQWdEeUppQWcra1pDUXZZR0FBTDNTME5BOW9hQWdQWUdBQUQyQmdBQTk0dUJndmNMQXdMekN3TUE4b2FBZ1BjTEF3TDNpNEdBOWdZQ0FQTUxBUUwyeHNMQzlvYUFndmJHd3NEMkJnSUM4Z1lDQXZRQUFBQUNSa0pDOWdZQ0FQSUdBQUQzaTRHQTlrWkFRUHBHUWtEMkJnQUE4d3NEQVBZR0FBRHp5OFBBOXdzQkFQZkx3OEQyQmdJQzlvYUFnUGJHd3NEMkJnQUM5Z1lDQVBZR0FnTHpDd01DOGdZQUFQWUdBZ0R5QmdBQThvYUFnUGFHZ0lEMkJnQUE5c2JDd1BZR0FBTDNDd01BOGdZQUFQYUdnSUwzQ3dFQzlnWUFBUElHQWdMMkJnSUE5b2FDZ3ZlTGc0RDJCZ0FDOXNiQ3dQY0xBd0wzQ3dFQTlnWUNBUFlHQUFMekN3TUM5d3NEQXZZR0FnRDJob0NDOWdZQUF2ZExRMEwyaG9LQTlnWUNBUGFHZ29EMlJrSkE5Z1lDQXZNTEFRTDJCZ0lDOTB0RFFQUUFBQUFDQmdJQzhnWUNBUE1MQXdEeWhvQ0M5Z1lBQXZJR0FnRDJ4c0xBOWdZQ0FQY0xBd0x6Q3dNQzgwdERRdmJHd3NMMkJnSUE5Z1lDQVBNTEFRRDJCZ0lBOGdZQUFQSUdBZ0R5QmdJQzkwdEJRUHBHUWtMMkJnSUE4Z1lDQVBBPT0=",
        //       "TemplateSize": 1388,
        //       "TemplateType": 0,
        //       "UserID": ""
        //     },
        //     {
        //       "TemplateData": "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",
        //       "TemplateSize": 23417,
        //       "TemplateType": 1,
        //       "UserID": ""
        //     }
        //   ],
        //   "message": "Face data captured successfully.",
        //   "status": "success"
        // };

        if (res.status == 'success') {
          this.toastr.success(res.message);
          this.alpeta_face_data = res.UserFaceWTInfo;
        } else if (res.status == 'val_error') {
          this.toastr.error(Global.showValidationMessage(res.errors));
        } else {
          this.toastr.error(res.message);
        }

        event.target.classList.remove('btn-loading');
      }, (err) => {
        event.target.classList.remove('btn-loading');
        this.toastr.error(Global.showServerErrorMessage(err));
      });
    }
  }

  scanCard(event: any) {
    this.apleta_card_data = null;
    this.scanCardForm.markAllAsTouched();
    setTimeout(function () {
      Global.scrollToQuery(".form-control.is-invalid.ng-invalid")
    }, 100);

    if (this.scanCardForm.valid) {
      event.target.classList.add('btn-loading');

      this.adminService.scanUserCard({
        'terminal_id': this.scanCardForm.value.terminal_id.id,
      }).subscribe(res => {
        // res = {
        //   "CardData": {
        //     "CardNum": "A7B7E01907401F",
        //     "UserID": ""
        //   },
        //   "message": "Card captured successfully.",
        //   "status": "success"
        // };

        if (res.status == 'success') {
          this.toastr.success(res.message);
          this.apleta_card_data = res.CardData;
        } else if (res.status == 'val_error') {
          this.toastr.error(Global.showValidationMessage(res.errors));
        } else {
          this.toastr.error(res.message);
        }

        event.target.classList.remove('btn-loading');
      }, (err) => {
        event.target.classList.remove('btn-loading');
        this.toastr.error(Global.showServerErrorMessage(err));
      });
    }
  }

  employeeCodeChanged() {
    if (this.userForm.value.employee_code) {
      swal.fire({
        title: 'Fetch data from Master DB',
        text: 'Do you want to auto-fill details?',
        icon: 'info',
        showCancelButton: false,
        allowOutsideClick: false,
        confirmButtonText: 'Yes',
        cancelButtonText: 'No'
      }).then((result) => {
        if (result.value) {
          this.fetchEmployeeDetailsFromEmployeeCode()
        }
      })
    }
  }

  validateAuthenticationCombination(isSubmit: Boolean = false) {
    if (!this.authenticationCombinationForm.valid) {
      this.authenticationCombinationForm.markAllAsTouched();
      setTimeout(function () {
        Global.scrollToQuery(".form-control.is-invalid.ng-invalid")
      }, 500);

      return false;
    }

    if (this.userAuthenticationCombination.length < 1) {
      this.toastr.error("You must select atleast one authentication system")
      return false;
    }

    if (this.userAuthenticationCombination.length > 3) {
      this.toastr.error("You cannot select more than three authentication combination")
      return false;
    }

    this.userAuthenticationCombination.forEach(element => {

      if (element.value == "FP" && this.alpeta_fingerprint_data.length < 1) {
        this.toastr.warning("Scan the fingerprint before creating the user")

        if (isSubmit) {
          return;
        }
      }

      if (element.value == "FAW" && !this.alpeta_face_data) {
        this.toastr.warning("Scan the face before creating the user")

        if (isSubmit) {
          return;
        }
      }

      if (element.value == "CD" && !this.apleta_card_data) {
        this.toastr.warning("Scan the card before creating the user")

        if (isSubmit) {
          return;
        }
      }

      if (element.value == "PW" && !this.userForm.value.alpeta_password) {
        this.toastr.warning("Please enter a biometric password before creating the user")

        if (isSubmit) {
          return;
        }
      }
    });

    $('#authcombination-modal')?.find('[data-bs-dismiss="modal"]')?.click()
    return true;
  }

  fetchEmployeeDetailsFromEmployeeCode() {
    this.spinner.show();
    this.adminService.getUserDetailsfromEmployeeCode(this.userForm.value.employee_code)
      .subscribe(res => {
        this.spinner.hide();
        if (res.status == 'success') {
          if (res.user_data?.user_data?.status == "active" && !res.user_data?.user_data?.alpeta_user_id) {
            this.userForm.patchValue({
              "full_name": res.user_data?.user_data?.full_name ?? null,
              "phone": res.user_data?.user_data?.phone ?? null,
              "email": res.user_data?.user_data?.email ?? null,

              "address": res.user_data?.user_data?.address ?? null,
              "dob": res.user_data?.user_data?.dob ?? null,
              "employment_start_date": res.user_data?.user_data?.employment_start_date ?? null,
              "employment_end_date": res.user_data?.user_data?.employment_end_date ?? null,
              "employment_separation_date": res.user_data?.user_data?.employment_separation_date ?? null,
              "nationality": res.user_data?.user_data?.nationality ?? null,
              "employment_type": res.user_data?.user_data?.employment_type ?? null,
              "pf_no": res.user_data?.user_data?.pf_no ?? null,
              "esi_no": res.user_data?.user_data?.esi_no ?? null,

              "gender": this.genderMaster.find((obj: any) => {
                return obj.value == res.user_data?.user_data?.gender ?? null
              }) ?? null,

              "marital_status": this.maritalStatusMaster.find((obj: any) => {
                return obj.value == res.user_data?.user_data?.marital_status ?? null
              }) ?? null,

              "designation_id": this.designationMaster.find((obj: any) => {
                return obj.id == res.user_data?.user_data?.designation_id ?? null
              }) ?? null,

              "shift_id": this.shiftMaster.find((obj: any) => {
                return obj.id == res.user_data?.user_data?.shift_id ?? null
              }) ?? null,

              "vendor_id": this.vendorMaster.find((obj: any) => {
                return obj.id == res.user_data?.user_data?.vendor_id ?? null
              }) ?? null,
            })

            if ([3].includes(this.PageType.role_id)) {
              this.userForm.patchValue({
                "department_id": this.departmentMaster.find((obj: any) => {
                  return obj.costcntr == res.user_data?.user_data?.costcntr ?? null
                }) ?? null,
              })
            } else if ([2].includes(this.PageType.role_id)) {
              this.userForm.patchValue({
                "costcntr": res.user_data?.user_data?.costcntr,
              })
            }

            this.alpeta_user_id = this.userForm.value.employee_code;
          } else {
            let swaltext: any = "Registration cannot be initiated. Employee ID not validated";

            if (res.user_data?.user_data?.status != "active") {
              swaltext = 'Registration of the user is not possible as the current status of the user is inactive'
            }

            if (res.user_data?.user_data?.alpeta_user_id) {
              swaltext = 'The user registration has already been completed'
            }

            swal.fire({
              title: 'Registration Declined',
              text: swaltext,
              icon: 'error',
            })

            Global.resetForm(this.userForm);
          }
        } else if (res.status == 'val_error') {
          this.toastr.error(Global.showValidationMessage(res.errors));
          Global.resetForm(this.userForm);
        } else {
          this.toastr.error(res.message);
          Global.resetForm(this.userForm);
        }
      }, (err) => {
        this.spinner.hide();
        this.toastr.error(Global.showServerErrorMessage(err));
        Global.resetForm(this.userForm);
      });
  }

  assignDummyCard() {
    let dummyCard = {
      "CardNum": "GRSDMCARD" + Math.floor(100000 + Math.random() * 900000),
      "UserID": ""
    }

    this.apleta_card_data = dummyCard;
    $('#card-modal').find('[data-bs-dismiss="modal"]').click();
  }
}
