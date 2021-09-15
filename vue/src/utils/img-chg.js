import tinycolor from "tinycolor2";

function median(arr) {
  arr = [...arr].sort((a, b) => a - b);
  return (arr[(arr.length - 1) >> 1] + arr[arr.length >> 1]) / 2;
}

const balanceLighting = imgData => {
  if (imgData.colorSpace == "srgb") {
    let hsvData = [];

    let brightnessTotal = 0;
    for (let pixPos = 0; pixPos < imgData.data.length; pixPos += 4) {
      let rgb = tinycolor({
        r: imgData.data[pixPos],
        g: imgData.data[pixPos + 1],
        b: imgData.data[pixPos + 2]
      });
      let hsv = rgb.toHsv();
      brightnessTotal += hsv.v;
      hsvData.push(hsv);
      // console.log("individual light: " + hsl.l);
    }

    if (hsvData.length == 0) return imgData;

    // let brightnesses = hsvData.map(item => item.v);
    // brightnesses.sort();
    // let threholdPos = parseInt(brightnesses.length * 0.8);
    // let threholdPos = parseInt(brightnesses.length * 0.7);
    // console.log("threholdPos: " + threholdPos);

    // let threhold = brightnesses[threholdPos];
    let threholdavg = brightnessTotal / hsvData.length;
    let threholdFix = 0.81;

    let thredhold = (threholdavg + threholdFix) / 2;

    if (threholdavg > threholdFix) {
      thredhold = threholdFix;
    }

    // console.log(brightnesses);
    // let lightValues = hsvData.map(item => item.v);
    // let medLights = median(lightValues);

    for (let idx in hsvData) {
      let hsv = hsvData[idx];
      if (hsv.v > thredhold) hsv.v = thredhold;

      let newRgb = tinycolor(hsv).toRgb();
      let toChangePox = idx * 4;
      imgData.data[toChangePox] = newRgb.r;
      imgData.data[toChangePox + 1] = newRgb.g;
      imgData.data[toChangePox + 2] = newRgb.b;
    }
  }

  return imgData;
};

const rgb2hsv = arr => {
  let rr;
  let gg;
  let bb;
  let r = arr[0] / 255;
  let g = arr[1] / 255;
  let b = arr[2] / 255;
  let h;
  let s;
  let v = Math.max(r, g, b);
  let diff = v - Math.min(r, g, b);
  let diffc = function(c) {
    return (v - c) / 6 / diff + 1 / 2;
  };

  if (diff === 0) {
    h = s = 0;
  } else {
    s = diff / v;
    rr = diffc(r);
    gg = diffc(g);
    bb = diffc(b);

    if (r === v) {
      h = bb - gg;
    } else if (g === v) {
      h = 1 / 3 + rr - bb;
    } else if (b === v) {
      h = 2 / 3 + gg - rr;
    }
    if (h < 0) {
      h += 1;
    } else if (h > 1) {
      h -= 1;
    }
  }
  return [Math.round(h * 360), Math.round(s * 100), Math.round(v * 100)];
};

const hsv2rgb = hsv => {
  let _l = hsv[0];
  let _m = hsv[1];
  let _n = hsv[2];
  let newR;
  let newG;
  let newB;
  if (_m === 0) {
    _l = _m = _n = Math.round((255 * _n) / 100);
    newR = _l;
    newG = _m;
    newB = _n;
  } else {
    _m = _m / 100;
    _n = _n / 100;
    let p = Math.floor(_l / 60) % 6;
    let f = _l / 60 - p;
    let a = _n * (1 - _m);
    let b = _n * (1 - _m * f);
    let c = _n * (1 - _m * (1 - f));
    switch (p) {
      case 0:
        newR = _n;
        newG = c;
        newB = a;
        break;
      case 1:
        newR = b;
        newG = _n;
        newB = a;
        break;
      case 2:
        newR = a;
        newG = _n;
        newB = c;
        break;
      case 3:
        newR = a;
        newG = b;
        newB = _n;
        break;
      case 4:
        newR = c;
        newG = a;
        newB = _n;
        break;
      case 5:
        newR = _n;
        newG = a;
        newB = b;
        break;
    }
    newR = Math.round(255 * newR);
    newG = Math.round(255 * newG);
    newB = Math.round(255 * newB);
  }
  return [newR, newG, newB];
};

const changeImageLuminance = (imgdata, value) => {
  const data = imgdata.data;
  for (let i = 0; i < data.length; i += 4) {
    const hsv = rgb2hsv([data[i], data[i + 1], data[i + 2]]);
    hsv[2] *= 1 + value;
    const rgb = hsv2rgb([...hsv]);
    data[i] = rgb[0];
    data[i + 1] = rgb[1];
    data[i + 2] = rgb[2];
  }
  return imgdata;
};

function getImgRow(imgPixcels, row, channel) {
  let startPox = imgPixcels.width * channel * row;
  let endPox = startPox + imgPixcels.width * channel;
  let theRow = imgPixcels.data.slice(startPox, endPox);

  let rs = [];
  for (let i = 0; i < imgPixcels.width; i++) {
    let pixValues = [];
    for (let j = 0; j < channel; j++) {
      pixValues.push(theRow[i * channel + j]);
    }
    rs.push(pixValues);
  }
  return rs;
}

function getImgColumn(imgPixcels, column, channel) {
  let rs = [];
  let startPox = column * channel;
  for (let lineNum = 0; lineNum < imgPixcels.height; lineNum++) {
    let pickPox = lineNum * imgPixcels.width * channel + startPox;

    let pixVals = [];
    for (let i = 0; i < channel; i++) {
      pixVals.push(imgPixcels.data[pickPox + i]);
    }
    rs.push(pixVals);
  }
  return rs;
}

/*
    Parameter Edge: 1 for top, 2 for right, 3 for bottom, 4 for left.
*/
const getImageEdge = (imgPixcels, edge, channel = 4, _width = 1) => {
  switch (edge) {
    case 1:
      return getImgRow(imgPixcels, 0, channel);
    case 2:
      return getImgColumn(imgPixcels, imgPixcels.width - 1, channel);
    case 3:
      return getImgRow(imgPixcels, imgPixcels.height - 1, channel);
    default:
      // assume the edge is 4
      return getImgColumn(imgPixcels, 0, channel);
  }
};

const imageAverageLuminance = imgdata => {
  const data = imgdata.data;
  let lum = 0;
  let lumCount = 0;
  for (let i = 0; i < data.length; i += 4) {
    const hsv = rgb2hsv([data[i], data[i + 1], data[i + 2]]);
    lum += hsv[2];
    lumCount++;
  }
  return lum / lumCount;
};

export {
  rgb2hsv,
  hsv2rgb,
  changeImageLuminance,
  imageAverageLuminance,
  getImageEdge,
  balanceLighting
};
