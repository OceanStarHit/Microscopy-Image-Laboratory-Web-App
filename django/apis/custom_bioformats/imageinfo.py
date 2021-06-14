import os.path
import javabridge

_jars_dir = os.path.join(os.path.dirname(__file__), 'jars')

JAR_VERSION = '6.6.0'

# Using bioformats_package.jar for version 6.6.0
JARS = [os.path.realpath(os.path.join(_jars_dir, name + '.jar'))
        for name in ['bioformats_package_660']]

from . import formatreader as _formatreader

# import cv2
import numpy as np

from traceback import print_exc

from . import utils

class ImageInfo(object):
    def __init__(self, path, heap_size=4):
        self.path = path
        self.filename = os.path.basename(self.path)
        self.heap_size = heap_size # GB

        javabridge.start_vm(class_path=javabridge.JARS + JARS,run_headless=True,max_heap_size=f'{self.heap_size}G')
        javabridge.attach()

        DebugTools = javabridge.JClassWrapper("loci.common.DebugTools")
        DebugTools.setRootLevel("OFF")

        self.rdr = _formatreader.ImageReader(self.path, perform_init=True)
        self.reader = self.rdr.rdr
        self.J = javabridge.JWrapper(self.reader.getMetadataStore())

        self.ids = []
        self.datas = []

    def close(self):
        self.reader.close()
        self.rdr.close()

        javabridge.attach()

    def parse_by_bioformat(self, show_log=True):
        try:
            if show_log:
                print('\n\n***************************************')
                print(f'===== File Name : {self.filename} =====')

            self.core_metadata = self.parse_core_metadata(self.reader, show_log)
            self.origin_metadata = self.parse_origin_metadata(self.reader, show_log)

            self.well_samples = []

            self.plates = self.parse_plate_data(self.J, show_log)
            self.instruments = self.parse_instrument_data(self.J, show_log)

            if show_log:
                print('===== Well Samples =====')
                print(self.well_samples)
            
            # self.images = self.parse_image_data(rdr, J, show_log)

            result = True
        except Exception:
            print_exc()
            result = False

        return result

    def image_by_id(self, image_id):
        self.image_id = image_id
        self.core_metadata = self.parse_core_metadata(self.reader, show_log=False, series=image_id)
        self.image = self.parse_image_data_by_series(image_id, self.rdr, self.J, show_log=False)

    def make_response_file_header(self):
        file_header = {}
        file_header['originMetadata'] = self.origin_metadata
        file_header['plates'] = self.plates
        file_header['wellSamples'] = self.well_samples

        return file_header

    def make_response_image_header(self):
        plate_id = well_id = position_x = position_y = -1

        for well_samples in self.well_samples:
            if well_samples['imageId'] == self.image_id:
                plate_id = well_samples['plateId']
                well_id = well_samples['wellId']
                position_x = well_samples['positionX']
                position_y = well_samples['positionY']
                break

        image_header = {'imageId': self.image_id, 'plateId': plate_id, 'wellId': well_id}
        image_header['positionX'] = position_x
        image_header['positionY'] = position_y
        image_header['coreMetadata'] = self.core_metadata
        image_header['imageInfo'] = self.image['info']

        return image_header

    def make_response_data(self, hearder={}, t=0, z=0, c=0):
        response = hearder.copy()

        try:
            image_array = self.image['image5d0'][t, z, c, ...]
            scale = self.image['scales'][t, z, c]
            channel = self.image['info']['channels'][c]
            
            image_tzc = utils.save_image(image_array, scale, channel)

            response['imageData'] = utils.make_image_data(image_tzc)

        except Exception:
            print_exc()
            pass
        
        response['parameters'] = {'T': 0, 'Z': 0, 'C': 0}
        
        return response

    def get_first_image(self):
        if len(self.well_samples) > 0:
            first_well_sample = self.well_samples[0]

            image_id = first_well_sample['imageId']            
        else:
            image_id = 0

        self.image_by_id(image_id)

        self.ids.append(image_id)
        self.datas.append(self.image)

        file_header = self.make_response_file_header()
        image_header = self.make_response_image_header()

        header = file_header.copy()
        header.update(image_header)

        return self.make_response_data(header)

    def change_image(self, image_id):
        if self.image_id != image_id:
            try:
                idx = self.ids.index(image_id)
                self.image_id = image_id
                self.image = self.datas[idx]
            except Exception:
                self.image_by_id(image_id)

        image_header = self.make_response_image_header()

        return self.make_response_data(image_header)

    def change_tzc(self, t, z, c):
        return self.make_response_data(t=t, z=z, c=c)

    def parse_core_metadata(self, reader, show_log, series=0):
        try:
            series_count = reader.getSeriesCount()
            image_count = reader.getImageCount()
            
            series = reader.setSeries(series)

            series = reader.getSeries()
            size_x = reader.getSizeX()
            size_y = reader.getSizeY()
            size_z = reader.getSizeZ()
            size_t = reader.getSizeT()
            size_c = reader.getSizeC()
            effective_size_c = reader.getEffectiveSizeC()
            rgb_channel_count = reader.getRGBChannelCount()
            dimension_order = reader.getDimensionOrder()
            is_rgb = reader.isRGB()
            is_little_endian = reader.isLittleEndian()
            is_interleaved = reader.isInterleaved()
            pixel_type = reader.getPixelType()
            bits_per_pixel = reader.getBitsPerPixel()
            
            core_metadata={'seriesCount': series_count, 'imageCount': image_count, 'currentSeries': series}
            core_metadata['sizeX'] = size_x
            core_metadata['sizeY'] = size_y
            core_metadata['sizeC'] = size_c
            core_metadata['effectiveSizeC'] = effective_size_c
            core_metadata['sizeZ'] = size_z
            core_metadata['sizeT'] = size_t
            core_metadata['pixelType'] = pixel_type
            core_metadata['bitsPerPixel'] = bits_per_pixel
            core_metadata['rgbChannelCount'] = rgb_channel_count
            core_metadata['dimensionOrder'] = dimension_order
            core_metadata['isRGB'] = is_rgb
            core_metadata['isLittleEndian'] = is_little_endian
            core_metadata['isInterleaved'] = is_interleaved
        except Exception:
            core_metadata = {}
        finally:
            if show_log: 
                print('===== Core Metadata =====')
                print(core_metadata)

        return core_metadata

    def parse_origin_metadata(self, reader, show_log):
        try:
            origin_metadata = javabridge.jutil.jdictionary_to_string_dictionary(reader.getMetadata())
        except Exception:
            origin_metadata = {}
        finally:
            # if show_log: 
            #     print('===== Origin Metadata =====')
            #     print(origin_metadata)
            pass

        
        return origin_metadata

    def parse_plate_data(self, J, show_log):
        plate_data = []

        plate_count = J.getPlateCount()
        if plate_count > 0:
            for plate_index in range(plate_count):                
                try:
                    id = self.j2py_value(J.getPlateID(plate_index))
                except Exception:
                    id = ''

                try:
                    name = self.j2py_value(J.getPlateName(plate_index))
                except Exception:
                    name = ''

                try:
                    description = self.j2py_value(J.getPlateDescription(plate_index))
                except Exception:
                    description = ''

                try:
                    external_identifier = self.j2py_value(J.getPlateExternalIdentifier(plate_index))
                except Exception:
                    external_identifier = ''
                
                try:
                    status = self.j2py_value(J.getPlateStatus(plate_index))
                except Exception:
                    status = ''

                try:
                    row_naming_convention = self.j2py_value(J.getPlateRowNamingConvention(plate_index).toString())
                except Exception:
                    row_naming_convention = 'letter'

                try:
                    rows = self.j2py_value(J.getPlateRows(plate_index).getValue(), int)
                except Exception:
                    rows = 0

                try:
                    column_naming_convention = self.j2py_value(J.getPlateColumnNamingConvention(plate_index).toString())
                except Exception:
                    column_naming_convention = 'number'

                try:
                    columns = self.j2py_value(J.getPlateColumns(plate_index).getValue(), int)
                except Exception:
                    columns = 0

                _wells, _rows, _columns, _well_samples = self.parse_well_data(J, plate_index)
                
                _plate = {'id': id, 'name': name, 'description': description}
                _plate['externalIdentifier'] = external_identifier
                _plate['status'] = status
                _plate['rowNamingConvention'] = row_naming_convention
                _plate['rows'] = rows if rows > _rows else _rows
                _plate['columnNamingConvention'] = column_naming_convention
                _plate['columns'] = columns if columns > _columns else _columns
                
                _plate['wells'] = _wells
                _plate['well_samples'] = _well_samples

                plate_data.append(_plate)

        if show_log:
            print('===== Plates =====')
            print(plate_data)

        return plate_data

    def parse_well_data(self, J, plate_index):
        well_data = []
        well_sample_data = []
        rows = columns = -1

        well_count = J.getWellCount(plate_index)
        if well_count > 0:
            for well_index in range(well_count):
                try:
                    id = self.j2py_value(J.getWellID(plate_index, well_index))
                except Exception:
                    id = ''
                
                try:
                    external_description = self.j2py_value(J.getWellExternalDescription(plate_index, well_index))
                except Exception:
                    external_description = ''
                
                try:
                    external_identifier = self.j2py_value(J.getWellExternalIdentifier(plate_index, well_index))
                except Exception:
                    external_identifier = ''

                try:
                    row = self.j2py_value(J.getWellRow(plate_index, well_index).getValue(), int)
                except Exception:
                    row = -1
                
                try:
                    column = self.j2py_value(J.getWellColumn(plate_index, well_index).getValue(), int)
                except Exception:
                    column = -1

                type = self.j2py_value(J.getWellType(plate_index, well_index))
                
                try:
                    color_r = self.j2py_value(J.getWellColor(plate_index, well_index).getRed(), int)
                    color_g = self.j2py_value(J.getWellColor(plate_index, well_index).getGreen(), int)
                    color_b = self.j2py_value(J.getWellColor(plate_index, well_index).getBlue(), int)
                except Exception:
                    color_r = color_g = color_b = 0

                _well = {'id': id}
                _well['externalDescription'] = external_description
                _well['externalIdentifier'] = external_identifier
                _well['row'] = row
                _well['column'] = column
                _well['type'] = type
                _well['color'] = {'r': color_r, 'g': color_g, 'b': color_b}
                _well['wellSamples'] = self.parse_well_sample_data(J, plate_index, well_index)

                if rows < row: rows = row
                if columns < column: columns = column

                well_data.append(_well)

                well_sample_data.append(_well['wellSamples'])

        return well_data, rows + 1, columns + 1, well_sample_data

    def parse_well_sample_data(self, J, plate_index, well_index):
        well_sample_data = []

        well_sample_count = J.getWellSampleCount(plate_index, well_index)
        if well_sample_count > 0:
            for well_sample_index in range(well_sample_count):
                try:
                    index = self.j2py_value(J.getWellSampleIndex(plate_index, well_index, well_sample_index).getValue(), int)
                except Exception:
                    index = -1

                try:
                    id = self.j2py_value(J.getWellSampleID(plate_index, well_index, well_sample_index))
                except Exception:
                    id = ''
                
                try:
                    position_x = self.j2py_value(J.getWellSamplePositionX(plate_index, well_index, well_sample_index).floatValue(), float)
                except Exception:
                    position_x = 0.
                
                try:
                    position_y = self.j2py_value(J.getWellSamplePositionY(plate_index, well_index, well_sample_index).floatValue(), float)
                except Exception:
                    position_y = 0.

                try:
                    image_ref = self.j2py_value(J.getWellSampleImageRef(plate_index, well_index, well_sample_index))
                except Exception:
                    image_ref = ''

                image_id = self.index_from_id(image_ref)
                
                _well_sample = {'index': index, 'id': id}
                _well_sample['imageId'] = image_id
                _well_sample['positionX'] = position_x
                _well_sample['positionY'] = position_y
                _well_sample['plateId'] = plate_index
                _well_sample['wellId'] = well_index
                
                well_sample_data.append(_well_sample)

                self.well_samples.append(_well_sample)
        
        return well_sample_data

    def parse_instrument_data(self, J, show_log):
        instrument_data = []

        instrument_count = J.getInstrumentCount()
        if instrument_count > 0:
            for instrument_index in range(instrument_count):
                try:
                    id = self.j2py_value(J.getInstrumentID(instrument_index))
                except Exception:
                    id = ''

                try:
                    microscope_model = self.j2py_value(J.getMicroscopeModel(instrument_index))
                except Exception:
                    microscope_model = ''

                try:
                    microscope_manufacturer = self.j2py_value(J.getMicroscopeManufacturer(instrument_index))
                except Exception:
                    microscope_manufacturer = ''

                try:
                    microscope_serial_number = self.j2py_value(J.getMicroscopeSerialNumber(instrument_index))
                except Exception:
                    microscope_serial_number = ''

                try:
                    microscope_lot_number = self.j2py_value(J.getMicroscopeLotNumber(instrument_index))
                except Exception:
                    microscope_lot_number = ''

                try:
                    microscope_type = self.j2py_value(J.getMicroscopeType(instrument_index).toString())
                except Exception:
                    microscope_type = ''

                _instrument = {'id': id}
                _instrument['microscopeModel'] = microscope_model
                _instrument['microscopeManufacturer'] = microscope_manufacturer
                _instrument['microscopeSerialNumber'] = microscope_serial_number
                _instrument['microscopeLotNumber'] = microscope_lot_number
                _instrument['microscopeType'] = microscope_type

                _instrument['objectives'] = self.parse_objective_data(J, instrument_index)

                instrument_data.append(_instrument)

        if show_log:
            print('===== Instruments =====')
            print(instrument_data)

        return instrument_data

    def parse_objective_data(self, J, instrument_index):
        objective_data = []

        objective_count = J.getObjectiveCount(instrument_index)
        if objective_count > 0:
            for objective_index in range(objective_count):
                try:
                    id = self.j2py_value(J.getObjectiveID(instrument_index, objective_index))
                except Exception:
                    id = ''

                try:
                    model = self.j2py_value(J.getObjectiveModel(instrument_index, objective_index))
                except Exception:
                    model = ''

                try:
                    manufacturer = self.j2py_value(J.getObjectiveManufacturer(instrument_index, objective_index))
                except Exception:
                    manufacturer = ''

                try:
                    serial_number = self.j2py_value(J.getObjectiveSerialNumber(instrument_index, objective_index))
                except Exception:
                    serial_number = ''

                try:
                    lot_number = self.j2py_value(J.getObjectiveLotNumber(instrument_index, objective_index))
                except Exception:
                    lot_number = ''

                try:
                    correction = self.j2py_value(J.getObjectiveCorrection(instrument_index, objective_index).toString())
                except Exception:
                    correction = ''

                try:
                    immersion = self.j2py_value(J.getObjectiveImmersion(instrument_index, objective_index).toString())
                except Exception:
                    immersion = ''

                try:
                    iris = self.j2py_value(J.getObjectiveIris(instrument_index, objective_index).booleanValue(), bool)
                except Exception:
                    iris = ''

                try:
                    lens_na = self.j2py_value(J.getObjectiveLensNA(instrument_index, objective_index).floatValue(), float)
                except Exception:
                    lens_na = 0.
                
                try:
                    nominal_magnification = self.j2py_value(J.getObjectiveNominalMagnification(instrument_index, objective_index).floatValue(), float)
                except Exception:
                    nominal_magnification = 0.
                
                try:
                    calibrated_magnification = self.j2py_value(J.getObjectiveCalibratedMagnification(instrument_index, objective_index).floatValue(), float)
                except Exception:
                    calibrated_magnification = 0.
                
                try:
                    working_distance = self.j2py_value(J.getObjectiveWorkingDistance(instrument_index, objective_index).floatValue(), float)
                except Exception:
                    working_distance = 0.
                
                _objective = {'id': id, 'model': model, 'manufacturer': manufacturer, 'serialNumber': serial_number, 'lotNumber': lot_number}
                _objective['correction'] = correction
                _objective['immersion'] = immersion
                _objective['iris'] = iris
                _objective['lensNA'] = lens_na
                _objective['nominalMagnification'] = nominal_magnification
                _objective['calibratedMagnification'] = calibrated_magnification
                _objective['workingDistance'] = working_distance
                
                objective_data.append(_objective)

        return objective_data

    def parse_image_data(self, show_log):
        image_data = []

        image_count = self.J.getImageCount()
        if image_count > 0:
            for image_index in range(image_count):
                _image = self.parse_image_data_by_series(image_index, self.rdr, self.J, show_log)
                image_data.append(_image)

        if show_log:
            print('===== Images =====')
            print(image_data)

        return image_data
        
    def parse_image_data_by_series(self, series=0, rdr=None, J=None, show_log=True):
        image_index = series
        if rdr is None: rdr = self.rdr
        if J is None: J = self.J

        try:
            id = self.j2py_value(J.getImageID(image_index))
        except Exception:
            id = ''

        try:
            name = self.j2py_value(J.getImageName(image_index))
        except Exception:
            name = ''

        try:
            description = self.j2py_value(J.getImageDescription(image_index))
        except Exception:
            description = ''
        
        try:
            acquisition_date = self.j2py_value(J.getImageAcquisitionDate(image_index).toString())
        except Exception:
            acquisition_date = ''

        try:
            instrument_ref = self.j2py_value(J.getImageInstrumentRef(image_index))
        except Exception:
            instrument_ref = ''

        instrument_idx = self.index_from_id(instrument_ref)
        try:
            instrument = self.instruments[instrument_idx]
        except Exception:
            instrument = None

        try:
            objective_settings_id = self.j2py_value(J.getObjectiveSettingsID(image_index))
        except Exception:
            objective_settings_id = ''

        objective_idx = self.index_from_id(objective_settings_id)
        try:
            objectives = self.instruments[instrument_idx]['objectives']
            objective = objectives[objective_idx]
        except Exception:
            objective = None
        
        try:
            objective_settings_correction_collar = self.j2py_value(J.getObjectiveSettingsCorrectionCollar(image_index).floatValue(), float)
        except Exception:
            objective_settings_correction_collar = 0.

        try:
            objective_settings_medium = self.j2py_value(J.getObjectiveSettingsMedium(image_index).toString())
        except Exception:
            objective_settings_medium = ''

        try:
            objective_settings_refractive_index = self.j2py_value(J.getObjectiveSettingsRefractiveIndex(image_index).floatValue(), float)
        except Exception:
            objective_settings_refractive_index = 0.

        info = {'name': name, 'description': description}
        info['acquisitionDate'] = acquisition_date
        info['instrument'] = instrument
        info['objective'] = objective
        info['pixels'] = self.parse_pixels_data(J, image_index)
        info['channels'] = self.parse_channel_data(J, image_index)
        info['objectiveSettingsCorrectionCollar'] = objective_settings_correction_collar
        info['objectiveSettingsMedium'] = objective_settings_medium
        info['objectiveSettingsRefractiveIndex'] = objective_settings_refractive_index

        image_data = {'id': id, 'info': info}

        size_t = info['pixels']['sizeT']
        size_z = info['pixels']['sizeZ']
        size_c = self.core_metadata['effectiveSizeC']
        isRGB = self.core_metadata['isRGB']
        
        if not (size_t == 0 or size_z == 0 or size_c == 0):
            image000, scale000 = rdr.read(z=0, t=0, series=image_index, c=None if isRGB else 0,rescale=False, wants_max_intensity=True)
            _base_size = (size_t, size_z, size_c)
            _image_data_size = _base_size + image000.shape

            image5d0 = np.zeros(_image_data_size)
            scales = np.zeros(_base_size)

            for t in range(size_t):
                for z in range(size_z):
                    for c in range(1) if isRGB else range(size_c):
                        if t == 0 and z == 0 and c == 0:
                            image5d0[t, z, c] = image000
                            scales[t, z, c] = scale000
                        else:
                            image5d0[t, z, c], scales[t, z, c] = rdr.read(z=z, t=t, series=image_index, c=None if isRGB else c, rescale=False, wants_max_intensity=True)

            image_data['image5d0'] = image5d0
            image_data['scales'] = scales
        else:
            image_data['image5d0'] = None
            image_data['scales'] = None

        return image_data

    def parse_pixels_data(self, J, image_index):
        try:
            id = self.j2py_value(J.getPixelsID(image_index))
        except Exception:
            id = ''

        try:
            type = self.j2py_value(J.getPixelsType(image_index).toString())
        except Exception:
            type = ''

        try:
            size_z = self.j2py_value(J.getPixelsSizeZ(image_index).getValue(), int)
        except Exception:
            size_z = 0

        try:
            size_t = self.j2py_value(J.getPixelsSizeT(image_index).getValue(), int)
        except Exception:
            size_t = 0

        try:
            size_c = self.j2py_value(J.getPixelsSizeC(image_index).getValue(), int)
        except Exception:
            size_c = 0

        try:
            size_x = self.j2py_value(J.getPixelsSizeX(image_index).getValue(), int)
        except Exception:
            size_x = 0

        try:
            size_y = self.j2py_value(J.getPixelsSizeY(image_index).getValue(), int)
        except Exception:
            size_y = 0

        try:
            significant_bits = self.j2py_value(J.getPixelsSignificantBits(image_index).getValue(), int)
        except Exception:
            significant_bits = 0

        try:
            dimension_order = self.j2py_value(J.getPixelsDimensionOrder(image_index).toString())
        except Exception:
            dimension_order = ''

        try:
            interleaved = self.j2py_value(J.getPixelsInterleaved(image_index).booleanValue(), bool)
        except Exception:
            interleaved = None

        try:
            physical_size_x = self.j2py_value(J.getPixelsPhysicalSizeX(image_index).getValue(), float)
        except Exception:
            physical_size_x = 0.

        try:
            physical_size_y = self.j2py_value(J.getPixelsPhysicalSizeY(image_index).getValue(), float)
        except Exception:
            physical_size_y = 0.

        try:
            physical_size_z = self.j2py_value(J.getPixelsPhysicalSizeZ(image_index).getValue(), float)
        except Exception:
            physical_size_z = 0.
                
        _pixels = {'id': id}
        _pixels['type'] = type
        _pixels['sizeZ'] = size_z
        _pixels['sizeT'] = size_t
        _pixels['sizeC'] = size_c
        _pixels['sizeX'] = size_x
        _pixels['sizeY'] = size_y
        _pixels['significantBits'] = significant_bits
        _pixels['dimensionOrder'] = dimension_order
        _pixels['interleaved'] = interleaved
        _pixels['physicalSizeX'] = physical_size_x
        _pixels['physicalSizeY'] = physical_size_y
        _pixels['physicalSizeZ'] = physical_size_z

        return _pixels

    def parse_channel_data(self, J, image_index):
        channel_data = []

        try:
            channel_count = J.getChannelCount(image_index)
        except Exception:
            channel_count = 0

        if channel_count > 0:
            for channel_index in range(channel_count):
                try:
                    id = self.j2py_value(J.getChannelID(image_index, channel_index))
                except Exception:
                    id = ''

                idx = self.index_from_id(id)

                try:
                    name = self.j2py_value(J.getChannelName(image_index, channel_index))
                except Exception:
                    name = ''
                if name == '': name = f'Channel-{idx}'

                try:
                    dye = self.j2py_value(J.getChannelFluor(image_index, channel_index))
                except Exception:
                    dye = ''

                try:
                    emission_wavelength = self.j2py_value(J.getChannelEmissionWavelength(image_index, channel_index).getValue(), int)
                except Exception:
                    emission_wavelength = 0

                try:
                    excitation_wavelength = self.j2py_value(J.getChannelExcitationWavelength(image_index, channel_index).getValue(), int)
                except Exception:
                    excitation_wavelength = 0

                try:
                    samples_per_pixel = self.j2py_value(J.getChannelSamplesPerPixel(image_index, channel_index).getValue(), int)
                except Exception:
                    samples_per_pixel = 0

                try:
                    color_r = self.j2py_value(J.getChannelColor(image_index, channel_index).getRed(), int)
                    color_g = self.j2py_value(J.getChannelColor(image_index, channel_index).getGreen(), int)
                    color_b = self.j2py_value(J.getChannelColor(image_index, channel_index).getBlue(), int)
                except Exception:
                    color_r = color_g = color_b = 0

                try:
                    nd_filter = self.j2py_value(J.getChannelNDFilter(image_index).floatValue(), float)
                except Exception:
                    nd_filter = 0.

                try:
                    pinhole_size = self.j2py_value(J.getChannelPinholeSize(image_index).floatValue(), float)
                except Exception:
                    pinhole_size = 0.

                try:
                    pockel_cell_setting = self.j2py_value(J.getChannelPockelCellSetting(image_index, channel_index).intValue(), int)
                except Exception:
                    pockel_cell_setting = 0

                try:
                    illumination_type = self.j2py_value(J.getChannelIlluminationType(image_index, channel_index).toString())
                except Exception:
                    illumination_type = ''

                try:
                    contrast_method = self.j2py_value(J.getChannelContrastMethod(image_index, channel_index).toString())
                except Exception:
                    contrast_method = ''
                
                _channel = {'id': idx, 'name': name, 'dye': dye}
                _channel['emissionWavelength'] = emission_wavelength
                _channel['excitationWavelength'] = excitation_wavelength
                _channel['samplesPerPixel'] = samples_per_pixel
                _channel['color'] = {'r': color_r, 'g': color_g, 'b': color_b}
                _channel['ndFilter'] = nd_filter
                _channel['pinholeSize'] = pinhole_size
                _channel['pockelCellSetting'] = pockel_cell_setting
                _channel['illuminationType'] = illumination_type
                _channel['contrastMethod'] = contrast_method
                
                channel_data.append(_channel)

        return channel_data

    def j2py_value(self, j_value, dtype = str):
        try:
            if dtype is str:
                py_value  = str(j_value if j_value is not None else '')
            elif dtype is int:
                py_value  = int(j_value)
            elif dtype is bool:
                py_value  = bool(j_value)
            elif dtype is float:
                py_value  = float(j_value)
            else:
                py_value = j_value
        except Exception:
            if dtype is str:
                py_value  = ''
            elif dtype is int:
                py_value  = -1
            elif dtype is float:
                py_value  = 0.
            else:
                py_value = None
        finally:
            return py_value
    
    def index_from_id(self, id):
        if id != '':
            _tmp = id.split(':')
            index = int(_tmp[len(_tmp) - 1])
        else:
            index = -1

        return index

# """ Get OMEXML Metadata """
# try:
#     xml=bioformats.get_omexml_metadata(image_file)
#     print(xml)
    
#     # xml_normalized=unicodedata.normalize('NFKD', xml).encode('ascii','ignore')

#     # omeXMLObject=bioformats.OMEXML(xml_normalized)
#     # metaName = omeXMLObject.image().Name
# except Exception:
#     print_exc()
#     print('No metadata')
