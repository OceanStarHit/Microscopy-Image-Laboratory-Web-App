import Vue from "vue";
import { tiffImage } from "../../utils/utils-func";
const noPreviewImage = require("../../assets/images/no-preview.png");

const namePatterns = {
  series: [-1, -1],
  row: [-1, -1],
  col: [-1, -1],
  field: [-1, -1],
  channel: [-1, -1],
  z: [-1, -1],
  time: [-1, -1]
};

const position = {
  namespaced: true,

  state: () => ({
    files: [],
    namePatterns: namePatterns,
    selects: {
      row: -1,
      col: -1,
      z: -1,
      timeline: -1,
      channels: [],
      objectLense: -1
    }
  }),
  getters: {
    getFiles: state => state.files,
    getNamePattern: state => state.namePatterns,
    getFilesAtRowCol: (state, getters) => {
      let targetRow = state.selects.row;
      let targetCol = state.selects.col;

      return state.files.filter(
        file =>
          file.metaData &&
          file.metaData.row == targetRow &&
          file.metaData.col == targetCol
      );
    },
    getFilesAtSelection: (state, getters) => {
      let rs = state.files.filter(file => {
        if (file.metaData) {
          let ck =
            file.metaData.row == state.selects.row &&
            file.metaData.col == state.selects.col &&
            file.metaData.z == state.selects.z &&
            file.metaData.timeline == state.selects.timeline &&
            file.metaData.objectLense == state.selects.objectLense &&
            state.selects.channels.includes(file.metaData.channel);
          return ck;
        }
        return false;
      });
      return rs;
    },
    getChannelOptions: (state, getters) => {
      var rs = [];
      for (let idx in state.files) {
        let f = state.files[idx];
        if (f.metaData) {
          rs.push(f.metaData.channel);
        }
      }
      return [...new Set(rs)];

      // switch (rs.length) {
      //   case 1:
      //     return ["S"];
      //   case 2:
      //     return ["S", "B"];
      //   default:
      //     return ["B", "G", "R"];
      // }
    }
  },
  actions: {
    setFiles({ commit }, files) {
      commit("clearFiles");

      files.forEach(function(file, index) {
        commit("addFile", file);
        const reader = new FileReader();
        reader.onload = function() {
          let imageData = reader.result;

          if (
            file.type.startsWith("image/tif") ||
            file.type.startsWith("image/tiff")
          ) {
            try {
              imageData = tiffImage(reader.result.substring(23));
            } catch (err) {
              console.error(err);
            }
          }

          if (imageData.startsWith("data:image")) {
            commit("addImageData", { index, imageData });
          }
        };
        reader.readAsDataURL(file);
      });
    },
    clearFiles({ commit }) {
      commit("clearFiles");
    },
    addFile({ commit, state }, file) {
      commit("addFile", file);

      const index = state.files.length - 1;

      const reader = new FileReader();
      reader.onload = function() {
        let imageData = reader.result;

        if (
          file.type.startsWith("image/tif") ||
          file.type.startsWith("image/tiff")
        ) {
          try {
            imageData = tiffImage(reader.result.substring(23));
          } catch (err) {
            console.error(err);
          }
        }

        if (imageData.startsWith("data:image")) {
          commit("addImageData", { index, imageData });
        }
      };
      reader.readAsDataURL(file);
    },
    addMetaData({ commit, state }, payload) {
      commit("addMetaData", {
        index: payload.index,
        metaData: payload.metaData
      });
    },
    setNamePattern({ commit }, keyPos) {
      commit("setNamePattern", keyPos);
    },
    changeSelectsByRowCol({ commit, state }, payload) {
      if (
        state.selects.row != payload.row ||
        state.selects.col != payload.col
      ) {
        changeSelects(commit, state, payload);
      }
    },
    changeSelectsByChannels({ commit, state }, payload) {
      changeSelects(commit, state, {
        channels: payload
      });
    },
    changeSelectsByObjectLense({ commit, state }, payload) {
      if (state.selects.objectLense != payload) {
        changeSelects(commit, state, {
          objectLense: payload
        });
      }
    },
    changeSelectsByZ({ commit, state }, payload) {
      if (state.selects.z != payload) {
        changeSelects(commit, state, {
          z: payload
        });
      }
    },
    changeSelectsByTimeline({ commit, state }, payload) {
      if (state.selects.timeline != payload) {
        changeSelects(commit, state, {
          timeline: payload
        });
      }
    }
  },
  mutations: {
    clearFiles(state) {
      state.files.splice(0, state.files.length);
    },
    addFile(state, file) {
      state.files.push({
        name: file.name,
        type: file.type,
        size: file.size,
        lastModified: file.lastModified,
        lastModifiedDate: file.lastModifiedDate,
        imageData: noPreviewImage
      });
    },
    addImageData(state, payload) {
      Vue.set(state.files[payload.index], "imageData", payload.imageData);
    },
    addMetaData(state, payload) {
      Vue.set(state.files[payload.index], "metaData", payload.metaData);
    },
    setNamePattern(state, keyValue) {
      state.namePatterns[keyValue["key"]] = keyValue["pos"];
    },

    changeSelects(state, payload) {
      state.selects = Object.assign({}, state.selects, {
        row: payload.row,
        col: payload.col,
        z: payload.z,
        timeline: payload.timeline,
        channels: payload.channels,
        objectLense: payload.objectLense
      });
    }
  }
};

