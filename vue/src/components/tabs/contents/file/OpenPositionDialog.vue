<template>
  <div style="display:none;">
    <input type="file" id="uploadFile" @change="requestUploadFile" />
    <v-dialog v-model="visibleDialog" max-width="980">
      <simple-dialog
        title="Position"
        okTitle="Select"
        :updateButton="true"
        :deleteButton="true"
        :singleButton="false"
        :updateDisable="!newFiles.length"
        :selectDisable="!selectPossible"
        :deleteDisable="!deletePossible"
        @update="onUpdate"
        @delete="onDelete"
        @select="onSelect"
        @close="onClose"
      >
        <v-tabs v-model="selectedTab" fixed-tabs>
          <v-tab href="#tabs-new" class="primary--text">New Files</v-tab>
          <v-tab href="#tabs-images" class="primary--text">Images</v-tab>
          <v-tab href="#tabs-tiling" class="primary--text">Tiling</v-tab>
          <v-tab href="#tabs-metadata" class="primary--text">Metadata</v-tab>
          <v-tab href="#tabs-name-type" class="primary--text"
            >Names &amp; Types</v-tab
          >
        </v-tabs>

        <v-tabs-items v-model="selectedTab" class="v-tab-item">
          <!-- New File Tab -->
          <v-tab-item value="tabs-new" class="v-tab-item">
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
                  <v-spacer></v-spacer>
                  <v-text-field
                    v-model="searchNewFile"
                    append-icon="mdi-magnify"
                    label="Search"
                    single-line
                    hide-details
                  ></v-text-field>
                </v-card-title>
                <v-data-table
                  v-model="selectedNewContents"
                  class="new-file-table"
                  :headers="newHeaders"
                  :items="newContents"
                  :search="searchNewFile"
                  :single-select="false"
                  :item-class="meta_row_highlight"
                  item-key="no"
                  show-select
                >
                </v-data-table>
              </v-card>
            </v-sheet>
          </v-tab-item>
          <!-- Images Tab -->
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
                v-if="!metaFiles.length"
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
                  v-for="(file, idx) in metaFiles"
                  :key="idx"
                  @click="selectContent(idx)"
                  v-bind:class="meta_row_highlight(idx)"
                >
                  <v-img
                    class="v-img-align"
                    :src="metaDatas[idx].imageData"
                    width="150"
                    height="150"
                    fill
                  />
                  <p class="ms-5 name-center">
                    {{ file.name }}
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
                v-if="!metaFiles.length"
                class="d-flex align-center justify-center"
                style="height: 200px;"
              >
                <p class="text-h4 grey--text text--lighten-2">
                  Drag and Drop.
                </p>
              </div>
              <v-card v-else>
                <v-card-title class="v-card-title">
                  <v-spacer></v-spacer>
                  <v-text-field
                    v-model="searchMetadata"
                    append-icon="mdi-magnify"
                    label="Search"
                    single-line
                    hide-details
                  ></v-text-field>
                </v-card-title>
                <v-data-table
                  v-model="selectedMetaContents"
                  class="meta-file-table"
                  :headers="metaHeaders"
                  :items="getMetaContents"
                  :search="searchMetadata"
                  :single-select="false"
                  :item-class="meta_row_highlight"
                  item-key="no"
                  show-select
                  @click:row="selectContent"
                >
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
                    :disabled="!changeNameType"
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
                    v-model="searchNameType"
                    append-icon="mdi-magnify"
                    label="Search"
                    single-line
                    hide-details
                  ></v-text-field>
                </v-card-title>
                <v-data-table
                  v-model="selectedNameContents"
                  class="name-type-table"
                  :headers="nameHeaders"
                  :items="getNameContents"
                  :search="searchNameType"
                  :single-select="false"
                  :item-class="meta_row_highlight"
                  item-key="no"
                  show-select
                  @click:row="selectContent"
                >
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

    // meta files
    metaFiles: [],
    metaDatas: [],

    // for all files
    searchNewFile: "",
    newFiles: [],
    newContents: [],
    selectedNewContents: [],
    newHeaders: [
      { text: "No", value: "no", sortable: false },
      { text: "File Name", value: "filename", sortable: false }
    ],

    // for image tag
    curImgIdx: -1,
    imgFiles: [],
    imgDatas: [],
    selectedImgIndices: [],

    // for tiling
    curTileIdx: -1,
    tilingFiles: [],
    tilingDatas: [],

    // for meta tag
    curMetaIdx: -1,
    searchMetadata: "",
    selectedMetaContents: [],
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

    // for filename type
    curNameIdx: -1,
    searchNameType: "",
    selectedNameContents: [],
    nameTypes: [
      { name: "Series", value: "", color: "success" },
      { name: "Column", value: "", color: "deep-orange" },
      { name: "Row", value: "", color: "primary" },
      { name: "Field", value: "", color: "warning" },
      { name: "View Method", value: "", color: "purple" },
      { name: "Z Position", value: "", color: "blue-grey" },
      { name: "Time Point", value: "", color: "error" }
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
      { text: "Time Point", value: "timepoint", sortable: false }
    ]
  }),

  created() {
    this.unwatch = this.$store.watch(
      (state, getters) => getters["image/metadatas"],
      res => {
        for (var key in res) {
          if (res[key]) {
            const curFileIdx = parseInt(key.split("_")[1]);

            if (curFileIdx < this.newFiles.length) {
              this.metaFiles.push(this.newFiles[curFileIdx]);
              this.metaDatas.push(res[key]);
            }
          }
        }

        // init new files
        this.newFiles = [];
        this.newContents = [];
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
    changeNameType() {
      if (
        this.isChangedNameType() &&
        -1 < this.curNameIdx &&
        this.curNameIdx < this.metaFiles.length
      ) {
        if (
          this.makeNameType().match(
            /^(\w+)[_\s](\w+_\w)_(\w\d{2})_(\d)_(\w)(\d{2})(\w\d{2})(\w\d)\.(\w+)$/
          )
        ) {
          return true;
        }
      }

      return false;
    },
    clearNameTypeDisable() {
      return !this.isChangedNameType();
    },
    deletePossible() {
      switch (this.selectedTab) {
        case "tabs-new":
          return this.selectedNewContents.length;

        case "tabs-images":
          return this.selectedImgIndices.length;

        case "tabs-tiling":
          break;

        case "tabs-metadata":
          return this.selectedMetaContents.length;

        case "tabs-name-type":
          return this.selectedNameContents.length;
      }

      return false;
    },
    selectPossible() {
      switch (this.selectedTab) {
        case "tabs-new":
          return false;

        case "tabs-images":
          return this.curImgIdx > -1;

        case "tabs-tiling":
          return false;

        case "tabs-metadata":
          return this.curMetaIdx > -1;

        case "tabs-name-type":
          return this.curNameIdx > -1;
      }

      return false;
    },
    getNameContents() {
      const contents = [];
      this.metaFiles.forEach(file => {
        contents.push({
          no: contents.length + 1,
          filename: file.name,
          series: this.getSeries(file.name),
          column: this.getColumn(file.name),
          row: this.getRow(file.name),
          field: this.getField(file.name),
          viewMethod: this.getViewMethod(file.name),
          zPosition: this.getZPosition(file.name),
          timepoint: this.getTimepoint(file.name)
        });
      });

      return contents;
    },
    getMetaContents() {
      const contents = [];
      this.metaFiles.forEach((file, idx) => {
        const coreMetadata = this.metaDatas[idx].coreMetadata;
        contents.push({
          no: contents.length + 1,
          filename: file.name,
          series: coreMetadata.seriesCount,
          frame: coreMetadata.imageCount,
          c: coreMetadata.currentSeries,
          size_c: coreMetadata.sizeC,
          size_t: coreMetadata.sizeT,
          size_x: coreMetadata.sizeX,
          size_y: coreMetadata.sizeY,
          size_z: coreMetadata.sizeZ
        });
      });

      return contents;
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
          if (file) {
            this.newFiles.push(file);
            this.newContents.push({
              no: this.newContents.length + 1,
              filename: file.name
            });
          }
        }
      }
    },

    // the entire simple dialog
    // update,delete, select, cancel
    onUpdate() {
      if (this.newFiles.length > 0) {
        // dispatch
        var formData = new FormData();
        for (var i = 0; i < this.newFiles.length; i++) {
          formData.append("metafile" + "_" + i, this.newFiles[i]);
        }
        this.$store.dispatch("image/setMetaFiles", formData);

        this.selectedNewContents = [];
      }
    },
    onDelete() {
      switch (this.selectedTab) {
        case "tabs-new":
          {
            const remainFiles = [];
            const remainContents = [];
            this.newContents.forEach(content => {
              if (
                !this.selectedNewContents.includes(content) &&
                0 < content.no &&
                content.no <= this.newFiles.length
              ) {
                remainFiles.push(this.newFiles[content.no - 1]);
                content.no = remainContents.length + 1;
                remainContents.push(content);
              }
            });
            this.newFiles = remainFiles;
            this.newContents = remainContents;
            this.selectedNewContents = [];
          }
          break;

        case "tabs-images":
          {
            const remainFiles = [];
            const remainDatas = [];
            this.metaFiles.forEach((file, idx) => {
              if (!this.selectedImgIndices.includes(idx)) {
                remainFiles.push(file);
                remainDatas.push(this.metaDatas[idx]);
              }
            });
            this.metaFiles = remainFiles;
            this.metaDatas = remainDatas;
          }
          this.initMetaDatas();
          break;

        case "tabs-tiling":
          break;

        case "tabs-metadata":
          {
            const remainFiles = [];
            const remainDatas = [];
            const remainContents = [];
            this.getMetaContents.forEach(content => {
              if (
                !this.selectedMetaContents.includes(content) &&
                0 < content.no &&
                content.no <= this.metaFiles.length
              ) {
                remainFiles.push(this.metaFiles[content.no - 1]);
                remainDatas.push(this.metaDatas[content.no - 1]);
                content.no = remainContents.length + 1;
                remainContents.push(content);
              }
            });
            this.metaFiles = remainFiles;
            this.metaDatas = remainDatas;
          }
          this.initMetaDatas();
          break;

        case "tabs-name-type":
          {
            const remainFiles = [];
            const remainDatas = [];
            const remainContents = [];
            this.getNameContents.forEach(content => {
              if (
                !this.selectedNameContents.includes(content) &&
                0 < content.no &&
                content.no <= this.metaFiles.length
              ) {
                remainFiles.push(this.metaFiles[content.no - 1]);
                remainDatas.push(this.metaDatas[content.no - 1]);
                content.no = remainContents.length + 1;
                remainContents.push(content);
              }
            });
            this.metaFiles = remainFiles;
            this.metaDatas = remainDatas;
          }
          this.initMetaDatas();
          break;
      }
    },
    initMetaDatas() {
      this.curImgIdx = -1;
      this.curMetaIdx = -1;
      this.curNameIdx = -1;
      this.selectedImgIndices = [];
      this.selectedMetaContents = [];
      this.selectedNameContents = [];
    },
    onSelect() {
      switch (this.selectedTab) {
        case "tabs-new":
          break;

        case "tabs-images":
          this.showMetaData(this.curImgIdx);
          break;

        case "tabs-tiling":
          break;

        case "tabs-metadata":
          this.showMetaData(this.curMetaIdx);
          break;

        case "tabs-name-type":
          this.showMetaData(this.curNameIdx);
          break;
      }

      this.visibleDialog = false;
    },
    showImageData(idx) {
      if (-1 < idx && idx < this.imgDatas.length) {
        const imgData = this.imgDatas[idx];
        if (imgData) {
          this.$store.dispatch("image/setImageDataFromPosition", imgData);
        }
      }
    },
    showMetaData(idx) {
      if (-1 < idx && idx < this.metaDatas.length) {
        const metaData = this.metaDatas[idx];
        if (metaData) {
          this.$store.dispatch("image/setMetadataFromPosition", metaData);
        }
      }
    },
    onClose() {
      this.visibleDialog = false;
    },

    selectContent(content) {
      switch (this.selectedTab) {
        case "tabs-new":
          break;

        case "tabs-images":
          {
            this.curImgIdx = content;
            const i = this.selectedImgIndices.indexOf(content);
            if (i > -1) {
              this.selectedImgIndices.splice(i, 1);
            } else {
              this.selectedImgIndices.push(content);
            }
          }
          break;

        case "tabs-tiling":
          break;

        case "tabs-metadata":
          this.curMetaIdx = content.no - 1;
          break;

        case "tabs-name-type":
          this.curNameIdx = content.no - 1;
          break;
      }
    },

    // update
    updateNameType() {
      const filename = this.makeNameType();
      var nameType = this.getNameContents[this.curNameIdx];
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
      const type = filename.match(
        /^(\w+)[_\s](\w+_\w)_(\w\d{2})_(\d)_(\w)(\d{2})(\w\d{2})(\w\d)\.(\w+)$/
      );
      return type ? type[2] : "";
    },
    getColumn(filename) {
      const type = filename.match(
        /^(\w+)[_\s](\w+_\w)_(\w\d{2})_(\d)_(\w)(\d{2})(\w\d{2})(\w\d)\.(\w+)$/
      );
      return type ? type[5] : "";
    },
    getRow(filename) {
      const type = filename.match(
        /^(\w+)[_\s](\w+_\w)_(\w\d{2})_(\d)_(\w)(\d{2})(\w\d{2})(\w\d)\.(\w+)$/
      );
      return type ? type[6] : "";
    },
    getField(filename) {
      const type = filename.match(
        /^(\w+)[_\s](\w+_\w)_(\w\d{2})_(\d)_(\w)(\d{2})(\w\d{2})(\w\d)\.(\w+)$/
      );
      return type ? type[7] : "";
    },
    getViewMethod(filename) {
      const type = filename.match(
        /^(\w+)[_\s](\w+_\w)_(\w\d{2})_(\d)_(\w)(\d{2})(\w\d{2})(\w\d)\.(\w+)$/
      );
      return type ? type[8] : "";
    },
    getZPosition(filename) {
      const type = filename.match(
        /^(\w+)[_\s](\w+_\w)_(\w\d{2})_(\d)_(\w)(\d{2})(\w\d{2})(\w\d)\.(\w+)$/
      );
      return type ? type[4] : "";
    },
    getTimepoint(filename) {
      const type = filename.match(
        /^(\w+)[_\s](\w+_\w)_(\w\d{2})_(\d)_(\w)(\d{2})(\w\d{2})(\w\d)\.(\w+)$/
      );
      return type ? type[3] : "";
    },
    getNameType(idx) {
      if (this.curNameIdx == -1) {
        return "";
      } else {
        const filename = this.metaFiles[this.curNameIdx].name;
        switch (idx) {
          case 0:
            return this.getSeries(filename);
          case 1:
            return this.getColumn(filename);
          case 2:
            return this.getRow(filename);
          case 3:
            return this.getField(filename);
          case 4:
            return this.getViewMethod(filename);
          case 5:
            return this.getZPosition(filename);
          case 6:
            return this.getTimepoint(filename);
        }
      }

      return "";
    },

    // styles
    meta_row_highlight(item) {
      let rowClass = "";

      switch (this.selectedTab) {
        case "tabs-new":
          if (this.selectedNewContents.includes(item)) {
            rowClass = "row_delete";
          }
          break;

        case "tabs-images":
          if (item == this.curImgIdx) {
            rowClass = "success lighten-3 ";
          }
          if (this.selectedImgIndices.includes(item)) {
            rowClass += "row_delete";
          }
          break;

        case "tabs-tiling":
          break;

        case "tabs-metadata":
          if (item.no - 1 == this.curMetaIdx) {
            rowClass = "success lighten-3 ";
          }
          if (this.selectedMetaContents.includes(item)) {
            rowClass += "row_delete";
          }
          break;

        case "tabs-name-type":
          if (item.no - 1 == this.curNameIdx) {
            rowClass = "success lighten-3 ";
          }
          if (this.selectedNameContents.includes(item)) {
            rowClass += "row_delete";
          }
          break;
      }

      return rowClass;
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
      var filename = this.metaFiles[this.curNameIdx].name;
      const type = filename.match(
        /^(\w+)[_\s](\w+_\w)_(\w\d{2})_(\d)_(\w)(\d{2})(\w\d{2})(\w\d)\.(\w+)$/
      );
      const idx = filename.lastIndexOf(".");
      const ext = filename.substring(idx + 1);
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
  width: 23%;
  padding: 10px;
  margin: 1%;
}
.img-align > p {
  margin: 0px !important;
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
.new-file-table >>> tr th:nth-child(2),
.new-file-table >>> tr td:nth-child(2) {
  width: 60px !important;
}
.meta-file-table >>> tr th:nth-child(3),
.meta-file-table >>> tr td:nth-child(3) {
  width: 295px !important;
}
.name-type-table >>> tr th:nth-child(3),
.name-type-table >>> tr td:nth-child(3) {
  width: 295px !important;
}
::v-deep .row_delete {
  color: #c36a0a;
}
</style>
