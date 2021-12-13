import store from '@/store';

export interface WindowSize {
  heightPx: number;
  widthPx: number;
}

class WindowSizeService {

  constructor() {
    window.addEventListener('resize', this.resizeHandler)
  }

  _size: WindowSize = {
    heightPx: window.innerHeight,
    widthPx: window.innerWidth
  };

  resizeHandler(_: Event) {
    this._size = {
      heightPx: window.innerHeight,
      widthPx: window.innerWidth
    };
    store.commit('view/setWindowSize', this._size);
  }

  set size(size: WindowSize) {

    this._size = size;
  }

  get size(): WindowSize  {
    return this._size;
  }
}
/** Use 'new' here to create an instance, this instance is then what is exported
 *  This essentially makes the Service work as a Singleton when imported, since you are importing the instance */
export default new WindowSizeService();
