import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '@env/environment';
import { LoginStatus } from '@app/login-page/Classes/LoginStatus';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

const flaskUrl = environment.flaskApi;

@Injectable({
  providedIn: 'root'
})
export class LoginService {

  flaskUrl = flaskUrl;
  userName: string;
  isLoggedIn = false;

  constructor(
    private http: HttpClient
  ) { }

  public getLoginSession(userName: string) {
    const queryParams = '?name=' + userName;
    return this.http.get(this.flaskUrl + '/login' + queryParams);
  }

  public login(userName: string, password: string): Observable<LoginStatus> {
    return this.http.post<LoginStatus>(this.flaskUrl + '/login', {
      name: userName,
      password: password
    });
  }
}
