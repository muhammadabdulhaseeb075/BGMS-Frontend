import Overlay from 'ol/Overlay';
import store from '@/mapmanagement/store/index';

export default class MapMarker {

  private _id;
  private _index;
  private _name;
  private group;
  private _position;
  private positioning;
  private offset;
  private tooltip;
  private _template;
  private _label;
  private _message;
  private _class

  get position() {
    return this._position;
  }
  set position(position) {
    this._position = position;

    if (this._label)
      this._label.setPosition(position);
  }

  get message() {
    return this._message;
  }
  set message(message) {
    if (this._message !== message) {
      this._message = message;
      this.redrawMarker();
    }
  }

  get template() {
    return this._template;
  }

  get class() {
    return this._class;
  }
  set class(newClass) {
    this._class = newClass;
    this.redrawMarker();
  }

  get id() {
    return this._id;
  }

  get name() {
    return this._name;
  }
  set name(name) {
    this._name = name;
  }

  get index() {
    return this._index;
  }

  get label() {
    return this._label;
  }

  constructor(marker, markerIndex) {
    this._index = markerIndex;
    this._name = marker.name ? marker.name : 'marker';
    this._id = this._name + markerIndex.toString();

    this.group = marker.group;
    this._position = marker.position;
    this.positioning = marker.positioning;
    this.offset = marker.offset;
    this.tooltip = marker.tooltip;
    this._template = marker.template;
    this._class = marker.class;

    markerIndex += 1;
  }

  /**
   * For reasons I don't understand, changes to object of this class, are not reactive in Vue.
   */
  private redrawMarker() {
    const pos = store.getters.getMarkerPositionInStack('name', this.name);
    if(pos.length) {
      store.getters.getMarkers.splice(pos[0], 1);
      store.getters.getMarkers.push(this);
    }
  }

  public addMarkerToMap() {
    let element = document.getElementById(this.id);

    this._label = new Overlay({
      element: element,
      position: this._position,
      stopEvent: true
    });

    element.style.visibility = 'hidden';
    (window as any).OLMap.addOverlay(this._label);

    let positioning = this.positioning[0];
    let offset = this.offset[positioning];
    let oldPositioning = this.positioning[1];

    const LABELPOSITION = this.label.getPosition();

    if(element.parentElement.clientHeight>((window as any).OLMap.getPixelFromCoordinate(LABELPOSITION)[1]+offset[1])){
      oldPositioning = this.positioning[0];
      positioning = this.positioning[1];
      offset = this.offset[positioning];
    }

    if(this.tooltip){
      element.classList.remove(this.tooltip[oldPositioning]);
      element.classList.add(this.tooltip[positioning]);
    }

    this._label.setPositioning(positioning);
    this._label.setOffset(offset);
    element.style.visibility = 'visible';
  }

  public removeMarkerFromMap() {
    (window as any).OLMap.removeOverlay(this._label);
  }
}