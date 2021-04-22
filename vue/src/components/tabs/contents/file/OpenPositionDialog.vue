<template>
  <div style="display: none">
    <input type="file" id="uploadFile" @change="requestUploadFile" />
    <v-dialog v-model="visibleDialog" max-width="980">
      <simple-dialog
        title="Position"
        okTitle="Select"
        :singleButton="false"
        :selectDisable="!this.allFiles.length"
        @select="onSelect"
        @close="onClose"
      >
        <v-tabs v-model="selectedTab" fixed-tabs>
          <v-tab href="#tabs-images" class="primary--text">Images</v-tab>
          <v-tab href="#tabs-tiling" class="primary--text">Tiling</v-tab>
          <v-tab href="#tabs-metadata" class="primary--text">Metadata</v-tab>
          <v-tab href="#tabs-name-type" class="primary--text">Names &amp; Types</v-tab>
        </v-tabs>

        <v-tabs-items v-model="selectedTab" class="v-tab-item">
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
                v-if="!files.length"
                class="d-flex align-center justify-center"
                style="height: 200px"
              >
                <p class="text-h4 grey--text text--lighten-2">Drag and Drop.</p>
              </div>
              <v-row v-else class="align-center">
                <div
                  class="img-align"
                  v-for="(file, idx) in files"
                  :key="idx"
                  @click="selectContent(idx)"
                >
                  <v-img
                    class="v-img-align"
                    :src="file.imageData"
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
                style="height: 200px"
              >
                <p class="text-h4 grey--text text--lighten-2">Drag and Drop.</p>
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
                v-if="!allFiles.length"
                class="d-flex align-center justify-center"
                style="height: 200px"
              >
                <p class="text-h4 grey--text text--lighten-2">Drag and Drop.</p>
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
                  item-key="no"
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
                v-if="allFiles.length == 0"
                class="d-flex align-center justify-center"
                style="height: 200px"
              >
                <p class="text-h4 grey--text text--lighten-2">Drag and Drop.</p>
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
              <v-card v-if="allFiles.length > 0">
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
                  item-key="no"
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
import { createNamespacedHelpers } from 'vuex';
import { checkFileType } from "../../../../utils/utils-func";
import SimpleDialog from "../../../custom/SimpleDialog";

const { mapState, mapActions } = createNamespacedHelpers('files');

