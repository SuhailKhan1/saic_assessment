import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  apihit:boolean = false;
  outputJson:any = null;
  constructor(private http: HttpClient){}

  fetchOutputJson(){
    this.apihit = true;
    this.http.get('https://0t9zlvh8fh.execute-api.ap-south-1.amazonaws.com/dev/face-comparison').subscribe((res:any) => {
      this.outputJson = res;
      this.apihit = false;
    },err => {
      console.error('Unable to retrive details');
    });
  }
}
