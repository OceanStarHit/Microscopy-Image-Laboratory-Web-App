<template>
  <div class="d-none">
    <input
      type="file"
      id="uploadFile"
      class="d-none"
      @change="requestUploadFile"
    />
    <v-dialog v-model="visibleDialog" max-width="1080">
      <simple-dialog
        title="Position"
        okTitle="Select"
        :singleButton="false"
        :selectDisable="!this.allFiles.length"
        @select="onSelect"
        @close="onClose"
      >
        <v-tabs v-model="selectedTab" fixed-tabs @change="onTabChange">
          <v-tab href="#tabs-images" class="primary--text">Images</v-tab>
          <v-tab href="#tabs-tiling" class="primary--text">Tiling</v-tab>
          <v-tab href="#tabs-metadata" class="primary--text">Metadata</v-tab>
          <v-tab href="#tabs-name-type" class="primary--text"
            >Names &amp; Types</v-tab
          >
        </v-tabs>

        <v-tabs-items v-model="selectedTab" class="v-tab-item">
          <!-- Images Tab -->
          <v-tab-item value="tabs-images">
            <v-sheet
              class="drop pa-5 overflow-y-auto"
              height="600"
              :class="getClasses"
              @dragover.prevent="dragOver"
              @dragleave.prevent="dragLeave"
              @drop.prevent="drop($event)"
            >
              <div
                v-if="!files.length"
                class="d-flex align-center justify-center fill-height"
              >
                <p class="text-h4 grey--text text--lighten-2">{{ backgroundText }}</p>
              </div>
              <v-row v-else class="align-center">
                <v-col
                  v-for="(file, idx) in files"
                  :key="idx"
                  cols="2"
                  class="px-4"
                >
                  <v-img
                    :src="file.imageData"
                    lazy-src="../../../../assets/images/image-placeholder.png"
                    class="mx-auto"
                    aspect-ratio="1"
                    width="130"
                    height="130"
                  />
                  <p class="ma-2 text-center text-caption">
                    {{ file.name }}
                  </p>
                </v-col>
              </v-row>
            </v-sheet>
          </v-tab-item>
          <v-tab-item value="tabs-tiling" class="v-tab-item" eager>
            <v-sheet class="drop pa-5" height="600">
              <v-row no-gutters>
                <v-col cols="2">
                  <v-card class="pa-1">
                    <v-list shaped>
                      <v-list-item-group
                        v-model="activeMenuItem"
                        color="primary"
                      >
                        <v-list-item
                          v-for="(menuTitle, idx) in tilingMenus"
                          :key="idx"
                        >
                          <v-list-item-content>
                            <v-list-item-title
                              v-text="menuTitle"
                            ></v-list-item-title>
                          </v-list-item-content>
                        </v-list-item>
                      </v-list-item-group>
                    </v-list>
                  </v-card>
                </v-col>
                <v-col cols="10" class="pa-2">
                  <!-- Editing -->
                  <v-card v-if="activeMenuItem == 0" flat>
                    <v-card-title class="pa-1">Editing</v-card-title>
                    <div class="d-flex ma-4">
                      <div class="control-panel">
                        <v-list
                          class="overflow-y-auto fill-height mr-4"
                          max-height="450"
                          outlined
                        >
                          <v-list-item v-for="(file, idx) in files" :key="idx">
                            <v-list-item-content>
                              <v-list-item-title
                                v-text="file.name"
                              ></v-list-item-title>
                            </v-list-item-content>
                          </v-list-item>
                        </v-list>
                      </div>
                      <canvas id="canvas" ref="canvas" class="black-border"></canvas>
                      <!-- <v-img
                        src=""
                        class="black-border"
                        width="350"
                        height="350"
                        fill
                      /> -->
                    </div>
                  </v-card>

                  <!-- Alignment -->
                  <v-card v-else-if="activeMenuItem == 1" flat>
                    <v-card-title class="pa-1">Alignment</v-card-title>
                    <div class="d-flex ma-4">
                      <div class="control-panel">
                        <v-btn-toggle v-model="activeAlignMode">
                          <v-btn v-for="n in 6" :key="n">
                            <v-img
                              src="../../../../assets/images/pos_align_0.png"
                              aspect-ratio="1"
                            />
                          </v-btn>
                        </v-btn-toggle>

                        <v-checkbox
                          v-model="alignOrder"
                          label="Left-Right"
                          color="primary"
                          value="left-right"
                          hide-details
                        ></v-checkbox>
                        <v-checkbox
                          v-model="alignOrder"
                          label="Up-Down"
                          color="primary"
                          value="up-down"
                          hide-details
                        ></v-checkbox>
                        <v-checkbox
                          v-model="alignOrder"
                          label="Descending Order"
                          color="primary"
                          value="descending-order"
                          hide-details
                        ></v-checkbox>

                        <v-select
                          v-model="activeAlignDirection"
                          :items="alignDirections"
                          class="my-4"
                          dense
                          solo
                          style="max-width: 60% !important"
                        ></v-select>

                        <v-row class="mr-4">
                          <v-col cols="6">
                            <v-text-field
                              class="range-field"
                              label="Row"
                              type="number"
                              outlined
                              dense
                            />
                          </v-col>
                          <v-col cols="6">
                            <v-text-field
                              class="range-field"
                              label="Column"
                              type="number"
                              outlined
                              dense
                            />
                          </v-col>
                        </v-row>
                      </div>
                      <v-img
                        src=""
                        class="black-border"
                        width="350"
                        height="350"
                        fill
                      />
                    </div>
                  </v-card>

                  <!-- Bonding -->
                  <v-card v-else-if="activeMenuItem == 2" flat>
                    <v-card-title class="pa-1">Bonding</v-card-title>
                    <div class="d-flex">
                      <div class="control-panel"></div>
                      <v-img
                        src=""
                        class="black-border"
                        width="350"
                        height="350"
                        fill
                      />
                    </div>
                  </v-card>

                  <!-- Shading -->
                  <v-card v-else-if="activeMenuItem == 3" flat>
                    <v-card-title class="pa-1">Shading</v-card-title>
                    <div class="d-flex">
                      <div class="control-panel"></div>
                      <v-img
                        src=""
                        class="black-border"
                        width="350"
                        height="350"
                        fill
                      />
                    </div>
                  </v-card>

                  <!-- Display -->
                  <v-card v-else-if="activeMenuItem == 4" flat>
                    <v-card-title class="pa-1">Display</v-card-title>
                    <div class="d-flex">
                      <div class="control-panel"></div>
                      <v-img
                        src=""
                        class="black-border"
                        width="350"
                        height="350"
                        fill
                      />
                    </div>
                  </v-card>
                </v-col>
              </v-row>
            </v-sheet>
          </v-tab-item>
          <v-tab-item value="tabs-metadata" class="v-tab-item">
            <v-sheet
              class="drop pa-5"
              height="600"
              :class="getClasses"
              @dragover.prevent="dragOver"
              @dragleave.prevent="dragLeave"
              @drop.prevent="drop($event)"
            >
              <div
                v-if="!files.length"
                class="d-flex align-center justify-center fill-height"
              >
                <p class="text-h4 grey--text text--lighten-2">{{ backgroundText }}</p>
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
              height="600"
              :class="getClasses"
              @dragover.prevent="dragOver"
              @dragleave.prevent="dragLeave"
              @drop.prevent="drop($event)"
              v-on:mouseup="selectExampleString"
            >
              <div
                v-if="files.length == 0"
                class="d-flex align-center justify-center fill-height"
              >
                <p class="text-h4 grey--text text--lighten-2">{{ backgroundText }}</p>
              </div>
              <div v-else>
                <v-row class="justify-center mx-5">
                  <div
                    class="d-flex align-center justify-center"
                    style="width: calc(100% - 70px);"
                  >
                    <v-row class="align-center justify-center">
                      <p class="mb-0 mr-8">Example</p>
                      <div
                        ref="exampleBox"
                        class="d-flex example-string"
                        v-html="exampleFileName"
                        v-on:mouseup="selectExampleString"
                      ></div>
                    </v-row>
                  </div>
                  <v-select
                    v-model="selectedFileName"
                    :items="fileNames"
                    class="filenames-list"
                    flat
                  >
                  </v-select>
                </v-row>
                <v-row class="align-center justify-center name-type-input">
                  <div
                    class="pattern-section"
                    v-for="(pattern, idx) in namePatterns"
                    :key="idx"
                  >
                    <v-btn
                      class="pattern-item-button"
                      :color="pattern.color"
                      small
                      dark
                      @click="clickNamePattern(idx)"
                    >
                      {{ pattern.label }}
                    </v-btn>
                    <v-text-field
                      class="pattern-item-button"
                      v-model="namePatterns[idx].text"
                      solo
                    ></v-text-field>
                  </div>
                </v-row>
              </div>
              <v-card v-if="files.length > 0">
                <v-card-title class="v-card-title">
                  <v-btn
                    class="common"
                    :disabled="!canUpdate"
                    depressed
                    color="primary"
                  >
                    Update
                  </v-btn>
                  <v-spacer class="type-spacer"></v-spacer>
                  <v-btn
                    class="common"
                    :disabled="!canClear"
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
                  class="name-type-table"
                  :headers="nameTypeTableHeaders"
                  :items="nameTypeTableContents"
                  :search="searchNameType"
                  :single-select="false"
                  item-key="no"
                  height="300"
                  fixed-header
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
import { createNamespacedHelpers } from "vuex";
import {
  getFileName,
  checkFileType,
  enumerateDirectory,
  isOverlapped,
  loadImage
} from "../../../../utils/utils-func";
import SimpleDialog from "../../../custom/SimpleDialog";

