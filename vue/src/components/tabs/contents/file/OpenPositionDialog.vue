<template>
  <div class="d-none">
    <v-dialog 
      v-model="visibleDialog" 
      persistent
    >
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
                    :src="file.imageData"
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
                        v-model="tiling.activeMenuItem"
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
                  <div class="d-flex ma-2">
                    <!-- Tiling Control Panel -->
                    <div class="control-panel">
                      <!-- Editing -->
                      <v-card v-if="tiling.activeMenuItem == 0" flat>
                        <v-card-title class="pa-1">Editing</v-card-title>
                        <div class="inside">
                          <v-list
                            class="overflow-y-auto fill-height"
                            max-height="450"
                            outlined
                          >
                            <v-list-item-group
                              v-if="files.length"
                              v-model="tiling.edit.activeFileItem"
                              color="green"
                              @change="pickImageFile"
                            >
                              <v-list-item
                                v-for="(file, idx) in files"
                                :key="idx"
                              >
                                <v-list-item-content>
                                  <v-list-item-title
                                    v-text="file.name"
                                  ></v-list-item-title>
                                </v-list-item-content>
                              </v-list-item>
                            </v-list-item-group>
                            <span v-else>
                              <v-list-item>
                                <v-list-item-content>
                                  <v-list-item-title
                                    >No Image Files!</v-list-item-title
                                  >
                                </v-list-item-content>
                              </v-list-item>
                            </span>
                          </v-list>
                        </div>
                      </v-card>
                      <!-- Alignment -->
                      <v-card v-else-if="tiling.activeMenuItem == 1" flat>
                        <v-card-title class="pa-1">Alignment</v-card-title>
                        <div class="inside">
                          <v-btn-toggle
                            v-model="tiling.alignment.activeMode"
                            mandatory
                            @change="changeAlignMode"
                          >
                            <v-tooltip v-for="n in 6" :key="n" bottom>
                              <template v-slot:activator="{ on, attrs }">
                                <v-btn :key="n" :disabled="n == 4">
                                  <v-img
                                    :src="alignButtonImage(n)"
                                    aspect-ratio="1"
                                    v-bind="attrs"
                                    :style="
                                      n == 4 ? { filter: 'grayscale(1)' } : {}
                                    "
                                    v-on="on"
                                  />
                                </v-btn>
                              </template>
                              <span>{{ tilingAlignButtons[n - 1] }}</span>
                            </v-tooltip>
                          </v-btn-toggle>

                          <v-checkbox
                            v-model="tiling.alignment.orders"
                            label="Left-Right"
                            color="primary"
                            value="left-right"
                            hide-details
                            :disabled="
                              tiling.alignment.disables[
                                tiling.alignment.activeMode
                              ].chkLR
                            "
                            @change="changeAlignOrder"
                          ></v-checkbox>
                          <v-checkbox
                            v-model="tiling.alignment.orders"
                            label="Up-Down"
                            color="primary"
                            value="up-down"
                            hide-details
                            :disabled="
                              tiling.alignment.disables[
                                tiling.alignment.activeMode
                              ].chkUD
                            "
                            @change="changeAlignOrder"
                          ></v-checkbox>
                          <v-checkbox
                            v-model="tiling.alignment.orders"
                            label="Descending Order"
                            color="primary"
                            value="descending-order"
                            hide-details
                            :disabled="
                              tiling.alignment.disables[
                                tiling.alignment.activeMode
                              ].chkDO
                            "
                            @change="changeAlignOrder"
                          ></v-checkbox>

                          <!-- <v-select
                            v-model="tiling.alignment.activeDirection"
                            :items="tilingAlignDirections"
                            class="my-4"
                            dense
                            solo
                            style="max-width: 60% !important"
                          ></v-select> -->

                          <v-row class="mt-4 mr-4">
                            <v-col cols="6">
                              <v-text-field
                                v-model="tiling.alignment.rows"
                                :value="tiling.alignment.rows"
                                class="range-field"
                                label="Row"
                                type="number"
                                outlined
                                dense
                                :disabled="
                                  tiling.alignment.disables[
                                    tiling.alignment.activeMode
                                  ].txtRows
                                "
                                @input="inputTilingRows"
                              />
                            </v-col>
                            <v-col cols="6">
                              <v-text-field
                                v-model="tiling.alignment.cols"
                                class="range-field"
                                label="Column"
                                type="number"
                                outlined
                                dense
                                :disabled="
                                  tiling.alignment.disables[
                                    tiling.alignment.activeMode
                                  ].txtCols
                                "
                                @input="inputTilingCols"
                              />
                            </v-col>
                          </v-row>

                          <v-row class="mr-4">
                            <v-col cols="4">
                              <v-text-field
                                v-model="tiling.alignment.border"
                                class="range-field"
                                label="Border"
                                type="number"
                                outlined
                                dense
                                :disabled="
                                  tiling.alignment.disables[
                                    tiling.alignment.activeMode
                                  ].txtBorder
                                "
                                @change="inputTilingBorder"
                              />
                            </v-col>
                            <v-col cols="4">
                              <v-text-field
                                v-model="tiling.alignment.gapX"
                                class="range-field"
                                label="Gap X"
                                type="number"
                                outlined
                                dense
                                :disabled="
                                  tiling.alignment.disables[
                                    tiling.alignment.activeMode
                                  ].txtGapX
                                "
                                @change="inputTilingGapX"
                              />
                            </v-col>
                            <v-col cols="4">
                              <v-text-field
                                v-model="tiling.alignment.gapY"
                                class="range-field"
                                label="Gap Y"
                                type="number"
                                outlined
                                dense
                                :disabled="
                                  tiling.alignment.disables[
                                    tiling.alignment.activeMode
                                  ].txtGapY
                                "
                                @change="inputTilingGapY"
                              />
                            </v-col>
                          </v-row>
                        </div>
                      </v-card>
                      <!-- Bonding -->
                      <v-card v-else-if="tiling.activeMenuItem == 2" flat>
                        <v-card-title class="pa-1">Bonding</v-card-title>
                        <div class="inside"></div>
                      </v-card>
                      <!-- Shading -->
                      <v-card v-else-if="tiling.activeMenuItem == 3" flat>
                        <v-card-title class="pa-1">Shading</v-card-title>
                        <div class="inside"></div>
                      </v-card>
                      <!-- Display -->
                      <v-card v-else-if="tiling.activeMenuItem == 4" flat>
                        <v-card-title class="pa-1">Display</v-card-title>
                        <div class="inside"></div>
                      </v-card>
                      <!-- Result -->
                      <v-card v-else-if="tiling.activeMenuItem == 5" flat>
                        <v-card-title class="pa-1">Result</v-card-title>
                        <div class="inside"></div>
                      </v-card>
                      <!-- Option -->
                      <v-card v-else-if="tiling.activeMenuItem == 6" flat>
                        <v-card-title class="pa-1">Option</v-card-title>
                        <div class="inside"></div>
                      </v-card>
                    </div>

                    <!-- Tiling Preview -->
                    <canvas id="canvas" class="mt-15 canvas"></canvas>
                  </div>
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
              @mouseup="selectExampleString"
            >
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
            :style="{visibility: progressBarPercent < 100 ? 'visible' : 'hidden'}" 
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

          <v-btn
            color="green darken-1"
            text
            @click="onClose"
          >
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
import {
  POSITION_DIALOG_CANVAS_MAX_PIXEL,
  POSITION_DIALOG_COL_COUNT,
  POSITION_DIALOG_CELL_SIZE
  // POSITION_DIALOG_STROKE_WIDTH
} from "../../../../utils/constants";
// import SimpleDialog from "../../../custom/SimpleDialog";

