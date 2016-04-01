import {Component, OnInit} from 'angular2/core';
import {HTTP_PROVIDERS} from 'angular2/http';
import {LocationService} from './location.service';
import {Country} from './country'
import {Region} from './region'

@Component({
  selector: 'location-chooser',
  template: `
  <div class="form-group">
    <label for="country">Pays*</label>
    <select class="form-control" id="country" name="country" (change)="updateRegions($event.target.value)">
      <option *ngFor="#country of countries" value="{{country.id}}">{{country.name}}</option>
    </select>
  </div>
  <div class="form-group" *ngIf="regions != undefined && regions.length > 0">
    <label for="region">Region*</label>
    <select class="form-control" id="region" name="region">
      <option *ngFor="#region of regions" value="{{region.id}}">{{region.name}}</option>
    </select>
  </div>
  `,
  providers: [
    HTTP_PROVIDERS,
    LocationService]
})
export class LocationChooserComponent implements OnInit {

  constructor(private _locationService: LocationService) {}

  errorMessage: string;
  countries: Country[];
  regions: Region[];

  ngOnInit() { this.getCountries(); }

  getCountries() {
    this._locationService.getCountries()
                         .subscribe(
                           countries => {
                             this.countries = countries;
                             this.updateRegions(this.countries[0].id)
                           },
                           error => this.errorMessage = <any>error
                         );
  }

  updateRegions(country_id: number) {
    this._locationService.getRegions(country_id)
                         .subscribe(
                           regions => this.regions = regions,
                           error => this.errorMessage = <any>error
                         );
  }
}
