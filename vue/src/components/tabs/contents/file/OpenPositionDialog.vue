<template>
  <div style="display:none;">
    <input type="file" id="uploadFile" @change="requestUploadFile" />
    <v-dialog v-model="visibleDialog" max-width="980">
      <simple-dialog
        title="Position"
        :singleButton="false"
        :updateButton="true"
        :deleteButton="true"
        updateTitle="Update"
        deleteTitle="Delete"
        okTitle="Select"
        cancelTitle="Cancel"
        @update="onUpdate"
        @delete="onDelete"
        @select="onSelect"
        @close="onClose"
      >
        <v-tabs v-model="selectedTab" fixed-tabs>
          <v-tab href="#tabs-images" class="primary--text">Images</v-tab>
          <v-tab href="#tabs-tiling" class="primary--text">Tiling</v-tab>
          <v-tab href="#tabs-metadata" class="primary--text">Metadata</v-tab>
          <v-tab href="#tabs-name-type" class="primary--text"
            >Names &amp; Types</v-tab
          >
        </v-tabs>

        <v-tabs-items v-model="selectedTab" class="v-tab-item">
          <v-tab-item value="tabs-images">
            <v-sheet
              class="drop pa-5 v-sheet"
              height="350"
              :class="getClasses"
              @dragover.prevent="dragOver"
              @dragleave.prevent="dragLeave"
              @drop.prevent="drop($event)"
            >
              <div
                v-if="!imgFiles.length"
                class="d-flex align-center justify-center"
                style="height: 200px;"
              >
                <p class="text-h4 grey--text text--lighten-2">
                  Drag and Drop.
                </p>
              </div>
              <v-row v-else class="align-center justify-center">
                <div
                  class="img-align"
                  v-for="(imgFile, idx) in imgFiles"
                  :key="idx"
                  @click="selectImage(idx)"
                  :style="
                    idx === curImgIdx ? { background: 'rgb(204,232,255)' } : {}
                  "
                >
                  <v-img
                    class="v-img-align"
                    :src="imgDatas[idx]"
                    width="150"
                    height="150"
                    fill
                  />
                  <p class="ms-5 name-center">
                    {{ imgFile.name }}
                  </p>
                </div>
              </v-row>
            </v-sheet>
          </v-tab-item>
          <v-tab-item value="tabs-tiling" class="v-tab-item">
            <v-sheet
              class="drop pa-5 v-sheet"
              height="350"
              :class="getClasses"
              @dragover.prevent="dragOver"
              @dragleave.prevent="dragLeave"
              @drop.prevent="drop($event)"
            >
              <div
                v-if="!tilingFiles.length"
                class="d-flex align-center justify-center"
                style="height: 200px;"
              >
                <p class="text-h4 grey--text text--lighten-2">
                  Drag and Drop.
                </p>
              </div>
            </v-sheet>
          </v-tab-item>
          <v-tab-item value="tabs-metadata" class="v-tab-item">
            <v-sheet
              class="drop pa-5 v-sheet"
              height="350"
              :class="getClasses"
              @dragover.prevent="dragOver"
              @dragleave.prevent="dragLeave"
              @drop.prevent="drop($event)"
            >
              <div
                v-if="!newFiles.length"
                class="d-flex align-center justify-center"
                style="height: 200px;"
              >
                <p class="text-h4 grey--text text--lighten-2">
                  Drag and Drop.
                </p>
              </div>
              <v-card v-else>
                <v-card-title class="v-card-title">
                  <v-btn
                    class="common"
                    depressed
                    :disabled="curFileIdx == newFiles.length - 1"
                    color="primary"
                    @click="updateMetadata"
                  >
                    Update
                  </v-btn>
                  <v-spacer></v-spacer>
                  <v-text-field
                    v-model="search"
                    append-icon="mdi-magnify"
                    label="Search"
                    single-line
                    hide-details
                  ></v-text-field>
                </v-card-title>
                <v-data-table
                  :headers="metaHeaders"
                  :items="metaContents"
                  :search="search"
                >
                  <template v-slot:body="{ items }">
                    <tbody>
                      <tr
                        v-for="(item, idx) in items"
                        :key="idx"
                        :style="
                          item.no === curMetaIdx
                            ? { background: 'rgb(204,232,255)' }
                            : {}
                        "
                        @click="selectImage(item.no)"
                      >
                        <td>{{ idx + 1 }}</td>
                        <td>{{ item.filename }}</td>
                        <td>{{ item.series }}</td>
                        <td>{{ item.frame }}</td>
                        <td>{{ item.c }}</td>
                        <td>{{ item.size_c }}</td>
                        <td>{{ item.size_t }}</td>
                        <td>{{ item.size_x }}</td>
                        <td>{{ item.size_y }}</td>
                        <td>{{ item.size_z }}</td>
                      </tr>
                    </tbody>
                  </template>
                </v-data-table>
              </v-card>
            </v-sheet>
          </v-tab-item>
          <v-tab-item value="tabs-name-type" class="v-tab-item">
            <v-sheet
              class="drop pa-5 v-sheet"
              height="350"
              :class="getClasses"
              @dragover.prevent="dragOver"
              @dragleave.prevent="dragLeave"
              @drop.prevent="drop($event)"
            >
              <div
                v-if="imgFiles.length + metaFiles.length == 0"
                class="d-flex align-center justify-center"
                style="height: 200px;"
              >
                <p class="text-h4 grey--text text--lighten-2">
                  Drag and Drop.
                </p>
              </div>
              <v-row v-else class="align-center justify-center name-type-input">
                <div
                  class="type-align"
                  v-for="(type, idx) in nameTypes"
                  :key="idx"
                >
                  <v-btn class="type-btn" :color="type.color" small dark>
                    {{ type.name }}
                  </v-btn>
                  <v-text-field
                    class="type-btn"
                    :color="type.color"
                    :label="getNameType(idx)"
                    v-model="nameTypes[idx].value"
                    solo
                  ></v-text-field>
                </div>
              </v-row>
              <v-card v-if="imgFiles.length + metaFiles.length > 0">
                <v-card-title class="v-card-title">
                  <v-btn
                    class="common"
                    :disabled="updateNameTypeDisable"
                    depressed
                    color="primary"
                    @click="updateNameType"
                  >
                    Update
                  </v-btn>
                  <v-spacer class="type-spacer"></v-spacer>
                  <v-btn
                    class="common"
                    :disabled="clearNameTypeDisable"
                    depressed
                    color="primary"
                    @click="clearNameType"
                  >
                    Clear
                  </v-btn>
                  <v-spacer></v-spacer>
                  <v-text-field
                    v-model="search"
                    append-icon="mdi-magnify"
                    label="Search"
                    single-line
                    hide-details
                  ></v-text-field>
                </v-card-title>
                <v-data-table
                  :headers="nameHeaders"
                  :items="nameContents"
                  :search="search"
                >
                  <template v-slot:body="{ items }">
                    <tbody>
                      <tr
                        v-for="(item, idx) in items"
                        :key="idx"
                        :style="
                          item.no === curNameIdx
                            ? { background: 'rgb(204,232,255)' }
                            : {}
                        "
                        @click="selectImage(item.no)"
                      >
                        <td>{{ idx + 1 }}</td>
                        <td>{{ item.filename }}</td>
                        <td>{{ getSeries(item.filename) }}</td>
                        <td>{{ getColumn(item.filename) }}</td>
                        <td>{{ getRow(item.filename) }}</td>
                        <td>{{ getField(item.filename) }}</td>
                        <td>{{ getViewMethod(item.filename) }}</td>
                        <td>{{ getZPosition(item.filename) }}</td>
                        <td>{{ getTimepoint(item.filename) }}</td>
                      </tr>
                    </tbody>
                  </template>
                </v-data-table>
              </v-card>
            </v-sheet>
          </v-tab-item>
        </v-tabs-items>
      </simple-dialog>
    </v-dialog>
  </div>