const positionModule = createNamespacedHelpers("files/position");

import { getPosition, getSeries } from "../../../../vuex/modules/files";

var createNewPage = true;

export default {
  name: "OpenPositionDialog",

  components: { },

  props: {
    value: {
      type: Boolean,
      default: false
    }
  },

  data: () => ({
    // loading: false,
    isDragging: false,
    selectedTab: null,

    imageWidth: 0,
    imageHeight: 0,

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
      preview: null,
      activeMenuItem: 0,
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
      { text: "Column", value: "column" },
      { text: "Field", value: "field" },
      { text: "Channel", value: "viewMethod" },
      { text: "Z Position", value: "zPosition" },
      { text: "Time Point", value: "timepoint" }
    ],
    progressBarValue: 0,
    progressBarMaxValue: 0
  }),

  mutations: {
    setProgressBarValue(state, v) {
      state.progressBarValue = v;
    }
  },

  created() {
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
              row: p[0],
              col: p[1],
              z: p[2],
              timeline: p[3],
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
    // this.allFilesWatch = this.$store.watch(
    //   (state, getters) => getters["image/currentPageData"],
    //   res => {
    //     console.log("allFilesWatch !!!!");
    //     console.log(res);
    //     this.allFiles = res;
    //   }
    // );

    this.filesWatch = this.$store.watch(
      (state, getters) => getters["files/position/getFiles"],
      async files => {
        if (files.length) {
          this.selectedFileName = files[0].name;

          if (this.tiling.preview) {
            await this.getImageSize();
            this.drawImages();
          }
        }
      }
    );

    /* this.filesWatch = this.$store.watch(
      (state, getters) => getters["files/position/getFiles"],
      async files => {
        if (files.length) {
          this.selectedFileName = files[0].name;

          if (this.tiling.preview) {
            await this.getImageSize();
            this.drawImages();
          }
        }
      }
    ); */
  },

  beforeDestroy() {
    this.newResWatch();
    // this.allFilesWatch();
    this.filesWatch();
  },

  computed: {
    ...positionModule.mapGetters({
      files: "getFiles",
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

    alignButtonImage() {
      return index =>
        require(`../../../../assets/images/pos_align_${index - 1}.png`);
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
    },

    progressBarPercent() {
      if(this.progressBarMaxValue != 0) {
        return 100 * this.progressBarValue / this.progressBarMaxValue;
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
            thiz.progressBarValue ++;
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
            self.progressBarMaxValue ++;

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
        if (this.tiling.preview == null) {
          let c = document.getElementById("canvas");
          this.tiling.preview = c.getContext("2d");
        }

        if (this.files && this.files.length) {
          await this.getImageSize();
          this.drawImages();
        }
      }
    },

    async getImageSize() {
      let image = await loadImage(this.files[0].imageData);

      this.imageWidth = image.width;
      this.imageHeight = image.height;
    },
    // Tiling preview
    drawImages() {
      if (this.files && this.files.length) {
        switch (this.tiling.alignment.activeMode) {
          case 0:
            this.drawCascade();
            break;
          case 1:
            this.drawHeightDecreasing();
            break;
          case 2:
            this.drawHeightIncreasing();
            break;
          case 3:
            this.drawByXYZ();
            break;
          case 4:
            this.drawByColumns();
            break;
          case 5:
            this.drawByRows();
            break;
        }
      } else {
        this.tiling.preview.canvas.width =
          POSITION_DIALOG_COL_COUNT * POSITION_DIALOG_CELL_SIZE;
        this.tiling.preview.canvas.height = this.tiling.preview.canvas.width;
      }
    },
    drawInit(mode, setNull = true) {
      console.log(mode);

      if (setNull) {
        this.tiling.alignment.rows = null;
        this.tiling.alignment.cols = null;
      }

      this.tiling.preview.clearRect(
        0,
        0,
        this.tiling.preview.canvas.width,
        this.tiling.preview.canvas.height
      );
    },
    drawCascade() {
      this.drawInit("Cascade");

      let imageWidth = this.imageWidth,
        imageHeight = this.imageHeight;
      let border = parseInt(this.tiling.alignment.border);
      if (isNaN(border)) {
        border = 0;
        this.tiling.alignment.border = 0;
      }
      const tick = 50;
      let d = Math.max(imageWidth, imageHeight) / tick;
      const width =
        Math.max(this.imageWidth, this.imageHeight) +
        d * this.files.length +
        2 * border;

      if (width < POSITION_DIALOG_CANVAS_MAX_PIXEL) {
        this.tiling.preview.canvas.width = width;
      } else {
        this.tiling.preview.canvas.width = POSITION_DIALOG_CANVAS_MAX_PIXEL;
        border = (POSITION_DIALOG_CANVAS_MAX_PIXEL * border) / width;
        let fitSize =
          ((POSITION_DIALOG_CANVAS_MAX_PIXEL - 2 * border) * tick) /
          (tick + this.files.length);
        d = fitSize / tick;
        if (imageWidth > imageHeight) {
          imageWidth = fitSize;
          imageHeight = (imageWidth / this.imageWidth) * this.imageHeight;
        } else {
          imageHeight = fitSize;
          imageWidth = (imageHeight / this.imageHeight) * this.imageWidth;
        }
      }
      this.tiling.preview.canvas.height = this.tiling.preview.canvas.width;

      let idx = 0;
      while (idx < this.files.length) {
        let image = document.getElementById(`images_${idx}`);
        const x = border + idx * d,
          y = x;
        this.tiling.preview.drawImage(image, x, y, imageWidth, imageHeight);

        idx++;
      }
    },
    drawHeightDecreasing() {
      this.drawInit("HeightDecreasing");

      const cols = Math.floor(Math.sqrt(this.files.length));
      const rows =
        Math.floor(this.files.length / cols) +
        (this.files.length / cols == Math.floor(this.files.length / cols)
          ? 0
          : 1);

      let imageWidth = this.imageWidth,
        imageHeight = this.imageHeight;
      let border = parseInt(this.tiling.alignment.border),
        gapX = parseInt(this.tiling.alignment.gapX),
        gapY = parseInt(this.tiling.alignment.gapY);
      if (isNaN(border)) {
        border = 0;
        this.tiling.alignment.border = 0;
      }
      if (isNaN(gapX)) {
        gapX = 0;
        this.tiling.alignment.gapX = 0;
      }
      if (isNaN(gapY)) {
        gapY = 0;
        this.tiling.alignment.gapY = 0;
      }

      const width =
        Math.max(
          rows * imageHeight + (rows - 1) * gapY,
          cols * imageWidth + (cols - 1) * gapX
        ) +
        2 * border;

      if (width < POSITION_DIALOG_CANVAS_MAX_PIXEL) {
        this.tiling.preview.canvas.width = width;
      } else {
        this.tiling.preview.canvas.width = POSITION_DIALOG_CANVAS_MAX_PIXEL;
        border = (POSITION_DIALOG_CANVAS_MAX_PIXEL * border) / width;
        gapX = (POSITION_DIALOG_CANVAS_MAX_PIXEL * gapX) / width;
        gapY = (POSITION_DIALOG_CANVAS_MAX_PIXEL * gapY) / width;
        if (
          cols * imageWidth + (cols - 1) * gapX >
          rows * imageHeight + (rows - 1) * gapY
        ) {
          imageWidth =
            (POSITION_DIALOG_CANVAS_MAX_PIXEL -
              2 * border -
              (cols - 1) * gapX) /
            cols;
          imageHeight = (imageWidth / this.imageWidth) * this.imageHeight;
        } else {
          imageHeight =
            (POSITION_DIALOG_CANVAS_MAX_PIXEL -
              2 * border -
              (rows - 1) * gapY) /
            rows;
          imageWidth = (imageHeight / this.imageHeight) * this.imageWidth;
        }
      }
      this.tiling.preview.canvas.height = this.tiling.preview.canvas.width;

      let row = 0,
        idx = 0;
      while (row < rows) {
        let col = 0;
        while (col < cols) {
          idx = row * cols + col;
          if (idx >= this.files.length) break;

          let image = document.getElementById(`images_${idx}`);
          const x = border + col * (imageWidth + gapX),
            y = border + row * (imageHeight + gapY);
          this.tiling.preview.drawImage(image, x, y, imageWidth, imageHeight);

          col++;
        }
        if (idx >= this.files.length) break;

        row++;
      }
    },
    drawHeightIncreasing() {
      this.drawInit("HeightIncreasing");

      const cols = Math.floor(Math.sqrt(this.files.length));
      const rows =
        Math.floor(this.files.length / cols) +
        (this.files.length / cols == Math.floor(this.files.length / cols)
          ? 0
          : 1);

      let imageWidth = this.imageWidth,
        imageHeight = this.imageHeight;
      let border = parseInt(this.tiling.alignment.border),
        gapX = parseInt(this.tiling.alignment.gapX),
        gapY = parseInt(this.tiling.alignment.gapY);
      if (isNaN(border)) {
        border = 0;
        this.tiling.alignment.border = 0;
      }
      if (isNaN(gapX)) {
        gapX = 0;
        this.tiling.alignment.gapX = 0;
      }
      if (isNaN(gapY)) {
        gapY = 0;
        this.tiling.alignment.gapY = 0;
      }

      const width =
        Math.max(
          rows * imageHeight + (rows - 1) * gapY,
          cols * imageWidth + (cols - 1) * gapX
        ) +
        2 * border;

      if (width < POSITION_DIALOG_CANVAS_MAX_PIXEL) {
        this.tiling.preview.canvas.width = width;
      } else {
        this.tiling.preview.canvas.width = POSITION_DIALOG_CANVAS_MAX_PIXEL;
        border = (POSITION_DIALOG_CANVAS_MAX_PIXEL * border) / width;
        gapX = (POSITION_DIALOG_CANVAS_MAX_PIXEL * gapX) / width;
        gapY = (POSITION_DIALOG_CANVAS_MAX_PIXEL * gapY) / width;
        if (
          cols * imageWidth + (cols - 1) * gapX >
          rows * imageHeight + (rows - 1) * gapY
        ) {
          imageWidth =
            (POSITION_DIALOG_CANVAS_MAX_PIXEL -
              2 * border -
              (cols - 1) * gapX) /
            cols;
          imageHeight = (imageWidth / this.imageWidth) * this.imageHeight;
        } else {
          imageHeight =
            (POSITION_DIALOG_CANVAS_MAX_PIXEL -
              2 * border -
              (rows - 1) * gapY) /
            rows;
          imageWidth = (imageHeight / this.imageHeight) * this.imageWidth;
        }
      }
      this.tiling.preview.canvas.height = this.tiling.preview.canvas.width;

      let row = 0,
        idx = 0;
      while (row < rows) {
        let col = 0;
        while (col < cols) {
          idx = row * cols + col;
          if (idx >= this.files.length) break;

          let image = document.getElementById(
            `images_${this.files.length - idx - 1}`
          );
          const x = border + col * (imageWidth + gapX),
            y = border + row * (imageHeight + gapY);
          this.tiling.preview.drawImage(image, x, y, imageWidth, imageHeight);

          col++;
        }
        if (idx >= this.files.length) break;

        row++;
      }
    },
    drawByXYZ() {
      this.drawInit("ByXYZ");
    },
    drawByColumns() {
      this.drawInit("ByColumns", false);

      if (this.tiling.alignment.rows == null) {
        this.tiling.alignment.rows = Math.floor(Math.sqrt(this.files.length));
      }
      this.tiling.alignment.cols =
        Math.floor(this.files.length / this.tiling.alignment.rows) +
        (this.files.length / this.tiling.alignment.rows ==
        Math.floor(this.files.length / this.tiling.alignment.rows)
          ? 0
          : 1);

      let imageWidth = this.imageWidth,
        imageHeight = this.imageHeight;
      let border = parseInt(this.tiling.alignment.border),
        gapX = parseInt(this.tiling.alignment.gapX),
        gapY = parseInt(this.tiling.alignment.gapY);
      if (isNaN(border)) {
        border = 0;
        this.tiling.alignment.border = 0;
      }
      if (isNaN(gapX)) {
        gapX = 0;
        this.tiling.alignment.gapX = 0;
      }
      if (isNaN(gapY)) {
        gapY = 0;
        this.tiling.alignment.gapY = 0;
      }
      const width =
        Math.max(
          this.tiling.alignment.rows * imageHeight +
            (this.tiling.alignment.rows - 1) * gapY,
          this.tiling.alignment.cols * imageWidth +
            (this.tiling.alignment.cols - 1) * gapX
        ) +
        2 * border;

      if (width < POSITION_DIALOG_CANVAS_MAX_PIXEL) {
        this.tiling.preview.canvas.width = width;
      } else {
        this.tiling.preview.canvas.width = POSITION_DIALOG_CANVAS_MAX_PIXEL;
        border = (POSITION_DIALOG_CANVAS_MAX_PIXEL * border) / width;
        gapX = (POSITION_DIALOG_CANVAS_MAX_PIXEL * gapX) / width;
        gapY = (POSITION_DIALOG_CANVAS_MAX_PIXEL * gapY) / width;
        if (
          this.tiling.alignment.cols * imageWidth +
            (this.tiling.alignment.cols - 1) * gapX >
          this.tiling.alignment.rows * imageHeight +
            (this.tiling.alignment.rows - 1) * gapY
        ) {
          imageWidth =
            (POSITION_DIALOG_CANVAS_MAX_PIXEL -
              2 * border -
              (this.tiling.alignment.cols - 1) * gapX) /
            this.tiling.alignment.cols;
          imageHeight = (imageWidth / this.imageWidth) * this.imageHeight;
        } else {
          imageHeight =
            (POSITION_DIALOG_CANVAS_MAX_PIXEL -
              2 * border -
              (this.tiling.alignment.rows - 1) * gapY) /
            this.tiling.alignment.rows;
          imageWidth = (imageHeight / this.imageHeight) * this.imageWidth;
        }
      }
      this.tiling.preview.canvas.height = this.tiling.preview.canvas.width;

      let c = 0,
        dir = 1,
        idx = 0;
      while (c < this.tiling.alignment.cols) {
        let r = 0;
        while (r < this.tiling.alignment.rows) {
          idx = r + c * this.tiling.alignment.rows;
          if (idx >= this.files.length) break;

          let image = document.getElementById(`images_${idx}`);

          let row = r;
          if (this.tiling.alignment.orders.includes("descending-order")) {
            if (this.tiling.alignment.orders.includes("up-down")) {
              row = dir < 0 ? r : this.tiling.alignment.rows - 1 - r;
            } else {
              row = dir > 0 ? r : this.tiling.alignment.rows - 1 - r;
            }
          } else {
            if (this.tiling.alignment.orders.includes("up-down")) {
              row = this.tiling.alignment.rows - 1 - r;
            }
          }

          let col = this.tiling.alignment.orders.includes("left-right")
            ? this.tiling.alignment.cols - 1 - c
            : c;

          const x = border + col * (imageWidth + gapX),
            y = border + row * (imageHeight + gapY);
          this.tiling.preview.drawImage(image, x, y, imageWidth, imageHeight);

          r++;
        }
        if (idx >= this.files.length) break;

        c++;
        dir *= -1;
      }
    },
    drawByRows() {
      this.drawInit("ByRows", false);

      if (this.tiling.alignment.cols == null) {
        this.tiling.alignment.cols = Math.floor(Math.sqrt(this.files.length));
      }
      this.tiling.alignment.rows =
        Math.floor(this.files.length / this.tiling.alignment.cols) +
        (this.files.length / this.tiling.alignment.cols ==
        Math.floor(this.files.length / this.tiling.alignment.cols)
          ? 0
          : 1);

      let imageWidth = this.imageWidth,
        imageHeight = this.imageHeight;
      let border = parseInt(this.tiling.alignment.border),
        gapX = parseInt(this.tiling.alignment.gapX),
        gapY = parseInt(this.tiling.alignment.gapY);
      if (isNaN(border)) {
        border = 0;
        this.tiling.alignment.border = 0;
      }
      if (isNaN(gapX)) {
        gapX = 0;
        this.tiling.alignment.gapX = 0;
      }
      if (isNaN(gapY)) {
        gapY = 0;
        this.tiling.alignment.gapY = 0;
      }
      const width =
        Math.max(
          this.tiling.alignment.rows * imageHeight +
            (this.tiling.alignment.rows - 1) * gapY,
          this.tiling.alignment.cols * imageWidth +
            (this.tiling.alignment.cols - 1) * gapX
        ) +
        2 * border;

      if (width < POSITION_DIALOG_CANVAS_MAX_PIXEL) {
        this.tiling.preview.canvas.width = width;
      } else {
        this.tiling.preview.canvas.width = POSITION_DIALOG_CANVAS_MAX_PIXEL;
        border = (POSITION_DIALOG_CANVAS_MAX_PIXEL * border) / width;
        gapX = (POSITION_DIALOG_CANVAS_MAX_PIXEL * gapX) / width;
        gapY = (POSITION_DIALOG_CANVAS_MAX_PIXEL * gapY) / width;
        if (
          this.tiling.alignment.cols * imageWidth +
            (this.tiling.alignment.cols - 1) * gapX >
          this.tiling.alignment.rows * imageHeight +
            (this.tiling.alignment.rows - 1) * gapY
        ) {
          imageWidth =
            (POSITION_DIALOG_CANVAS_MAX_PIXEL -
              2 * border -
              (this.tiling.alignment.cols - 1) * gapX) /
            this.tiling.alignment.cols;
          imageHeight = (imageWidth / this.imageWidth) * this.imageHeight;
        } else {
          imageHeight =
            (POSITION_DIALOG_CANVAS_MAX_PIXEL -
              2 * border -
              (this.tiling.alignment.rows - 1) * gapY) /
            this.tiling.alignment.rows;
          imageWidth = (imageHeight / this.imageHeight) * this.imageWidth;
        }
      }
      this.tiling.preview.canvas.height = this.tiling.preview.canvas.width;

      let r = 0,
        dir = 1,
        idx = 0;
      while (r < this.tiling.alignment.rows) {
        let c = 0;
        while (c < this.tiling.alignment.cols) {
          idx = r * this.tiling.alignment.cols + c;
          if (idx >= this.files.length) break;

          let image = document.getElementById(`images_${idx}`);

          let col = c;
          if (this.tiling.alignment.orders.includes("descending-order")) {
            if (this.tiling.alignment.orders.includes("left-right")) {
              col = dir < 0 ? c : this.tiling.alignment.cols - 1 - c;
            } else {
              col = dir > 0 ? c : this.tiling.alignment.cols - 1 - c;
            }
          } else {
            if (this.tiling.alignment.orders.includes("left-right")) {
              col = this.tiling.alignment.cols - 1 - c;
            }
          }

          let row = this.tiling.alignment.orders.includes("up-down")
            ? this.tiling.alignment.rows - 1 - r
            : r;

          const x = border + col * (imageWidth + gapX),
            y = border + row * (imageHeight + gapY);
          this.tiling.preview.drawImage(image, x, y, imageWidth, imageHeight);

          c++;
        }
        if (idx >= this.files.length) break;

        r++;
        dir *= -1;
      }
    },

    // Edit section
    pickImageFile(_selectedIndex) {
      if (_selectedIndex) {
        console.log(_selectedIndex);
        //   let row = 0,
        //     dir = 1,
        //     idx = 0;
        //   while(true) { /* eslint-disable-line */
        //     let col = 0;
        //     while (0 <= col && col <= this.tiling.alignment.cols) {
        //       idx = row * this.tiling.alignment.cols + col;
        //       if (idx >= this.files.length) break;

        //       if (idx == this.tiling.edit.oldFileItem) {
        //         let image = document.getElementById(`images_${idx}`);
        //         this.tiling.preview.drawImage(
        //           image,
        //           (dir > 0 ? col : this.tiling.alignment.cols - 1 - col) *
        //             POSITION_DIALOG_CELL_SIZE,
        //           row * POSITION_DIALOG_CELL_SIZE,
        //           POSITION_DIALOG_CELL_SIZE,
        //           POSITION_DIALOG_CELL_SIZE
        //         );
        //       }

        //       if (idx == _selectedIndex) {
        //         let _X =
        //             (dir > 0 ? col : this.tiling.alignment.cols - 1 - col) *
        //               POSITION_DIALOG_CELL_SIZE +
        //             POSITION_DIALOG_STROKE_WIDTH,
        //           _Y =
        //             row * POSITION_DIALOG_CELL_SIZE +
        //             POSITION_DIALOG_STROKE_WIDTH,
        //           _W =
        //             POSITION_DIALOG_CELL_SIZE - 2 * POSITION_DIALOG_STROKE_WIDTH,
        //           _H = _W;

        //         this.tiling.preview.beginPath();
        //         this.tiling.preview.lineWidth = POSITION_DIALOG_STROKE_WIDTH;
        //         this.tiling.preview.strokeStyle = "#76FF03";
        //         this.tiling.preview.rect(_X, _Y, _W, _H);
        //         this.tiling.preview.stroke();
        //       }

        //       col++;
        //     }

        //     if (idx >= this.files.length) break;

        //     row++;
        //     dir *= -1;
        //   }

        //   this.tiling.edit.oldFileItem = _selectedIndex;
      }
    },

    changeAlignMode() {
      this.drawImages();
    },

    changeAlignOrder() {
      this.drawImages();
    },

    // Change text fields
    inputTilingRows() {
      this.drawImages();
    },
    inputTilingCols() {
      this.drawImages();
    },
    inputTilingBorder() {
      this.drawImages();
    },
    inputTilingGapX() {
      this.drawImages();
    },
    inputTilingGapY() {
      this.drawImages();
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

    updateNamePattern() {
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
        if (key)
          this.setNamePattern({
            key: key,
            pos: [this.namePatterns[i].start, this.namePatterns[i].end]
          });
      }
    },

    // update
    updateNameType() {
      let MAX_BATCH_SIZE = 10;

      this.updateNamePattern();

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
            row: p[0],
            col: p[1],
            z: p[2],
            timeline: p[3],
            channel: p[4],
            objectLense: 4 // The default object lense for name & type
          },
          doneCB: function() {
            thiz.progressBarValue ++;
            console.log(thiz.progressBarValue + " / " + thiz.progressBarMaxValue);
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
.isDragging {
  background-color: #e0f2f1;
  border-color: #fff;
}

.control-panel {
  width: calc(100% - 450px);
}

.control-panel .inside {
  height: 450px;
  margin-top: 20px;
  margin-right: 16px;
}

.canvas {
  width: 450px;
  height: 450px;
  border: 1px solid #333;
  background-color: black;
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
.progress-bar {
  width: 300pt;
}
</style>