const defaultPattern = /^(\w+)[_\s](\w+_\w+)_(\w\d{2})_(\d)_(\w)(\d{2})(\w\d{2})(\w\d)\.(\w+)$/;

export function getSeries(filename) {
  const s = namePatterns.series[0];
  const e = namePatterns.series[1];
  const tokens = filename.match(defaultPattern);

  var seris = "name";
  if (s >= 0 && e >= 0 && e > s) {
    seris = filename.substring(s, e);
  } else if (tokens) {
    seris = tokens[3];
  }

  return seris;
}

export function getChannel(filename) {
  const s = namePatterns.channel[0];
  const e = namePatterns.channel[1];

  const tokens = filename.match(defaultPattern);
  var c = "0";
  if (s >= 0 && e >= 0 && e > s) {
    c = filename.substring(s, e);
  } else if (tokens) {
    c = tokens[3];
  }

  return parseInt(c.replace(/\D/g, ""));
}

export function getPosition(filename) {
  const patternRowStart = namePatterns.row[0];
  const patternRowEnd = namePatterns.row[1];
  const patternColStart = namePatterns.col[0];
  const patternColEnd = namePatterns.col[1];

  const patternZStart = namePatterns.z[0];
  const patternZEnd = namePatterns.z[1];

  const timelineStart = namePatterns.time[0];
  const timelineEnd = namePatterns.time[1];

  const channelStart = namePatterns.channel[0];
  const channelEnd = namePatterns.channel[1];

  const type = filename.match(defaultPattern);

  var r = 0;
  if (
    patternRowStart >= 0 &&
    patternRowEnd >= 0 &&
    patternRowEnd > patternRowStart
  ) {
    r = filename.substring(patternRowStart, patternRowEnd);
    r = r.charCodeAt(0) - "A".charCodeAt(0) + 1;
  } else if (type) {
    r = type[5].charCodeAt(0) - "A".charCodeAt(0) + 1;
  }

  var c = 0;
  if (
    patternColStart >= 0 &&
    patternColEnd >= 0 &&
    patternColEnd > patternColStart
  ) {
    c = parseInt(filename.substring(patternColStart, patternColEnd));
  } else if (type) {
    c = parseInt(type[6]);
  }

  var z = 0;
  if (patternZStart >= 0 && patternZEnd >= 0 && patternZEnd > patternZStart) {
    z = parseInt(filename.substring(patternZStart, patternZEnd));
  } else if (type) {
    z = parseInt(type[4]);
  }

  var t = 0;
  if (timelineStart >= 0 && timelineEnd >= 0 && timelineEnd > timelineStart) {
    let tls = filename.substring(timelineStart, timelineEnd);
    tls = tls.replace(/\D/g, "");

    t = parseInt(tls);
  } else if (type) {
    t = parseInt(type[3]);
  }

  var channel = "";
  if (channelStart >= 0 && channelEnd >= 0 && channelEnd > channelStart) {
    channel = filename.substring(channelStart, channelEnd);
    channel = parseInt(channel.replace(/\D/g, ""));
    // d01 is linked to B, d02 is linked to G, and d03 is linked to R. 
    switch (channel) {
      case 1:
        channel = "B";
        break;
      case 2:
        channel = "G";
        break;
      default:
        channel = "R";
    }
  }

  return [r, c, z, t, channel];
}

export default {
  namespaced: true,
  modules: {
    position
  }
};

function changeSelects(commit, state, params) {
  let newSelects = Object.assign({}, state.selects, {});
  if (typeof params.z !== "undefined") {
    newSelects.z = params.z;
  }
  if (typeof params.row !== "undefined") {
    newSelects.row = params.row;
  }
  if (typeof params.col !== "undefined") {
    newSelects.col = params.col;
  }
  if (typeof params.timeline !== "undefined") {
    newSelects.timeline = params.timeline;
  }
  if (typeof params.channels !== "undefined") {
    newSelects.channels = params.channels;
  }
  if (typeof params.objectLense !== "undefined") {
    newSelects.objectLense = params.objectLense;
  }

  commit("changeSelects", newSelects);
}
