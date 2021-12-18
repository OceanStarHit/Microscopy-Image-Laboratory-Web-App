export const VESSEL_TYPES: string[] = ['Slide', 'WellPlate', 'Dish', 'Wafer'];

export interface VesselBaseModel {
  id: number;
  title: string;
  type: string;
}

export interface VesselSlideModel extends VesselBaseModel {
  count: number;
}

export interface VesselWellPlateModel extends VesselBaseModel {
  rowCount: number;
  columnCount: number;
  isShowName: boolean;
}

export interface VesselDishModel extends VesselBaseModel {
  size: number;
}

export interface VesselWaferModel extends VesselBaseModel {
  size: number;
}

export const VESSEL_SLIDES: VesselSlideModel[] = [
  { id: 1, type: 'Slide', count: 1, title: 'Single' },
  { id: 2, type: 'Slide', count: 2, title: 'Double' },
  { id: 3, type: 'Slide', count: 4, title: 'Quarter' }
]

export const VESSEL_WELLPLATES: VesselWellPlateModel[] = [
  { id: 4, type: 'WellPlate', rowCount: 2, columnCount: 3, title: '6', isShowName: false },
  { id: 5, type: 'WellPlate', rowCount: 3, columnCount: 4, title: '12', isShowName: true },
  { id: 6, type: 'WellPlate', rowCount: 4, columnCount: 6, title: '24', isShowName: true },
  { id: 7, type: 'WellPlate', rowCount: 6, columnCount: 8, title: '48', isShowName: true },
  { id: 8, type: 'WellPlate', rowCount: 8, columnCount: 12, title: '96', isShowName: true },
  { id: 9, type: 'WellPlate', rowCount: 16, columnCount: 24, title: '384', isShowName: true }
]

export const VESSEL_DISHES: VesselDishModel[] = [
  { id: 10, type: 'Dish', size: 35, title: '35' },
  { id: 11, type: 'Dish', size: 60, title: '60' },
  { id: 12, type: 'Dish', size: 100, title: '100' }
]

export const VESSEL_WAFERS: VesselWaferModel[] = [
  { id: 13, type: 'Wafer', size: 150, title: '150 (6inch)' },
  { id: 14, type: 'Wafer', size: 200, title: '200 (8inch)' },
  { id: 15, type: 'Wafer', size: 300, title: '300 (12inch)' }
]

export const VESSELS: VesselBaseModel[][] = [
    VESSEL_SLIDES,
    VESSEL_WELLPLATES,
    VESSEL_DISHES,
    VESSEL_WAFERS
]

export function getVesselById(id: number): VesselBaseModel | null {
  for (const vessel of VESSELS) {
    for (const one of vessel) {
      if (one.id === id) {
        return one;
      }
    }
  }

  return null;
}
