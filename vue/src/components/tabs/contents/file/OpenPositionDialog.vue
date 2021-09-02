<template>
  <div class="d-none">
    <v-dialog v-model="visibleDialog" persistent>
      <!-- <simple-dialog
        title="Position"
        ok-title="Select"
        :single-button="false"
        :select-disable="!this.allFiles.length"
        @select="onSelect"
        @close="onClose"
      > -->
      <v-card>
        <!-- <v-card-title class="text-h5">
          Position
        </v-card-title> -->

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
                <p class="text-h4 grey--text text--lighten-2">
                  {{ backgroundText }}
                </p>
              </div>
              <v-row v-else class="align-center">
                <v-col
                  v-for="(file, idx) in files"
                  :key="idx"
                  cols="2"
                  class="px-4"
                >
                  <img
                    :id="'images_' + idx"
                    :src="file.imageData.src"
                    class="mx-auto"
                  />
                  <p class="ma-2 text-center text-caption">
                    {{ file.name }}
                  </p>
                </v-col>
              </v-row>
            </v-sheet>
          </v-tab-item>
          <v-tab-item value="tabs-tiling" class="v-tab-item" eager>
            <Tiling />
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
                <p class="text-h4 grey--text text--lighten-2">
                  {{ backgroundText }}
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
            >
              <!-- @mouseup="selectExampleString" -->
              <div
                v-if="files.length == 0"
                class="d-flex align-center justify-center fill-height"
              >
                <p class="text-h4 grey--text text--lighten-2">
                  {{ backgroundText }}
                </p>
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
                        @mouseup="selectExampleString"
                        v-html="exampleFileName"
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
                    v-for="(pattern, idx) in namePatterns"
                    :key="idx"
                    class="pattern-section"
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
                      v-model="namePatterns[idx].text"
                      class="pattern-item-button"
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
                    @click="updateNameType"
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

        <v-card-actions>
          <v-progress-linear
            :style="{
              visibility: progressBarPercent < 100 ? 'visible' : 'hidden'
            }"
            color="light-blue"
            height="10"
            width="300"
            :value="progressBarPercent"
            striped
            class="progress-bar"
          ></v-progress-linear>

          <v-spacer></v-spacer>
          <v-btn
            color="green darken-1"
            :disabled="!this.allFiles.length"
            text
            @click="onSelect"
          >
            OK
          </v-btn>

          <v-btn color="green darken-1" text @click="onClose">
            CANCEL
          </v-btn>
        </v-card-actions>
      </v-card>
      <!-- </simple-dialog> -->
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
// import SimpleDialog from "../../../custom/SimpleDialog";

const positionModule = createNamespacedHelpers("files/position");

import { getPosition, getSeries } from "../../../../vuex/modules/files";
// import OpenPositionViewTab from "./OpenPositionViewTab";
import Tiling from "./Tiling.vue";

var createNewPage = true;

