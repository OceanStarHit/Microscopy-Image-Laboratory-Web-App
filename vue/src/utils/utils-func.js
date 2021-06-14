import tiff from "tiff.js";
import atob from "atob";
import { FILE_TYPES } from "./file-types";

const getFileExtension = filename => {
  const regex = /(?:\.([^.]+))?$/;

  let extension = regex.exec(filename)[1];

  return extension ? "." + extension : "";
};

const checkFileType = filename => {
  const extension = getFileExtension(filename);

  return FILE_TYPES.includes(extension.toLowerCase());
};

const base64ToArrayBuffer = base64 => {
  var binary_string = atob(base64);
  var len = binary_string.length;
  var bytes = new Uint8Array(len);
  for (var i = 0; i < len; i++) {
    bytes[i] = binary_string.charCodeAt(i);
  }
  return bytes.buffer;
};

const tiffImage = base64 => {
  const buffer = base64ToArrayBuffer(base64);
  const tiff_data = new tiff({ buffer });

  return tiff_data.toDataURL();
};

export { checkFileType, tiffImage };
