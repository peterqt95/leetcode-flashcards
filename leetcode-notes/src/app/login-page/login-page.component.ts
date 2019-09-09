import { Component, OnInit } from '@angular/core';
import { LoginService } from '@services/login.service';
import { PartialObserver } from 'rxjs';
import { LoginStatus } from './Classes/LoginStatus';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { LoadStatus } from '@app/shared/Classes/LoadStatus';

@Component({
  selector: 'app-login-page',
  templateUrl: './login-page.component.html',
  styleUrls: ['./login-page.component.css']
})
export class LoginPageComponent implements OnInit {

  // Form Group
  loginFg: FormGroup;

  // Hide for password
  hidePwd = true;

  // Load Status
  loadStatus: LoadStatus = new LoadStatus();

  constructor(
    private loginService: LoginService,
    private _formBuilder: FormBuilder
  ) { }

  ngOnInit() {
    // Route away if logged in
    if (this.loginService.isLoggedIn) {

    } else {
      this.loginFg = this._formBuilder.group({
        userName: ['', Validators.required],
        password: ['', Validators.required]
      });

      this.loadStatus.isLoaded = true;
    }
  }

  public login() {
    this.loadStatus.isLoaded = false;
    const userName = this.loginFg.controls.userName.value;
    const password = this.loginFg.controls.password.value;
    this.loginService.login(userName, password).subscribe(this.loginSub());
  }

  private loginSub(): PartialObserver<any> {
    return {
      next: (data: LoginStatus) => {
        if (!data.status) {
          this.loadStatus.isError = true;
          this.loadStatus.errorMsg = data.error;
        } else {
          // Route to new component
        }
      },
      error: (err) => {
        console.log(err);
        this.loadStatus.isError = true;
        this.loadStatus.errorMsg = 'Something went wrong';
      },
      complete: () => {
        this.loadStatus.isLoaded = true;
      }
    };
  }

}
