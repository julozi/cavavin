import {bootstrap}    from 'angular2/platform/browser';
import {HTTP_PROVIDERS} from 'angular2/http';
import {LocationChooserComponent} from './location-chooser.component';
import 'rxjs/Rx';

bootstrap(LocationChooserComponent, [HTTP_PROVIDERS]);
