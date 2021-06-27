import tiff from "tiff.js";
import atob from "atob";
import { FILE_TYPES } from "./file-types";

const getFileName = fname => {
  const regex = /(.*)\.[^\.]+/g;/* eslint-disable-line */
  let filename = regex.exec(fname);

  return filename ? filename[1] : "";
};

const getFileExtension = filename => {
  const regex = /(?:\.([^.]+))?$/;
  let extension = regex.exec(filename);

  return extension ? "." + extension[1] : "";
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

const isOverlapped = (a, b) => {
  console.log(a, b);
  return Math.max(a[1], b[1]) - Math.min(a[0], b[0]) < (a[1] - a[0]) + (b[1] - b[0]);
}

export {
  getFileName,
  getFileExtension,
  checkFileType,
  tiffImage,
  isOverlapped
};
