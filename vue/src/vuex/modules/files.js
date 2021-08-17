import Vue from "vue";
import { tiffImage } from "../../utils/utils-func";
const noPreviewImage = require("../../assets/images/no-preview.png");

const position = {
  namespaced: true,

  state: () => ({
    files: [],
    namePatterns: {
      'row': [-1, -1],
      'col': [-1, -1],
      'field': [-1, -1],
      'view': [-1, -1],
      'z': [-1, -1],
      'time': [-1, -1],
    },  
  }),
  getters: {
    getFiles: state => state.files,
    getNamePattern: state => state.namePatterns
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
    setNamePattern( { commit}, keyPos) {
      commit("setNamePattern", keyPos);
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
    setNamePattern(state, keyValue) {
      console.log("setNamePattern key:" + keyValue['key'] + " pos: " + keyValue['pos']);
      state.namePatterns[keyValue['key']] = keyValue["pos"];
    }  
  }
};

export default {
  namespaced: true,
  modules: {
    position
  }
};
