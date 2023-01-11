import { HttpClient } from '@angular/common/http';
import { AfterViewInit, Component } from '@angular/core';
import * as L from 'leaflet';

import { forkJoin } from 'rxjs';

const iconRetinaUrl = 'assets/marker-icon-2x.png';
const iconUrl = 'assets/marker-icon.png';
const shadowUrl = 'assets/marker-shadow.png';
export const iconDefault = L.icon({
  iconRetinaUrl,
  iconUrl,
  shadowUrl,
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  tooltipAnchor: [16, -28],
  shadowSize: [41, 41]
});
L.Marker.prototype.options.icon = iconDefault;
export interface Player {
  position: string,
  dob_string: string,
  name: string,
  birthplace: string,
  country: string,
  wiki_page: string
}

export interface LatLong {
  lat: number,
  lon: number
}

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements AfterViewInit {
  private map: any;

  private initMap(): void {
    this.map = L.map('map', {
      center: [ 39.8282, -98.5795 ],
      zoom: 3
    });

    const tiles = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 18,
      minZoom: 3,
      attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    });

    tiles.addTo(this.map);

    this.players.forEach(p => {
      if (p.birthplace in this.hometowns) {
        const flagIcon = L.icon({
          iconUrl: encodeURI(`assets/flags/${p.country}.png`),
          iconSize: [12, 12],
        });
        const marker = new L.Marker([this.hometowns[p.birthplace].lat, this.hometowns[p.birthplace].lon], {icon: flagIcon});
        let markerStr = '';
        Object.keys(p).forEach(key => {
          let value = (p as any)[key];
          if (key === 'wiki_page') {
            value = `<a href=${value} target="_blank">${value}</a>`
          }
          markerStr += `${key}: ${value}<br>`
        })
        marker.bindPopup(markerStr);
        marker.addTo(this.map);
      } else {
        console.error('need to lookup info for', p);
      }
    })
  }


   ngAfterViewInit(): void {
    forkJoin(
      [
        this.http.get('assets/players.json'),
        this.http.get('assets/hometowns.json')
      ]
    )
    .subscribe(resp => {
      this.players = resp[0] as any;
      this.hometowns = resp[1] as any;
      this.initMap();

    });
  }


  title = 'world-cup-players'
  players: Array<Player> = [];
  hometowns: Record<string, LatLong> = {};
  constructor(private http: HttpClient) {
  }
}