</template>

<script>
// import { mapGetters } from "vuex";
// import tiff from "tiff.js";
// import atob from "atob";

import SimpleDialog from "../../../custom/SimpleDialog";

export default {
  name: "OpenPositionDialog",

  components: { SimpleDialog },

  data: () => ({
    isDragging: false,
    selectedTab: null,

    // for all files
    newFiles: [],
    curFileIdx: -1,

    // for image tag
    imgFiles: [],
    imgDatas: [],
    curImgIdx: -1,

    // for tiling
    tilingFiles: [],
    tilingDatas: [],
    curTileIdx: -1,

    // for meta tag
    metaFiles: [],
    metaDatas: [],
    curMetaIdx: -1,
    search: "",
    metaHeaders: [
      { text: "No", value: "no", sortable: false },
      { text: "FileName", value: "filename", sortable: false },
      { text: "Series", value: "series", sortable: false },
      { text: "Frame", value: "frame", sortable: false },
      { text: "C", value: "c", sortable: false },
      { text: "SizeC", value: "size_c", sortable: false },
      { text: "SizeT", value: "size_t", sortable: false },
      { text: "SizeX", value: "size_x", sortable: false },
      { text: "SizeY", value: "size_y", sortable: false },
      { text: "SizeZ", value: "size_z", sortable: false }
    ],
    metaContents: [],

    // for filename type
    curNameIdx: -1,
    nameTypes: [
      { name: "Series", value: "", color: "success" },
      { name: "Column", value: "", color: "deep-orange" },
      { name: "Row", value: "", color: "primary" },
      { name: "Field", value: "", color: "warning" },
      { name: "View Method", value: "", color: "purple" },
      { name: "Z Position", value: "", color: "blue-grey" },
      { name: "Timepoint", value: "", color: "error" }
    ],
    nameHeaders: [
      { text: "No", value: "no", sortable: false },
      { text: "FileName", value: "filename", sortable: false },
      { text: "Series", value: "series", sortable: false },
      { text: "Column", value: "column", sortable: false },
      { text: "Row", value: "row", sortable: false },
      { text: "Field", value: "field", sortable: false },
      { text: "View Method", value: "viewMethod", sortable: false },
      { text: "Z Position", value: "zPosition", sortable: false },
      { text: "Timepoint", value: "timepoint", sortable: false }
    ],
    nameContents: []
  }),

  created() {
    this.unwatch = this.$store.watch(
      (state, getters) => getters["image/metadatas"],
      res => {
        for (var key in res) {
          if (res[key]) {
            this.curFileIdx = parseInt(key.split("_")[1]);

            if (this.curFileIdx < this.newFiles.length) {
              this.metaFiles.push(this.newFiles[this.curFileIdx]);
              this.metaDatas.push(res[key]);

              let coreMetadata = res[key].coreMetadata;
              let filename = this.newFiles[this.curFileIdx].name;
              var cnt = this.metaContents.length;
              this.metaContents.push({
                no: cnt,
                filename: filename,
                series: coreMetadata.seriesCount,
                frame: coreMetadata.imageCount,
                c: coreMetadata.currentSeries,
                size_c: coreMetadata.sizeC,
                size_t: coreMetadata.sizeT,
                size_x: coreMetadata.sizeX,
                size_y: coreMetadata.sizeY,
                size_z: coreMetadata.sizeZ
              });

              cnt = this.nameContents.length;
              this.nameContents.push({
                no: cnt,
                filename: filename,
                classes: "metadata",
                idx: this.metaDatas.length - 1
              });
            }
          }
        }
      }
    );
  },

  beforeDestroy() {
    this.unwatch();
  },

  props: {
    value: {
      type: Boolean,
      default: false
    }
  },

  computed: {
    visibleDialog: {
      get() {
        return this.value;
      },
      set(val) {
        this.$emit("input", val);
      }
    },
    getClasses() {
      return { isDragging: this.isDragging };
    },
    updateNameTypeDisable() {
      if (
        this.isChangedNameType() &&
        -1 < this.curNameIdx &&
        this.curNameIdx < this.nameContents.length
      ) {
        if (
          this.makeNameType().match(
            /^(\w+)[_\s](\w+_\w)_(\w\d{2})_(\d)_(\w)(\d{2})(\w\d{2})(\w\d)\.(\w+)$/
          )
        ) {
          return false;
        }
      }

      return true;
    },
    clearNameTypeDisable() {
      return !this.isChangedNameType();
    }
  },

  methods: {
    dragOver() {
      this.isDragging = true;
    },
    dragLeave() {
      this.isDragging = false;
    },
    drop(e) {
      this.isDragging = false;

      const fileInput = this.$el.querySelector("#uploadFile");
      fileInput.files = e.dataTransfer.files;

      this.requestUploadFile();

      e.preventDefault();
    },
    requestUploadFile() {
      const fileInput = this.$el.querySelector("#uploadFile");

      if (fileInput.files && fileInput.files.length > 0) {
        for (let file of fileInput.files) {
          if (!file) {
            continue;
          }

          if (
            file.type.startsWith("image/") &&
            !file.type.startsWith("image/tif")
          ) {
            // for image tag
            this.imgFiles.push(file);
            let cnt = this.nameContents.length;
            this.nameContents.push({
              no: cnt,
              filename: file.name,
              classes: "image",
              idx: this.imgFiles.length - 1
            });

            let self = this;
            const reader = new FileReader();
            reader.onload = function() {
              let res = reader.result;
              if (res) {
                self.imgDatas.push(res);
              }
            };
            reader.readAsDataURL(file);
          } else {
            // for meta tag
            this.newFiles.push(file);
          }
        }
      }
    },
    showImageData(idx) {
      if (-1 < idx && idx < this.imgDatas.length) {
        let imgData = this.imgDatas[idx];
        if (imgData) {
          this.$store.dispatch("image/setImageDataFromPosition", imgData);
        }
      }
    },
    showMetaData(idx) {
      if (-1 < idx && idx < this.metaDatas.length) {
        let metaData = this.metaDatas[idx];
        if (metaData) {
          this.$store.dispatch("image/setMetadataFromPosition", metaData);
        }
      }
    },

    // the entire simple dialog
    // update,delete, select, cancel
    onUpdate() {},
    onDelete() {},
    onSelect() {
      switch (this.selectedTab) {
        case "tabs-images":
          this.showImageData(this.curImgIdx);
          break;

        case "tabs-tiling":
          break;

        case "tabs-metadata":
          this.showMetaData(this.curMetaIdx);
          break;

        case "tabs-name-type":
          if (
            -1 < this.curNameIdx &&
            this.curNameIdx < this.nameContents.length
          ) {
            let nameType = this.nameContents[this.curNameIdx];
            switch (nameType.classes) {
              case "image":
                this.showImageData(nameType.idx);
                break;
              case "metadata":
                this.showMetaData(nameType.idx);
                break;
            }
          }
          break;
      }

      this.visibleDialog = false;
    },
    onClose() {
      this.visibleDialog = false;
    },

    selectImage(idx) {
      switch (this.selectedTab) {
        case "tabs-images":
          this.curImgIdx = idx;
          break;

        case "tabs-tiling":
          break;

        case "tabs-metadata":
          this.curMetaIdx = idx;
          break;

        case "tabs-name-type":
          this.curNameIdx = idx;
          break;
      }
    },

    // update
    updateMetadata() {
      if (this.curFileIdx < this.newFiles.length - 1) {
        var formData = new FormData();
        for (var i = this.curFileIdx + 1; i < this.newFiles.length; i++) {
          formData.append("metafile" + "_" + i, this.newFiles[i]);
        }
        this.$store.dispatch("image/setMetaFiles", formData);
      }
    },
    updateNameType() {
      let filename = this.makeNameType();
      var nameType = this.nameContents[this.curNameIdx];
      nameType.filename = filename;
      switch (nameType.classes) {
        case "image":
          this.imgFiles.name = filename;
          break;
        case "metadata":
          this.metaFiles.name = filename;
          break;
      }
    },

    // clear
    clearNameType() {
      for (var i = 0; i < this.nameTypes.length; i++) {
        this.nameTypes[i].value = "";
      }
    },

    // regrex for name and type
    getSeries(filename) {
      let type = filename.match(
        /^(\w+)[_\s](\w+_\w)_(\w\d{2})_(\d)_(\w)(\d{2})(\w\d{2})(\w\d)\.(\w+)$/
      );
      return type ? type[2] : "";
    },
    getColumn(filename) {
      let type = filename.match(
        /^(\w+)[_\s](\w+_\w)_(\w\d{2})_(\d)_(\w)(\d{2})(\w\d{2})(\w\d)\.(\w+)$/
      );
      return type ? type[5] : "";
    },
    getRow(filename) {
      let type = filename.match(
        /^(\w+)[_\s](\w+_\w)_(\w\d{2})_(\d)_(\w)(\d{2})(\w\d{2})(\w\d)\.(\w+)$/
      );
      return type ? type[6] : "";
    },
    getField(filename) {
      let type = filename.match(
        /^(\w+)[_\s](\w+_\w)_(\w\d{2})_(\d)_(\w)(\d{2})(\w\d{2})(\w\d)\.(\w+)$/
      );
      return type ? type[7] : "";
    },
    getViewMethod(filename) {
      let type = filename.match(
        /^(\w+)[_\s](\w+_\w)_(\w\d{2})_(\d)_(\w)(\d{2})(\w\d{2})(\w\d)\.(\w+)$/
      );
      return type ? type[8] : "";
    },
    getZPosition(filename) {
      let type = filename.match(
        /^(\w+)[_\s](\w+_\w)_(\w\d{2})_(\d)_(\w)(\d{2})(\w\d{2})(\w\d)\.(\w+)$/
      );
      return type ? type[4] : "";
    },
    getTimepoint(filename) {
      let type = filename.match(
        /^(\w+)[_\s](\w+_\w)_(\w\d{2})_(\d)_(\w)(\d{2})(\w\d{2})(\w\d)\.(\w+)$/
      );
      return type ? type[3] : "";
    },
    getNameType(idx) {
      if (this.curNameIdx == -1) {
        return "";
      } else {
        switch (idx) {
          case 0:
            return this.getSeries(this.nameContents[this.curNameIdx].filename);
          case 1:
            return this.getColumn(this.nameContents[this.curNameIdx].filename);
          case 2:
            return this.getRow(this.nameContents[this.curNameIdx].filename);
          case 3:
            return this.getField(this.nameContents[this.curNameIdx].filename);
          case 4:
            return this.getViewMethod(
              this.nameContents[this.curNameIdx].filename
            );
          case 5:
            return this.getZPosition(
              this.nameContents[this.curNameIdx].filename
            );
          case 6:
            return this.getTimepoint(
              this.nameContents[this.curNameIdx].filename
            );
        }
      }

      return "";
    },

    // utils
    isChangedNameType() {
      for (var i = 0; i < this.nameTypes.length; i++) {
        if (this.nameTypes[i].value != "") {
          return true;
        }
      }

      return false;
    },
    makeNameType() {
      var filename = this.nameContents[this.curNameIdx].filename;
      let type = filename.match(
        /^(\w+)[_\s](\w+_\w)_(\w\d{2})_(\d)_(\w)(\d{2})(\w\d{2})(\w\d)\.(\w+)$/
      );
      let idx = filename.lastIndexOf(".");
      let ext = filename.substring(idx + 1);
      filename =
        (type ? type[1] : filename.substring(0, idx)) +
        "_" +
        (this.nameTypes[0].value
          ? this.nameTypes[0].value
          : this.getSeries(filename)) +
        "_" +
        (this.nameTypes[6].value
          ? this.nameTypes[6].value
          : this.getTimepoint(filename)) +
        "_" +
        (this.nameTypes[5].value
          ? this.nameTypes[5].value
          : this.getZPosition(filename)) +
        "_" +
        (this.nameTypes[1].value
          ? this.nameTypes[1].value
          : this.getColumn(filename)) +
        (this.nameTypes[2].value
          ? this.nameTypes[2].value
          : this.getRow(filename)) +
        (this.nameTypes[3].value
          ? this.nameTypes[3].value
          : this.getField(filename)) +
        (this.nameTypes[4].value
          ? this.nameTypes[4].value
          : this.getViewMethod(filename)) +
        "." +
        ext;

      return filename;
    }
  }
};
</script>

<style scoped>
.isDragging {
  background-color: #e0f2f1;
  border-color: #fff;
}
.name-center {
  text-align: center;
}
.img-align {
  width: 25%;
  padding: 10px;
}
.img-align > p {
  margin: auto;
}
.v-img-align {
  margin: auto;
}
#uploadFile {
  display: none;
}
.v-sheet {
  overflow: auto;
  padding: 15px !important;
}
.v-tab-item {
  padding-top: 10px;
}
.v-card-title {
  padding-top: 0px;
}
.type-align {
  width: 14.2%;
  padding: 5px;
}
.type-btn {
  width: 100%;
  text-transform: none;
}
.type-btn >>> input {
  width: 100%;
  text-align: center;
}
.type-btn >>> label {
  width: 100%;
  text-align: center;
}
.type-btn >>> .v-input__control {
  min-height: 30px !important;
}
.name-type-input {
  margin-left: -5px;
  margin-right: -5px;
  margin-bottom: -30px;
}
.type-spacer {
  flex-grow: 0.1 !important;
}
.common {
  width: 80px;
}
</style>