export default {
  name: "OpenPositionDialog",

  components: {
    Tiling
  },

  props: {
    value: {
      type: Boolean,
      default: false
    }
  },

  data: () => ({
    // ctxHeight,
    // ctxWidth,
    // canvasWidth,
    // canvasHeight,
    // mouseX,
    // mouseY;
    // loading: false,
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
    tilingAlignButtons: [
      "Cascade",
      "Height Decreasing",
      "Height Increasing",
      "By XYZ",
      "By Columns",
      "By Rows"
    ],
    tilingAlignDirections: ["Clockwise", "Counter-Clockwise"],

    tiling: {
      // 平铺图片界面参数设置
      preview: null,
      activeMenuItem: 0,
      bonding: {
        activeadsorption: -1
      },
      edit: {
        activeFileItem: -1,
        oldFileItem: -1
      },
      alignment: {
        activeMode: 5,
        orders: [],
        activeDirection: "Counter-Clockwise",
        rows: null,
        cols: null,
        border: 0,
        gapX: 0,
        gapY: 0,
        disables: [
          // alignment control enable/disable
          {
            chkLR: true,
            chkUD: true,
            chkDO: true,
            txtRows: true,
            txtCols: true,
            txtBorder: false,
            txtGapX: true,
            txtGapY: true
          },
          {
            chkLR: true,
            chkUD: true,
            chkDO: true,
            txtRows: true,
            txtCols: true,
            txtBorder: false,
            txtGapX: false,
            txtGapY: false
          },
          {
            chkLR: true,
            chkUD: true,
            chkDO: true,
            txtRows: true,
            txtCols: true,
            txtBorder: false,
            txtGapX: false,
            txtGapY: false
          },
          {
            chkLR: false,
            chkUD: false,
            chkDO: false,
            txtRows: false,
            txtCols: false,
            txtBorder: false,
            txtGapX: false,
            txtGapY: false
          },
          {
            chkLR: false,
            chkUD: false,
            chkDO: false,
            txtRows: false,
            txtCols: true,
            txtBorder: false,
            txtGapX: false,
            txtGapY: false
          },
          {
            chkLR: false,
            chkUD: false,
            chkDO: false,
            txtRows: true,
            txtCols: false,
            txtBorder: false,
            txtGapX: false,
            txtGapY: false
          }
        ]
      }
    },
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
      { label: "Series", text: "", start: 0, end: 17, color: "success" },
      { label: "Row", text: "", start: 24, end: 25, color: "primary" },
      { label: "Column", text: "", start: 25, end: 27, color: "deep-orange" },
      { label: "Field", text: "", start: 27, end: 30, color: "warning" },
      { label: "Channel", text: "", start: 30, end: 32, color: "purple" },
      { label: "Z Position", text: "", start: 22, end: 23, color: "blue-grey" },
      { label: "Time Point", text: "", start: 18, end: 21, color: "error" }
    ],
    nameTypeTableHeaders: [
      { text: "No", value: "no" },
      { text: "FileName", value: "filename" },
      { text: "Series", value: "series" },
      { text: "Row", value: "row" },
      { text: "Column", value: "col" },
      { text: "Field", value: "field" },
      { text: "Channel", value: "channel" },
      { text: "Z Position", value: "z" },
      { text: "Time Point", value: "timeline" }
    ],
    progressBarValue: 0,
    progressBarMaxValue: 0,
    luminance: 0.0
  }),

  mutations: {
    setProgressBarValue(state, v) {
      state.progressBarValue = v;
    }
  },

  created() {
    this.filesWatch = this.$store.watch(
      (state, getters) => getters["files/position/getFiles"],
      async files => {
        if (files.length) {
          this.selectedFileName = files[0].name;
        }
      }
    );

    this.newResWatch = this.$store.watch(
      (state, getters) => getters["image/newRes"],
      res => {
        let filteredData = new Map();
        const payload = {
          files: filteredData,
          appendToCurrentPage: false
        };

        payload.appendToCurrentPage = !createNewPage;
        createNewPage = false;
        for (var key in res) {
          const idx = parseInt(key.split("_")[1]);
          let fileName = this.allFiles[idx].name;
          let p = getPosition(fileName);
          if (
            key.startsWith("position_") &&
            res[key] &&
            idx < this.allFiles.length
          ) {
            let extParams = {
              row: p.row,
              col: p.col,
              z: p.z,
              timeline: p.timeline,
              objective: 4
            };

            let metadata = res[key];
            if (metadata.imageInfo.objective) {
              let X = 4;
              const cm = metadata.imageInfo.objective.calibratedMagnification;
              const nm = metadata.imageInfo.objective.nominalMagnification;

              if (cm && nm) {
                X = cm > nm ? cm : nm;
              } else if (cm && !nm) {
                X = cm;
              } else if (!cm && nm) {
                X = nm;
              }
              extParams.objective = X;
            }

            filteredData.set(idx, {
              filename: fileName,
              metadata: res[key],
              extParams: extParams
            });
          }
        }
        if (filteredData.size > 0) {
          this.$store.dispatch("image/addData", payload);
        }
        // this.newFile = null;
        // this.imageData = null;
      }
    );
  },

  beforeDestroy() {
    this.newResWatch();
    // this.allFilesWatch();
    this.filesWatch();
  },

  computed: {
    ...positionModule.mapGetters({
      files: "getFiles",
      filesSortByField: "getFilesSortByField",
      channelOptions: "getChannelOptions"
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
      return this.loading ? "Loading..." : "Drag and drop files or a folder";
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
          let p = getPosition(file.name);
          if (p.series.length > 0) {
            // convert 1, 2, 3 to A, B, C
            p.row = String.fromCharCode("A".charCodeAt() + p.row - 1);
            contents.push({
              no: contents.length + 1,
              filename: file.name,
              ...p
            });
          } else {
            contents.push({
              no: contents.length + 1,
              filename: file.name
            });
          }
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
    },

    progressBarPercent() {
      if (this.progressBarMaxValue != 0) {
        return (100 * this.progressBarValue) / this.progressBarMaxValue;
      }
      return 100;
    }
  },

  methods: {
    // Mapping actions from Position store
    ...positionModule.mapActions([
      "setFiles",
      "clearFiles",
      "addFile",
      "setNamePattern",
      "addMetaData",
      "changeSelectsByRowCol",
      "changeSelectsByObjectLense",
      "changeSelectsByZ",
      "changeSelectsByTimeline",
      "changeSelectsByChannels"
    ]),

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

      this.allFiles = [];
      this.clearFiles();
      let items = e.dataTransfer.items;

      this.progressBarValue = 0;
      this.progressBarMaxValue = 0;

      for (let i = 0; i < items.length; i++) {
        let item = items[i].webkitGetAsEntry();
        if (item) {
          let thiz = this;
          this.traverseFileTree(item, "", function() {
            thiz.progressBarValue++;
          });
        }
      }
      this.resetConfig();
    },
    traverseFileTree(item, path, doneCB) {
      let self = this;
      path = path || "";
      if (item.isFile) {
        item.file(function(file) {
          if (checkFileType(file.name)) {
            self.progressBarMaxValue++;

            self.addFile({
              file: file,
              doneCB: doneCB
            });
            self.allFiles.push(file);
          }
        });
        self.loading = false;
      } else if (item.isDirectory) {
        //   enumerateDirectory(item).then(entries => {
        //     entries = entries.sort(function(a, b) {
        //       return a.name.localeCompare(b.name, undefined, {
        //         numeric: true,
        //         sensitivity: "base"
        //       });
        //     });
        //     for (let i = 0; i < entries.length; i++) {
        //       self.traverseFileTree(entries[i], path + item.name + "/");
        //     }
        //     self.loading = false;
        //   });
      }
    },
    resetConfig() {
      this.imageWidth = 0;
      this.imageHeight = 0;
      this.tiling.edit.activeFileItem = -1;
      this.tiling.edit.oldFileItem = -1;
    },

    // Tab change (Tiling tab)
    async onTabChange(tabIdx) {
      if (tabIdx == "tabs-tiling") {
      }
    },

    // Select example string in names&types tab
    selectExampleString() {
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
        console.log(this.allFiles);
        return "";
      }

      // let formData = new FormData();
      // const name = this.getMainName();
      // if (name) {
      //   this.allFiles.forEach((file, idx) => {
      //     const series = getSeries(file.name);
      //     if(series == name) {
      //       formData.append("position_" + idx, file);
      //     }
      //   });
      // } else {
      //   formData.append("position_0", this.allFiles[0]);
      // }
      // this.$store.dispatch("image/setNewFiles", formData);
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
        if (this.allFiles[idx].name) {
          const name = getSeries(this.allFiles[idx].name);

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

    updateNamePattern(fileName) {
      for (let i = 0; i < this.namePatterns.length; i++) {
        var key = null;
        switch (i) {
          case 0:
            key = "series";
            break;
          case 1:
            key = "row";
            break;
          case 2:
            key = "col";
            break;
          case 3:
            key = "field";
            break;
          case 4:
            key = "channel";
            break;
          case 5:
            key = "z";
            break;
          case 6:
            key = "time";
            break;
        }
        if (key) {
          this.setNamePattern({
            key: key,
            pos: [this.namePatterns[i].start, this.namePatterns[i].end]
          });
        }
      }
      if (fileName) {
        this.setNamePattern({
          key: "totalLen",
          pos: fileName.length
        });
      }
    },

    // update
    updateNameType() {
      let MAX_BATCH_SIZE = 10;

      this.updateNamePattern(this.selectedFileName);

      if (!this.allFiles) {
        console.log("allFiles error: " + this.allFiles);
        return "";
      }
      let thiz = this;
      this.progressBarValue = 0;
      this.progressBarMaxValue = this.allFiles.length;
      for (let i in this.allFiles) {
        let p = getPosition(this.allFiles[i].name);
        this.addMetaData({
          index: i,
          metaData: {
            row: p.row,
            col: p.col,
            z: p.z,
            timeline: p.timeline,
            channel: p.channel,
            objectLense: 4 // The default object lense for name & type
          },
          doneCB: function() {
            thiz.progressBarValue++;
            console.log(
              thiz.progressBarValue + " / " + thiz.progressBarMaxValue
            );
          }
        });
      }
      if (this.allFiles.length > 0) {
        let defaultSelected = this.files[0];
        this.changeSelectsByRowCol({
          row: defaultSelected.metaData.row,
          col: defaultSelected.metaData.col
        });
        this.changeSelectsByObjectLense(defaultSelected.metaData.objectLense);
        this.changeSelectsByZ(defaultSelected.metaData.z);
        this.changeSelectsByTimeline(defaultSelected.metaData.timeline);
        this.changeSelectsByChannels(this.channelOptions);
      }

      return;

      // Remove bioformat.
      createNewPage = true;
      let formData = new FormData();
      const mainName = this.getMainName();
      let count = 0;
      if (mainName) {
        this.allFiles.forEach((file, idx) => {
          const name = getSeries(file.name);

          if (mainName == name) {
            formData.append("position_" + idx, file);
            count++;
          }

          if (count >= MAX_BATCH_SIZE) {
            this.$store.dispatch("image/setNewFiles", formData);
            formData = new FormData();
            count = 0;
          }
        });
      } else {
        formData.append("position_0", this.allFiles[0]);
        count++;
      }

      if (count > 0) {
        this.$store.dispatch("image/setNewFiles", formData);
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
.progress-bar {
  width: 300pt;
}
</style>
