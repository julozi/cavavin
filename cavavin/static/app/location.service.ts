import {Injectable} from 'angular2/core'
import {Http, Response} from 'angular2/http'
import {Country} from './country'
import {Region} from './region'
import {Observable} from 'rxjs/Observable'

@Injectable()
export class LocationService {
  constructor(private http: Http) {}

  getCountries() {
    return this.http.get('/countries')
                    .map(res => <Country[]> res.json())
                    .catch(this.handleError);
    // var countries: Country[] = [
    //   {"id": 1, "name": "France"},
    //   {"id": 2, "name": "Italie"}
    // ];
    // return countries;
  }

  getRegions(countryId: number) {
    return this.http.get('/countries/'+countryId+'/regions')
                    .map(res => <Region[]> res.json())
                    .catch(this.handleError);
  }

  private handleError(error: Response) {
    console.error(error);
    return Observable.throw(error.json().error || 'Server error');
  }
}