export default {
  name: "OpenPositionDialog",

  components: { SimpleDialog },

  data: () => ({
    isDragging: false,
    selectedTab: null,

    // dropped files
    droppedFiles: [],

    // all data
    allFiles: [],

    // meta files
    metaFiles: [],
    metaData: [],

    // for image tag
    curImgIdx: -1,
    imgFiles: [],
    imgData: [],
    selectedImgIndices: [],

    // for tiling
    curTileIdx: -1,
    tilingFiles: [],
    tilingData: [],

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
      { text: "SizeZ", value: "size_z", sortable: false },
    ],

    // for filename type
    curNameIdx: -1,
    searchNameType: "",
    selectedNameContents: [],
    nameTypes: [
      { name: "Series", value: "", color: "success" },
      { name: "Row", value: "", color: "primary" },
      { name: "Column", value: "", color: "deep-orange" },
      { name: "Field", value: "", color: "warning" },
      { name: "View Method", value: "", color: "purple" },
      { name: "Z Position", value: "", color: "blue-grey" },
      { name: "Time Point", value: "", color: "error" },
    ],
    nameHeaders: [
      { text: "No", value: "no", sortable: false },
      { text: "FileName", value: "filename", sortable: false },
      { text: "Series", value: "series", sortable: false },
      { text: "Row", value: "row", sortable: false },
      { text: "Column", value: "column", sortable: false },
      { text: "Field", value: "field", sortable: false },
      { text: "View Method", value: "viewMethod", sortable: false },
      { text: "Z Position", value: "zPosition", sortable: false },
      { text: "Time Point", value: "timepoint", sortable: false },
    ],
  }),

  created() {
    this.newResWatch = this.$store.watch(
      (state, getters) => getters["image/newRes"],
      (res) => {
        const filteredData = [];
        for (var key in res) {
          const idx = parseInt(key.split("_")[1]);
          if (
            key.startsWith("position_") &&
            res[key] &&
            idx < this.allFiles.length
          ) {
            filteredData.push({
              filename: this.allFiles[idx].name,
              metadata: res[key],
            });
          }
        }

        if (filteredData.length > 0) {
          this.$store.dispatch("image/addData", filteredData);
        }

        this.newFile = null;
        this.imageData = null;
      }
    );

    this.allFilesWatch = this.$store.watch(
      (state, getters) => getters["image/currentPageData"],
      (res) => {
        this.allFiles = res;
      }
    );
  },

  beforeDestroy() {
    this.newResWatch();
    this.allFilesWatch();
  },

  props: {
    value: {
      type: Boolean,
      default: false,
    },
  },

  computed: {
    visibleDialog: {
      get() {
        return this.value;
      },
      set(val) {
        this.$emit("input", val);
      },
    },
    getClasses() {
      return { isDragging: this.isDragging };
    },
    changeNameType() {
      if (
        this.isChangedNameType() &&
        -1 < this.curNameIdx &&
        this.curNameIdx < this.allFiles.length
      ) {
        if (
          this.makeNameType().match(
            /^(\w+)[_\s](\w+_\w+)_(\w\d{2})_(\d)_(\w)(\d{2})(\w\d{2})(\w\d)\.(\w+)$/
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

    getNameContents() {
      const contents = [];
      for (let file in this.allFiles) {
        if (file.name) {
          contents.push({
            no: contents.length + 1,
            filename: file.name,
            series: this.getSeries(file.name),
            row: this.getRow(file.name),
            column: this.getColumn(file.name),
            field: this.getField(file.name),
            viewMethod: this.getViewMethod(file.name),
            zPosition: this.getZPosition(file.name),
            timepoint: this.getTimepoint(file.name),
          });
        }
      }

      return contents;
    },
    getMetaContents() {
      const contents = [];
      this.allFiles.forEach((file) => {
        contents.push({
          no: contents.length + 1,
          filename: file.name,
          series: "",
          frame: "",
          c: "",
          size_c: "",
          size_t: "",
          size_x: "",
          size_y: "",
          size_z: "",
        });
      });

      return contents;
    },
    ...mapState({
      files: state => state.position.files,
    }),
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
      e.preventDefault();

      this.clearFiles();

      let items = e.dataTransfer.items;
      for (let i = 0; i < items.length; i++) {
        let item = items[i].webkitGetAsEntry();
        if (item) {
          this.traverseFileTree(item);
        }
      }
    },

    traverseFileTree(item, path) {
      let self = this;
      path = path || "";

      if (item.isFile) {
        item.file(function (file) {
          console.log(file.name);
          if (checkFileType(file.name)) {
            self.addFile(file);
          }
        });
      } else if (item.isDirectory) {
        let dirReader = item.createReader();
        dirReader.readEntries(function(entries) {
          for (let i = 0; i < entries.length; i++) {
            self.traverseFileTree(entries[i], path + item.name + "/");
          }
        });
      }
    },

    requestUploadFile() {
      const fileInput = this.$el.querySelector("#uploadFile");

      if (fileInput.files && fileInput.files.length > 0) {
        this.allFiles = fileInput.files;
        this.setFiles(fileInput.files);
      }
    },

    onSelect() {
      this.visibleDialog = false;

      if (!this.allFiles) {
        return "";
      }

      let formData = new FormData();
      const name = this.getMainName();
      if (name) {
        this.allFiles.forEach((file, idx) => {
          const type = file.name.match(
            /^(\w+)[_\s](\w+_\w+)_(\w\d{2})_(\d)_(\w)(\d{2})(\w\d{2})(\w\d)\.(\w+)$/
          );
          if (type && type[1] == name) {
            formData.append("position_" + idx, file);
          }
        });
      } else {
        formData.append("position_0", this.allFiles[0]);
      }

      this.$store.dispatch("image/setNewFiles", formData);
    },
    showImageData(idx) {
      if (-1 < idx && idx < this.imgData.length) {
        const imgData = this.imgData[idx];
        if (imgData) {
          this.$store.dispatch("image/setImageDataFromPosition", imgData);
        }
      }
    },
    showMetaData(idx) {
      if (-1 < idx && idx < this.metaData.length) {
        const metaData = this.metaData[idx];
        if (metaData) {
          this.$store.dispatch("image/setMetadataFromPosition", metaData);
        }
      }
    },
    onClose() {
      this.visibleDialog = false;
    },

    getMainName() {
      if (!this.allFiles) {
        return "";
      }

      let num = {};
      const cnt = this.allFiles.length;
      for (let idx = 0; idx < cnt; idx++) {
        const type = this.allFiles[idx].name.match(
          /^(\w+)[_\s](\w+_\w+)_(\w\d{2})_(\d)_(\w)(\d{2})(\w\d{2})(\w\d)\.(\w+)$/
        );
        if (type) {
          const name = type[1];
          if (num[name]) {
            num[name] += 1;
          } else {
            num[name] = 1;
          }
        }
      }

      let maxN = 1;
      let maxKey = "";
      for (var key in num) {
        if (maxN < num[key]) {
          maxN = num[key];
          maxKey = key;
        }
      }

      return maxKey;
    },
    getSource(file) {
      if (
        file &&
        file.type &&
        file.type.startsWith("image/") &&
        !file.type.startsWith("image/tif") &&
        file.size < 2 * 1024 * 1024
      ) {
        const reader = new FileReader();
        reader.onload = function () {
          if (file.type.startsWith("image/tif")) {
            return require("../../../../assets/images/no-preview.png");
          } else {
            return reader.result;
          }
        };
        reader.readAsDataURL(file);
      }

      return require("../../../../assets/images/no-preview.png");
    },

    selectContent(content) {
      switch (this.selectedTab) {
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
      // const filename = this.makeNameType();
      // const file = this.allFiles[this.curNameIdx];
      // file.name = filename;
      // this.allFiles = this.allFiles.map((val, idx) =>
      //   idx == this.curNameIdx ? file : val
      // );
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
        /^(\w+)[_\s](\w+_\w+)_(\w\d{2})_(\d)_(\w)(\d{2})(\w\d{2})(\w\d)\.(\w+)$/
      );
      return type ? type[2] : "";
    },
    getRow(filename) {
      const type = filename.match(
        /^(\w+)[_\s](\w+_\w+)_(\w\d{2})_(\d)_(\w)(\d{2})(\w\d{2})(\w\d)\.(\w+)$/
      );
      return type ? type[5] : "";
    },
    getColumn(filename) {
      const type = filename.match(
        /^(\w+)[_\s](\w+_\w+)_(\w\d{2})_(\d)_(\w)(\d{2})(\w\d{2})(\w\d)\.(\w+)$/
      );
      return type ? type[6] : "";
    },
    getField(filename) {
      const type = filename.match(
        /^(\w+)[_\s](\w+_\w+)_(\w\d{2})_(\d)_(\w)(\d{2})(\w\d{2})(\w\d)\.(\w+)$/
      );
      return type ? type[7] : "";
    },
    getViewMethod(filename) {
      const type = filename.match(
        /^(\w+)[_\s](\w+_\w+)_(\w\d{2})_(\d)_(\w)(\d{2})(\w\d{2})(\w\d)\.(\w+)$/
      );
      return type ? type[8] : "";
    },
    getZPosition(filename) {
      const type = filename.match(
        /^(\w+)[_\s](\w+_\w+)_(\w\d{2})_(\d)_(\w)(\d{2})(\w\d{2})(\w\d)\.(\w+)$/
      );
      return type ? type[4] : "";
    },
    getTimepoint(filename) {
      const type = filename.match(
        /^(\w+)[_\s](\w+_\w+)_(\w\d{2})_(\d)_(\w)(\d{2})(\w\d{2})(\w\d)\.(\w+)$/
      );
      return type ? type[3] : "";
    },
    getNameType(idx) {
      if (this.curNameIdx == -1) {
        return "";
      } else {
        const filename = this.allFiles[this.curNameIdx].name;
        switch (idx) {
          case 0:
            return this.getSeries(filename);
          case 1:
            return this.getRow(filename);
          case 2:
            return this.getColumn(filename);
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
      var filename = this.allFiles[this.curNameIdx].name;
      const type = filename.match(
        /^(\w+)[_\s](\w+_\w+)_(\w\d{2})_(\d)_(\w)(\d{2})(\w\d{2})(\w\d)\.(\w+)$/
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
          : this.getRow(filename)) +
        (this.nameTypes[2].value
          ? this.nameTypes[2].value
          : this.getColumn(filename)) +
        (this.nameTypes[3].value
          ? this.nameTypes[3].value
          : this.getField(filename)) +
        (this.nameTypes[4].value
          ? this.nameTypes[4].value
          : this.getViewMethod(filename)) +
        "." +
        ext;

      return filename;
    },
    ...mapActions([
      'setFiles',
      'clearFiles',
      'addFile'
    ]),
  },
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
.meta-file-table >>> tr th:nth-child(2),
.meta-file-table >>> tr td:nth-child(2) {
  width: 295px !important;
}
.name-type-table >>> tr th:nth-child(2),
.name-type-table >>> tr td:nth-child(2) {
  width: 295px !important;
}
</style>
