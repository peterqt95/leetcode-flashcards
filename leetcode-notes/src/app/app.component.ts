import { Component } from '@angular/core';
import { LoginService } from './services/login.service';
import { User } from './models/User';
import { Router } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'leetcode-notes';
  currentUser: User;

  constructor(
    private router: Router,
    private loginService: LoginService) {
      this.loginService.currentUser.subscribe(x => this.currentUser = x);
  }
}