const positionModule = createNamespacedHelpers("files/position");

export default {
  name: "OpenPositionDialog",

  components: { SimpleDialog },

  data: () => ({
    loading: false,

    isDragging: false,
    selectedTab: null,

    tilingMenus: [
      "Edit",
      "Alignment",
      "Bonding",
      "Shading",
      "Display",
      "Result",
      "Option"
    ],
    tilingCanvas: null,

    activeMenuItem: 0,
    activeAlignMode: null,
    alignOrder: [],
    alignDirections: ["Clockwise", "Counter-Clockwise"],
    activeAlignDirection: "Counter-Clockwise",
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
      { text: "SizeZ", value: "size_z", sortable: false }
    ],

    // Names & Types Tab
    curNameIdx: -1,
    searchNameType: "",
    selectedNameContents: [],
    selectedFileName: "",
    selectionRange: {
      text: "",
      startOffset: -1,
      endOffset: -1
    },
    namePatterns: [
      { label: "Series", text: "", start: -1, end: -1, color: "success" },
      { label: "Row", text: "", start: -1, end: -1, color: "primary" },
      { label: "Column", text: "", start: -1, end: -1, color: "deep-orange" },
      { label: "Field", text: "", start: -1, end: -1, color: "warning" },
      { label: "View Method", text: "", start: -1, end: -1, color: "purple" },
      { label: "Z Position", text: "", start: -1, end: -1, color: "blue-grey" },
      { label: "Time Point", text: "", start: -1, end: -1, color: "error" }
    ],
    nameTypeTableHeaders: [
      { text: "No", value: "no" },
      { text: "FileName", value: "filename" },
      { text: "Series", value: "series" },
      { text: "Row", value: "row" },
      { text: "Column", value: "column" },
      { text: "Field", value: "field" },
      { text: "View Method", value: "viewMethod" },
      { text: "Z Position", value: "zPosition" },
      { text: "Time Point", value: "timepoint" }
    ]
  }),

  created() {
    this.newResWatch = this.$store.watch(
      (state, getters) => getters["image/newRes"],
      res => {
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
              metadata: res[key]
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
      res => {
        this.allFiles = res;
      }
    );

    this.filesWatch = this.$store.watch(
      (state, getters) => getters["files/position/getFiles"],
      files => {
        if (files.length) {
          this.selectedFileName = files[0].name;

          if (this.tilingCanvas) {
            this.drawImages();
          }
        }
      }
    );
  },

  beforeDestroy() {
    this.newResWatch();
    this.allFilesWatch();

    this.filesWatch();
  },

  props: {
    value: {
      type: Boolean,
      default: false
    }
  },

  computed: {
    ...positionModule.mapGetters({
      files: "getFiles"
    }),

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

    backgroundText() {
      return this.loading ? "Loading..." : "Drag and drop files or a folder"
    },

    fileNames() {
      let filename_array = [];
      this.files.forEach(file => {
        filename_array.push(file.name);
      });

      return filename_array;
    },

    exampleFileName() {
      let fileNameOnly = getFileName(this.selectedFileName);
      var html = "",
        start = 0,
        str = "";

      const patterns = this.namePatterns
        .filter(n => n.start > -1)
        .map(n => Object.assign({}, n));
      for (var i = 0; i < patterns.length; i++) {
        for (var j = i + 1; j < patterns.length; j++) {
          if (patterns[i].start > patterns[j].start) {
            var temp = patterns[i];
            patterns[i] = patterns[j];
            patterns[j] = temp;
          }
        }

        if (patterns[i].start > 0) {
          str = fileNameOnly.substring(start, patterns[i].start);
          html += `<pre>${str}</pre>`;
        }
        str = fileNameOnly.substring(patterns[i].start, patterns[i].end);
        html += `<pre class="${patterns[i].color}--text">${str}</pre>`;

        start = patterns[i].end;
      }

      str = fileNameOnly.substring(start, fileNameOnly.length);
      html += `<pre>${str}</pre>`;

      return html;
    },

    canUpdate() {
      return this.namePatterns.filter(n => n.start > -1).length > 0;
    },

    canClear() {
      return this.namePatterns.filter(n => n.start > -1).length > 0;
    },

    nameTypeTableContents() {
      const contents = [];
      for (let file of this.files) {
        if (file.name) {
          const nameType = this.getNameType(getFileName(file.name));
          contents.push({
            no: contents.length + 1,
            filename: file.name,
            ...nameType
          });
        }
      }
      return contents;
    },

    getMetaContents() {
      const contents = [];
      this.allFiles.forEach(file => {
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
          size_z: ""
        });
      });
      return contents;
    }
  },

  methods: {
    // Mapping actions from Position store
    ...positionModule.mapActions([
      "setFiles",
      "clearFiles",
      "addFile"
    ]),

    // Tab change
    async onTabChange(tabIdx) {
      if (tabIdx == 'tabs-tiling') {
        if (this.tilingCanvas == null) {
          let c = document.getElementById('canvas');
          this.tilingCanvas = c.getContext('2d');

          this.tilingCanvas.canvas.width = 1000;
          this.tilingCanvas.canvas.height = 1000;
        }

        this.drawImages();
      }
    },
    async drawImages() {
      if (this.files && this.files.length) {
        this.tilingCanvas.clearRect(0, 0, this.tilingCanvas.canvas.width, this.tilingCanvas.canvas.height);

        for (var i = 0; i < this.files.length; i++ ) {
          let imageURL = await loadImage(this.files[i].imageData);
          this.tilingCanvas.drawImage(imageURL, i * 100, 0, 100, 100);
        }
      }
    },

    // Drag&Drop files or folder
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
          this.loading = true;
          this.traverseFileTree(item);
        }
      }
    },
    traverseFileTree(item, path) {
      let self = this;
      path = path || "";
      if (item.isFile) {
        item.file(function(file) {
          if (checkFileType(file.name)) {
            self.addFile(file);
          }
        });
        self.loading = false;
      } else if (item.isDirectory) {
        enumerateDirectory(item).then(entries => {
          entries = entries.sort(function(a, b) {
            return a.name.localeCompare(b.name, undefined, {
              numeric: true,
              sensitivity: 'base'
            });
          });

          for (let i = 0; i < entries.length; i++) {
            self.traverseFileTree(entries[i], path + item.name + "/");
          }
          self.loading = false;
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

    // Select example string in names&types tab
    selectExampleString(e) {/* eslint-disable-line */
      if (typeof window.getSelection != "undefined") {
        try {
          let sel = window.getSelection(),
            range = sel.getRangeAt(0);
          let selectionRect = range.getBoundingClientRect(),
            fullRect = this.$refs.exampleBox.getBoundingClientRect();

          this.selectionRange.text = range.toString();

          this.selectionRange.startOffset = Math.round(
            ((selectionRect.left - fullRect.left) / selectionRect.width) *
              range.toString().length
          );
          this.selectionRange.endOffset =
            this.selectionRange.startOffset + range.toString().length;
        } catch (error) {
          console.log(error);
        }
      }
    },

    // Click select button
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

    // Click close button
    onClose() {
      this.visibleDialog = false;
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

    clickNamePattern(index) {
      const { text, startOffset, endOffset } = this.selectionRange;
      let selectedText = this.getSelectionText();

      if (text != "" && selectedText != "") {
        if (text == selectedText) {
          if (startOffset > -1 && endOffset > -1) {
            const patterns = this.namePatterns.filter(n => n.start > -1);
            for (var i = 0; i < patterns.length; i++) {
              if (
                isOverlapped(
                  [patterns[i].start, patterns[i].end],
                  [startOffset, endOffset]
                )
              )
                break;
            }

            if (i == patterns.length) {
              this.namePatterns[index].text = text;
              this.namePatterns[index].start = startOffset;
              this.namePatterns[index].end = endOffset;
            }
          }
        }
      }
    },

    getSelectionText() {
      var text = "";
      if (window.getSelection) {
        text = window.getSelection().toString();
      } else if (document.selection && document.selection.type != "Control") {
        text = document.selection.createRange().text;
      }
      return text.replaceAll("\n", "");
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
        reader.onload = function() {
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

    // clear
    clearNameType() {
      this.namePatterns.forEach(pattern => {
        pattern.start = -1;
        pattern.end = -1;
        pattern.text = "";
      });
    },

    getNameType(filename) {
      return {
        series: this.getPatternValue(0, filename),
        row: this.getPatternValue(1, filename),
        column: this.getPatternValue(2, filename),
        field: this.getPatternValue(3, filename),
        viewMethod: this.getPatternValue(4, filename),
        zPosition: this.getPatternValue(5, filename),
        timepoint: this.getPatternValue(6, filename)
      };
    },

    getPatternValue(index, filename) {
      const pattern = this.namePatterns[index];
      return pattern.start == -1
        ? ""
        : filename.substring(pattern.start, pattern.end);
    }
  }
};
</script>

<style scoped>
.isDragging {
  background-color: #e0f2f1;
  border-color: #fff;
}

.control-panel {
  width: calc(100% - 350px);
}

.black-border {
  width: calc(100% - 350px);
  height: 450px;
  border: 1px solid #333;
}

/*.name-center {
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
*/
.pattern-section {
  width: 14.2%;
  padding: 5px;
}
.pattern-item-button {
  width: 100%;
  text-transform: none;
}
.pattern-item-button >>> input {
  width: 100%;
  text-align: center;
}
.pattern-item-button >>> label {
  width: 100%;
  text-align: center;
}
.pattern-item-button >>> .v-input__control {
  min-height: 30px !important;
}
.example-string >>> pre {
  font-size: 1.2em;
  font-weight: bold;
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
.filenames-list.v-select >>> .v-select__selections {
  display: none !important;
}
.filenames-list.v-select >>> .v-input__slot:before,
.filenames-list.v-select >>> .v-input__slot:after {
  border-style: none;
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
