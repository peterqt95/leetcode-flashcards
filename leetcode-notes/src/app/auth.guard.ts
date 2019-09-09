import { Injectable } from '@angular/core';
import { CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot, Router } from '@angular/router';
import { Observable } from 'rxjs';
import { LoginService } from './services/login.service';
import { map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class AuthGuard implements CanActivate {

  constructor(private loginSerivce: LoginService, private router: Router) {}

  canActivate(
    next: ActivatedRouteSnapshot,
    state: RouterStateSnapshot): Observable<boolean> | Promise<boolean> | boolean {
      const url: string = state.url;
      if (this.loginSerivce.isLoggedIn) {
        return true;
      } else {
        return this.sessionLoggedIn(this.loginSerivce.userName);
      }
  }

  private sessionLoggedIn(userName: string): Observable<boolean> {
    return this.loginSerivce.getLoginSession(userName).pipe(
      map( res => {
        if (res['status']) {
          this.loginSerivce.isLoggedIn = true;
          return true;
        }
      }, err => {
        this.router.navigate(['/login']);
        return false;
      })
    );
  }
}
