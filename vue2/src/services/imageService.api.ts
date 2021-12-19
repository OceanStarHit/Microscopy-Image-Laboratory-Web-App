import { apiClient } from '@/services/base.api';
import { AxiosResponse } from 'axios';

// export interface LoginModel {
//   email: string;
//   password: string;
//   otp: string | number;
// }

export interface ImageChannelModel {
    id: number;
    label: string;
    color: string;
    isActive: boolean;
}

export interface BaseTileApiModel {
    /** for deletion of tile */

    id: string;
    userId: string;
    absoluteBackendPath: string;
}

export interface TileApiModel extends BaseTileApiModel {
    /** Model of Tile as it exist from the Api */

    absoluteClientPath: string;
    absolutePath: string;
    fileName: string;
    contentType: string; // MIME
    widthPx: number;
    heightPx: number;

    offsetX?: number;
    offsetY?: number;

    rowIndex?: number;
    columnIndex?: number;
    zIndex?: number;
    timeIndex?: number;
    fieldIndex?: number;
    lensObjectiveM?: number;
    channel?: ImageChannelModel;
}


class ImageServiceApi {

    uploadTiles(files: File[], clearPrevious = false): Promise<AxiosResponse<TileApiModel[]>> {
        /**
         * Uploads the given files as tiles to the backend.
         * The backend reads the files and returns a TileApiModel without any of the alignment and metadata data set.
         * That will needs to be created separately.
         *
         * if clearPrevious is True, any previously set tiles for this user will be removed prior to adding these new
         * ones.
         */

        const formData = new FormData();  // must be form-data for files...multipart form
        for (const file in files) {
            console.log(file);
            formData.append('files', file);
        }

        formData.append('clearPrevious', clearPrevious ? 'True' : 'False');

        return apiClient.post('image/tile/upload_image_tiles', formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
        });
    }

    deleteTiles(tiles: BaseTileApiModel[]): Promise<AxiosResponse<any>> {
        /**
         * Deletes tiles
         *
         * argument tiles must contain the keys in BaseTileApiModel
         */

        /* remove unneeded keys to reduce size of request */
        const _tiles: BaseTileApiModel[] = tiles.map(tile => {
            return {
                id: tile.id,
                userId: tile.userId,
                absoluteBackendPath: tile.absoluteBackendPath
            }
        })

        return apiClient.post('image/tile/delete', _tiles, {
            headers: { 'Content-Type': 'multipart/form-data' }
        });
    }

}
/** Use 'new' here to create an instance, this instance is then what is exported
 *  This essentially makes the Service work as a Singleton when imported, since you are importing the instance */
export default new ImageServiceApi();
