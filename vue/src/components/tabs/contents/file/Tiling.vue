<template>
  <v-sheet class="drop pa-5" height="100%">
    <flash-message></flash-message>
    <v-row no-gutters>
      <v-col cols="2">
        <v-card class="pa-1">
          <v-list shaped>
            <v-list-item-group v-model="tiling.activeMenuItem" color="primary">
              <v-list-item v-for="(menuTitle, idx) in tilingMenus" :key="idx">
                <v-list-item-content>
                  <v-list-item-title v-text="menuTitle"></v-list-item-title>
                </v-list-item-content>
              </v-list-item>
            </v-list-item-group>
          </v-list>
        </v-card>
      </v-col>
      <v-col cols="8" class="pa-2">
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
                    v-if="filesSortByField.length"
                    v-model="tiling.edit.activeFileItem"
                    color="green"
                    @change="pickImageFile"
                  >
                    <v-list-item
                      v-for="(file, idx) in filesSortByField"
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
                        <v-list-item-title>No Image Files!</v-list-item-title>
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
                          :style="n == 4 ? { filter: 'grayscale(1)' } : {}"
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
                    tiling.alignment.disables[tiling.alignment.activeMode].chkLR
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
                    tiling.alignment.disables[tiling.alignment.activeMode].chkUD
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
                    tiling.alignment.disables[tiling.alignment.activeMode].chkDO
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
                        tiling.alignment.disables[tiling.alignment.activeMode]
                          .txtRows
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
                        tiling.alignment.disables[tiling.alignment.activeMode]
                          .txtCols
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
                        tiling.alignment.disables[tiling.alignment.activeMode]
                          .txtBorder
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
                        tiling.alignment.disables[tiling.alignment.activeMode]
                          .txtGapX
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
                        tiling.alignment.disables[tiling.alignment.activeMode]
                          .txtGapY
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
              <div class="inside">
                <v-row class="mr-4">
                  <v-checkbox
                    v-model="tiling.bonding.notSnapToEdge"
                    label="None"
                    color="primary"
                    :value="true"
                    hide-details
                    :disabled="
                      tiling.alignment.disables[tiling.alignment.activeMode]
                        .chkLR
                    "
                  ></v-checkbox>
                </v-row>
                <v-row class="mr-4">
                  <v-checkbox
                    v-model="tiling.bonding.snapToEdge"
                    label="Snap To Edge"
                    color="primary"
                    :value="true"
                    hide-details
                    :disabled="
                      tiling.alignment.disables[tiling.alignment.activeMode]
                        .chkLR
                    "
                  ></v-checkbox>
                </v-row>
                <v-row class="mr-4">
                  <v-checkbox
                    v-model="tiling.bonding.patternMatch"
                    label="Pattern Match"
                    color="primary"
                    :value="true"
                    hide-details
                    :disabled="
                      tiling.alignment.disables[tiling.alignment.activeMode]
                        .chkLR
                    "
                  ></v-checkbox>
                </v-row>
                <v-row class="mr-4" v-if="tiling.bonding.patternMatch">
                  <v-col cols="4">
                    <v-text-field
                      v-model="tiling.bonding.border"
                      class="range-field"
                      label="Border"
                      type="number"
                      outlined
                      dense
                    />
                  </v-col>
                  <v-col cols="4">
                    <v-text-field
                      v-model="tiling.bonding.overlapX"
                      class="range-field"
                      label="Overlap X"
                      type="number"
                      outlined
                      dense
                    />
                  </v-col>
                  <v-col cols="4">
                    <v-text-field
                      v-model="tiling.bonding.overlapY"
                      class="range-field"
                      label="Overlap Y"
                      type="number"
                      outlined
                      dense
                    />
                  </v-col>
                </v-row>
                <v-row
                  class="mr-4 justify-center"
                  v-if="tiling.bonding.patternMatch"
                >
                  <v-btn elevation="2" class="mt-5" @click="autoPatternMathing">
                    Auto
                  </v-btn>
                </v-row>
              </div>
            </v-card>
            <!-- Shading -->
            <v-card v-else-if="tiling.activeMenuItem == 3" flat>
              <v-card-title class="pa-1">Shading</v-card-title>
              <div class="inside">
                <v-row class="mt-4 mr-4">
                  <v-col cols="6">
                    <v-btn
                      class="px-0"
                      min-width="34"
                      :height="34"
                      text
                      color="teal"
                      @click="normalizeImgLuminance"
                      >Normalize</v-btn
                    >
                  </v-col>
                </v-row>
                <v-row class="mt-4 mr-4">
                  <v-col cols="6">
                    <v-btn
                      class="px-0"
                      min-width="34"
                      :height="34"
                      text
                      color="teal"
                      @click="correctLighting"
                      >Correct</v-btn
                    >
                  </v-col>
                </v-row>
              </div>
            </v-card>
            <!-- Display -->
            <v-card v-else-if="tiling.activeMenuItem == 4" flat>
              <v-card-title class="pa-1">Display</v-card-title>
              <div class="inside">
                <v-row class="mt-4 mr-4">
                  <v-col cols="6">
                    <v-icon color="yellow">mdi-weather-sunny</v-icon>
                    <v-btn
                      class="px-0"
                      min-width="34"
                      :height="34"
                      text
                      color="teal"
                      @click="decreaseImgLuminance"
                      >-</v-btn
                    >
                    <v-icon color="yellow">mdi-weather-sunny</v-icon>
                    <v-btn
                      class="px-0"
                      min-width="34"
                      :height="34"
                      text
                      color="teal"
                      @click="increaseImgLuminance"
                      >+</v-btn
                    >
                  </v-col>
                </v-row>
                <v-row class="mt-4 mr-4">
                  <v-col cols="6">
                    <v-btn
                      class="px-0"
                      min-width="34"
                      :height="34"
                      text
                      color="teal"
                      @click="resetImgLuminance"
                      >Reset</v-btn
                    >
                  </v-col>
                </v-row>
                <v-row class="mt-4 mr-4">
                  <v-col cols="6">
                    <v-btn
                      class="px-0"
                      min-width="34"
                      :height="34"
                      text
                      color="teal"
                      @click="bestFit"
                      >BestFit</v-btn
                    >
                  </v-col>
                </v-row>
              </div>
            </v-card>
            <!-- Result -->
            <v-card v-else-if="tiling.activeMenuItem == 5" flat>
              <v-card-title class="pa-1">Result</v-card-title>
              <div class="inside">
                <v-row class="mt-4 mr-4">
                  <v-col cols="6">
                    <v-btn-toggle
                      v-model="tiling.result.select"
                      color="primary"
                      dense
                      group
                      mandatory
                    >
                      <v-btn :value="true" text>
                        <v-icon>mdi-crop-free</v-icon>
                      </v-btn>
                      <v-btn :value="false" text>
                        <v-icon>mdi-close</v-icon>
                      </v-btn>
                    </v-btn-toggle>
                  </v-col>
                </v-row>
                <v-row class="mt-4 mr-4">
                  <v-col cols="6">
                    <v-btn depressed @click="exportTiledImage">
                      Tiled Image
                    </v-btn>
                  </v-col>
                </v-row>
              </div>
            </v-card>
            <!-- Option -->
            <v-card v-else-if="tiling.activeMenuItem == 6" flat>
              <v-card-title class="pa-1">Option</v-card-title>
              <div class="inside"></div>
            </v-card>
          </div>

          <!-- Tiling Preview -->
          <div class="container-fluid">
            <div class="row">
              <div class="col">
                <canvas
                  id="canvas"
                  class="canvas"
                  ref="canvasElement"
                  cursor="crosshair"
                ></canvas>
              </div>
              <div class="col">
                <ScrollBar
                  direction="col"
                  :total="verticalLength"
                  :value="tiling.canvasHeight"
                  :top="scrollBarVerticalMin"
                  @change="onCanvasMoved"
                />
              </div>
            </div>

            <div class="row">
              <div class="col">
                <ScrollBar
                  direction="row"
                  :total="rowLength"
                  :left="scrollBarHorizontalMin"
                  :value="tiling.canvasWidth"
                  @change="onCanvasRowMoved"
                />
              </div>

              <div class="col-sm-2" style="position: relative;">
                <v-btn
                  style="position: absolute; top: 0; width: 100%; height: 38px;"
                >
                  {{ scaleRate + "%" }}
                  <v-icon right>
                    mdi-pencil
                  </v-icon>
                </v-btn>
                <v-select
                  style="position: absolute; top: 0; width: 100%; height: 38px;opacity: 0;"
                  :items="tiling.canvasScales"
                  v-model="tiling.canvasScale"
                  @change="onScaleChange"
                  dense
                  solo
                >
                  <template #selection="{ item }">
                    {{ item + "%" }}
                  </template>
                </v-select>
              </div>
            </div>
          </div>
        </div>
      </v-col>
      <v-col cols="2" class="pa-2">
        <OpenPositionViewTab />
      </v-col>
    </v-row>
  </v-sheet>
</template>

<script>
import { createNamespacedHelpers } from "vuex";
import OpenPositionViewTab from "./OpenPositionViewTab";
import ScrollBar from "@/components/basic/ScrollBar";
import {
  autoFitLuminance,
  changeImageLuminance,
  getImageEdge,
  imageAverageLuminance,
  shadingCorrection2
} from "../../../../utils/img-chg";
import {
  imgHorizontalDistance,
  imgVerticalDistance,
  imgXDistance,
  imgYDistance,
  matchPixels
} from "../../../../utils/pattern-match";
import {
  POSITION_DIALOG_CELL_SIZE,
  POSITION_DIALOG_COL_COUNT,
  TILING_CANVAS_SIZE,
  TILING_SCALE_OPTIONS
} from "../../../../utils/constants";

import * as tilingApi from "@/api/tiles";

const positionModule = createNamespacedHelpers("files/position");

export default {
  name: "Tiling",
  components: {
    OpenPositionViewTab,
    ScrollBar
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

    imageWidth: 0,
    imageHeight: 0,

    scrollX: TILING_CANVAS_SIZE / 2,
    scrollY: TILING_CANVAS_SIZE / 2,
    scrollStep: 0,
    frontScale: TILING_SCALE_OPTIONS[1] / 100,
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
      // Setting for tile picture interface parameter
      canvas: null,
      canvasScales: TILING_SCALE_OPTIONS,
      canvasScale: TILING_SCALE_OPTIONS[1] / 100,
      canvasShiftX: 0, // displacement in the x direction
      canvasShiftY: 0, // displacement in the y direction
      canvasTop: 0,
      canvasLeft: 0,
      canvasWidth: TILING_CANVAS_SIZE,
      canvasHeight: TILING_CANVAS_SIZE,
      preview: null,
      canvasScaleRatio: 1,
      totalImagesWith: TILING_CANVAS_SIZE,
      totalImagesHeight: TILING_CANVAS_SIZE,
      activeMenuItem: 0,
      bonding: {
        notSnapToEdge: true,
        snapToEdge: false,
        patternMatch: false,
        lines: [],
        offsetX: 0,
        offsetY: 0,
        overlapX: 0,
        overlapY: 0,
        border: 25
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
      },
      result: {
        select: false
      },
      mouse: {
        moveTime: undefined,
        catchImg: false,
        draggingImgIdx: -1,
        startX: -1,
        startY: -1,
        imgOriginX: -1,
        imgOriginY: -1
      },

      drawList: [],
      drawListSorted: [],
      drawingOrder: 0,
      drawingIntervalHd: null,
      drawingIntervalNeedRedraw: false, // Recalculate x,y according to alignment setting.
      drawingIntervalNeedPerformingDrawing: false // Just draw images.
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
    // progressBarMaxValue: 0,
    luminance: 0.0,
    averageLuminance: 0.0,
    autoFit: false,
    translateX: 0,
    translateY: 0
  }),

  watch: {
    // whenever question changes, this function will run
    // "tiling.canvasScale": function(newV, oV) {
    // },
    "tiling.bonding.notSnapToEdge": function(newV, oV) {
      if (newV) {
        this.tiling.bonding.snapToEdge = false;
        this.tiling.bonding.patternMatch = false;
        this.performDrawing();
      }
    },
    "tiling.bonding.snapToEdge": function(newV, oV) {
      if (newV) {
        this.tiling.bonding.notSnapToEdge = false;
        this.tiling.bonding.patternMatch = false;
        this.performDrawing();
      }
    },
    "tiling.bonding.patternMatch": function(newV, oV) {
      if (newV) {
        this.tiling.bonding.notSnapToEdge = false;
        this.tiling.bonding.snapToEdge = false;
        this.performDrawing();
      }
    }
  },

  computed: {
    ...positionModule.mapGetters({
      files: "getFiles",
      filesSortByField: "getFilesSortByField",
      channelOptions: "getChannelOptions"
    }),
    alignButtonImage() {
      return index => require(`@/assets/images/pos_align_${index - 1}.png`);
    },
    scaleRate() {
      return (this.coordinateScale * 100).toFixed(0);
    },
    coordinateScale() {
      return this.tiling.canvasScale;
      // return this.tiling.canvasScale / 100;
    },
    maxAndMinPoint() {
      let xMax = 0;
      let yMax = 0;
      let xMin = 0;
      let yMin = 0;
      for (let img of this.tiling.drawList) {
        const { width, height, x, y } = this.coordinateTranslate(img);
        const xPoint = x + width;
        const yPoint = y + height;
        if (xPoint > xMax) xMax = xPoint;
        if (yPoint > yMax) yMax = yPoint;
        if (x < xMin) xMin = x;
        if (y < yMin) yMin = y;
      }
      return { xMin, xMax, yMin, yMax };
    },
    scrollBarHorizontalMax() {
      const gap = this.maxAndMinPoint.xMax - TILING_CANVAS_SIZE;
      return gap < 0 ? 0 : gap;
    },
    scrollBarHorizontalMin() {
      const gap = this.maxAndMinPoint.xMin;
      return gap > 0 ? 0 : gap;
    },
    scrollBarVerticalMax() {
      const gap = this.maxAndMinPoint.yMax - TILING_CANVAS_SIZE;
      return gap < 0 ? 0 : gap;
    },
    scrollBarVerticalMin() {
      const gap = this.maxAndMinPoint.yMin;
      return gap > 0 ? 0 : gap;
    },
    verticalLength() {
      return (
        TILING_CANVAS_SIZE +
        this.scrollBarVerticalMax -
        this.scrollBarVerticalMin
      );
    },
    rowLength() {
      return (
        TILING_CANVAS_SIZE +
        this.scrollBarHorizontalMax -
        this.scrollBarHorizontalMin
      );
    },
    overflowCanvas() {
      return this.scrollBarHorizontalMax > 0 || this.scrollBarVerticalMax > 0;
    }
  },

  methods: {
    updateLeftAndTop() {
      this.tiling.canvasLeft = Math.abs(this.scrollBarHorizontalMin);
      this.tiling.canvasTop = Math.abs(this.scrollBarVerticalMin);
    },
    onCanvasMoved(val) {
      const step = Math.abs(val) - Math.abs(this.scrollBarVerticalMin);
      this.tiling.drawList.forEach((item, index) => {
        item.y -= Number(step);
      });
      this.performDrawing();
    },
    onCanvasRowMoved(val) {
      const step = Math.abs(val) - Math.abs(this.scrollBarHorizontalMin);
      this.tiling.drawList.forEach((item, index) => {
        item.x -= step;
      });
      this.performDrawing();
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
    onScaleChange(val) {
      this.tiling.canvasTop = 0;
      this.tiling.canvasLeft = 0;
      this.tiling.canvasScale = val / 100;
      this.performDrawing();
    },
    pickImageFile(_selectedIndex) {
      const POSITION_DIALOG_STROKE_WIDTH = 2;
      if (_selectedIndex >= 0) {
        let row = 0,
          dir = 1,
          idx = 0;
        while(true) { /* eslint-disable-line */
          let col = 0;
          while (0 <= col && col <= this.tiling.alignment.cols) {
            idx = row * this.tiling.alignment.cols + col;
            if (idx >= this.files.length) break;

            if (idx == this.tiling.edit.oldFileItem) {
              let image = document.getElementById(`images_${idx}`);
              this.tiling.preview.drawImage(
                image,
                (dir > 0 ? col : this.tiling.alignment.cols - 1 - col) *
                  POSITION_DIALOG_CELL_SIZE,
                row * POSITION_DIALOG_CELL_SIZE,
                POSITION_DIALOG_CELL_SIZE,
                POSITION_DIALOG_CELL_SIZE
              );
            }

            if (idx == _selectedIndex) {
              let _X =
                  (dir > 0 ? col : this.tiling.alignment.cols - 1 - col) *
                    POSITION_DIALOG_CELL_SIZE +
                  POSITION_DIALOG_STROKE_WIDTH,
                _Y =
                  row * POSITION_DIALOG_CELL_SIZE +
                  POSITION_DIALOG_STROKE_WIDTH,
                _W =
                  POSITION_DIALOG_CELL_SIZE - 2 * POSITION_DIALOG_STROKE_WIDTH,
                _H = _W;

              this.tiling.preview.beginPath();
              this.tiling.preview.lineWidth = POSITION_DIALOG_STROKE_WIDTH;
              this.tiling.preview.strokeStyle = "#76FF03";
              this.tiling.preview.rect(_X, _Y, _W, _H);
              this.tiling.preview.stroke();
            }

            col++;
          }

          if (idx >= this.files.length) break;

          row++;
          dir *= -1;
        }
        this.tiling.edit.oldFileItem = _selectedIndex;
      }
    },
    async getImageSize() {
      if (this.files.length > 0) {
        let image = this.files[0].imageData;
        this.imageWidth = image.width * this.coordinateScale;
        this.imageHeight = image.height * this.coordinateScale;
      }
    },
    drawImages() {
      this.drawingIntervalNeedRedraw = true;
    },
    drawImages2() {
      if (
        this.filesSortByField.length > 0 &&
        this.filesSortByField[0].imageData
      ) {
        this.imageWidth = this.filesSortByField[0].imageData.width;
        this.imageHeight = this.filesSortByField[0].imageData.height;

        if (this.imageWidth && this.imageHeight) {
        } else {
          console.log("no image width");
          return;
        }
      } else {
        console.log("no image data");
        return;
      }

      // Reset the drawing order.
      // The drawing order is increased in the following methods.
      this.drawingOrder = 1;
      this.tiling.drawList = [];

      if (this.filesSortByField && this.filesSortByField.length) {
        console.log("ALIGNMENT = ", this.tiling.alignment.activeMode);
        switch (this.tiling.alignment.activeMode) {
          case 0:
            this.drawCascade(); // cascade display
            break;
          case 1:
            this.drawHeightDecreasing(); // Sort images in descending order by height
            break;
          case 2:
            this.drawHeightIncreasing(); // Sort images in ascending order by height
            break;
          case 3:
            this.drawByXYZ();
            break;
          case 4:
            this.drawByColumns(); // Fixed column arrangement
            break;
          case 5:
            this.drawByRows(); // Fixed line arrangement
            break;
        }
      } else {
        this.tiling.preview.canvas.width =
          POSITION_DIALOG_COL_COUNT * POSITION_DIALOG_CELL_SIZE;
        this.tiling.preview.canvas.height = this.tiling.preview.canvas.width;
      }

      this.tiling.canvasScaleRatio =
        this.canvas.width / this.canvas.offsetWidth;

      this.performDrawing();
      // if (this.averageLuminance != 0.0)
      // {
      //   this.normalizeImgLuminance();
      // } else if (this.luminance != 0.0) {
      //   this.updateImageLuminance();
      // }
    },
    updateImageLuminance: function() {
      let c = document.getElementById("canvas");
      if (this.tiling.preview == null) {
        this.tiling.preview = c.getContext("2d");
      }
      let imageData = this.tiling.preview.getImageData(0, 0, c.width, c.height);
      // imgData = new ImageData(
      //   new Uint8ClampedArray(
      //     this.$wasm.change_image_luminance(imgData.data, this.luminance)
      //   ),
      //   imgData.width,
      //   imgData.height
      // );
      imageData = changeImageLuminance(imageData, this.luminance);
      this.tiling.preview.putImageData(imageData, 0, 0);
    },

    // high-up image brightness
    increaseImgLuminance: function() {
      this.luminance += 0.05;
      this.performDrawing();
      // this.updateImageLuminance();
    },

    // Decrease image brightness
    decreaseImgLuminance() {
      this.luminance -= 0.05;
      this.performDrawing();
      this.autoFit = false;
      // this.updateImageLuminance();
    },
    bestFit(e) {
      this.autoFit = true;
      this.performDrawing();
    },
    /**
     * reset brightness
     */
    resetImgLuminance() {
      this.luminance = 0.0;
      this.autoFit = false;
      this.performDrawing();
    },
    /**
     * image object to ImageData object
     * @param params
     * @returns {ImageData}
     */
    img2ImageData(params) {
      var cvs = document.createElement("canvas");
      var ctx = cvs.getContext("2d");
      cvs.width = params.width;
      cvs.height = params.height;
      ctx.drawImage(params.image, 0, 0, cvs.width, cvs.height);

      let rs = ctx.getImageData(0, 0, cvs.width, cvs.height);

      cvs.remove();
      return rs;
    },
    imageData2ImgUri(imgData, width, height) {
      var cvs = document.createElement("canvas");
      var ctx = cvs.getContext("2d");

      cvs.width = width;
      cvs.height = height;

      ctx.putImageData(imgData, 0, 0, 0, 0, width, height);
      let rs = cvs.toDataURL();

      cvs.remove();
      return rs;
    },
    correctLighting() {
      let that = this;
      var idx = 0;
      that.$emit("set-progress-current", 0);
      that.$emit("set-progress-max", that.tiling.drawList.length - 1);

      // let hd = setInterval(function() {
      // console.log("idx: " + idx);

      function sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
      }
      async function go() {
        while (idx < that.tiling.drawList.length) {
          that.$emit("set-progress-current", idx);
          // console.log("Start correctLighting");

          let img = that.tiling.drawList[idx];
          let imgData = that.img2ImageData(img);
          if ("srgb" != imgData.colorSpace) {
            that.flashError("Color Space not supported: " + imgData.colorSpace);
            clearInterval(hd);
            return;
          }

          console.log("Get image daxta in memory");

          let newImgData = new ImageData(
            new Uint8ClampedArray(shadingCorrection2(img.image)),
            imgData.width,
            imgData.height
          );

          img.image.src = that.imageData2ImgUri(
            newImgData,
            imgData.width,
            imgData.height
          );

          if (idx == that.tiling.drawList.length - 1) {
            img.image.onload = function() {
              that.performDrawing();
            };
          }

          idx++;

          await sleep(300);
        }
      }
      go();
    },
    normalizeImgLuminance() {
      let entireLum = 0;
      let imgDataArr = [];
      let imgLumArr = [];
      for (let idx in this.tiling.drawList) {
        let item = this.coordinateTranslate(this.tiling.drawList[idx]);
        let imgData = this.img2ImageData(item);
        imgDataArr.push(imgData);
        let imgLum = imageAverageLuminance(imgData);
        imgLumArr.push(imgLum);
        entireLum += imgLum;
      }
      this.averageLuminance = entireLum / this.tiling.drawList.length;
      // console.log("entire image average lum ", this.averageLuminance);
      for (let idx in this.tiling.drawList) {
        let item = this.tiling.drawList[idx];
        let ratio =
          (imgLumArr[idx] - this.averageLuminance) / this.averageLuminance;
        item.lumRatio = ratio;
        // let imgData = imgDataArr[idx];
        // changeImageLuminance(imgData, ratio + this.luminance);
        // this.tiling.preview.putImageData(imgData, item.x, item.y, 0, 0,  item.width, item.height);
      }
      this.performDrawing();
    },
    /**
     * Initialize canvas, clear rows and columns
     * @param mode
     * @param setNull
     */
    drawInit(mode, setNull = true) {
      if (setNull) {
        this.tiling.alignment.rows = null;
        this.tiling.alignment.cols = null;
      }
    },

    drawCascade() {
      // cascade display picture method
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

      this.tiling.totalImagesHeight =
        this.imageHeight + d * this.files.length + 2 * border;

      this.tiling.totalImagesWith =
        this.imageWidth + d * this.files.length + 2 * border;

      let t = this.coordinateTranslate({
        height: this.tiling.totalImagesHeight
      });
      this.tiling.canvasShiftY = t.height;
      this.tiling.canvasShiftX = 0;

      let idx = 0;
      while (idx < this.filesSortByField.length) {
        let image = this.filesSortByField[idx].imageData;
        const x = border + idx * d,
          y = x;

        this.tiling.drawList.push({
          x,
          y,
          width: imageWidth,
          height: imageHeight,
          image,
          imageDataCache: null,
          occupied: true,
          drawingOrder: this.drawingOrder,
          orgIdx: idx
        });
        this.drawingOrder++;

        idx++;
      }
    },

    drawHeightDecreasing() {
      // sort pictures in descending order of height
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

      this.tiling.totalImagesHeight =
        rows * imageHeight + (rows - 1) * gapY + 2 * border;

      this.tiling.totalImagesWith =
        cols * imageWidth + (cols - 1) * gapX + 2 * border;

      let t = this.coordinateTranslate({
        height: this.tiling.totalImagesHeight
      });
      this.tiling.canvasShiftY = t.height;
      this.tiling.canvasShiftX = 0;

      let row = 0,
        idx = 0;
      while (row < rows) {
        let col = 0;
        while (col < cols) {
          idx = row * cols + col;
          if (idx >= this.filesSortByField.length) break;

          let image = this.filesSortByField[idx].imageData;
          const x = border + col * (imageWidth + gapX),
            y = border + row * (imageHeight + gapY);

          this.tiling.drawList.push({
            x,
            y,
            width: imageWidth,
            height: imageHeight,
            image,
            imageDataCache: null,
            occupied: true,
            drawingOrder: this.drawingOrder,
            orgIdx: idx,
            row: row,
            col: col
          });
          this.drawingOrder++;

          col++;
        }
        if (idx >= this.files.length) break;

        row++;
      }
    },

    drawHeightIncreasing() {
      // Sort images in ascending order by height
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

      this.tiling.totalImagesHeight =
        rows * imageHeight + (rows - 1) * gapY + 2 * border;

      this.tiling.totalImagesWith =
        cols * imageWidth + (cols - 1) * gapX + 2 * border;

      let t = this.coordinateTranslate({
        height: this.tiling.totalImagesHeight
      });
      this.tiling.canvasShiftY = t.height;
      this.tiling.canvasShiftX = 0;

      let row = 0,
        idx = 0;
      while (row < rows) {
        let col = 0;
        while (col < cols) {
          idx = row * cols + col;
          if (idx >= this.filesSortByField.length) break;

          let image = this.filesSortByField[idx].imageData;

          const x = border + col * (imageWidth + gapX),
            y = border + row * (imageHeight + gapY);

          this.tiling.drawList.push({
            x,
            y,
            width: imageWidth,
            height: imageHeight,
            image,
            imageDataCache: null,
            occupied: true,
            drawingOrder: this.drawingOrder,
            orgIdx: idx,
            row: row,
            col: col
          });
          this.drawingOrder++;

          col++;
        }
        if (idx >= this.files.length) break;

        row++;
      }
    },

    drawByXYZ() {
      this.drawInit("ByXYZ");
    },

    /**
     * Fixed column arrangement
     * @param patternMatch
     */
    drawByColumns(patternMatch = false) {
      this.drawInit("ByColumns", false); // Initialize the canvas without deleting the width and height

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

      this.tiling.totalImagesHeight =
        this.tiling.alignment.rows * imageHeight +
        (this.tiling.alignment.rows - 1) * gapY +
        2 * border;

      this.tiling.totalImagesWith =
        this.tiling.alignment.cols * imageWidth +
        (this.tiling.alignment.cols - 1) * gapX +
        2 * border;

      let t = this.coordinateTranslate({
        height: this.tiling.totalImagesHeight
      });
      this.tiling.canvasShiftY = t.height;
      this.tiling.canvasShiftX = 0;

      // The new backend solution
      tilingApi.alignTiles(this.tiling.alignment.rows, "byColumn", tiles => {
        tilingApi.listTiles(tiles => {
          console.log("Fetch the list again");
          console.log(tiles);
        });
      });

      // The lines below are deprecated.
      let c = 0,
        dir = 1,
        idx = 0;
      while (c < this.tiling.alignment.cols) {
        let r = 0;
        while (r < this.tiling.alignment.rows) {
          idx = r + c * this.tiling.alignment.rows;
          if (idx >= this.filesSortByField.length) break;

          let image = this.filesSortByField[idx].imageData;

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

          this.tiling.drawList.push({
            x,
            y,
            width: imageWidth,
            height: imageHeight,
            image,
            imageDataCache: null,
            occupied: true,
            drawingOrder: this.drawingOrder,
            orgIdx: idx,
            col: col,
            row: row
          });
          this.drawingOrder++;

          r++;
        }
        if (idx >= this.files.length) break;

        c++;
        dir *= -1;
      }
    },

    drawByRows(patternMatch = false) {
      // 固定行数排列
      this.drawInit("ByRows", false);

      if (this.tiling.alignment.cols == null) {
        this.tiling.alignment.cols = Math.floor(Math.sqrt(this.files.length));
      }

      this.tiling.alignment.rows = Math.ceil(
        this.files.length / this.tiling.alignment.cols
      );

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

      this.tiling.totalImagesHeight =
        this.tiling.alignment.rows * imageHeight +
        (this.tiling.alignment.rows - 1) * gapY +
        2 * border;

      this.tiling.totalImagesWith =
        this.tiling.alignment.cols * imageWidth +
        (this.tiling.alignment.cols - 1) * gapX +
        2 * border;

      let t = this.coordinateTranslate({
        height: this.tiling.totalImagesHeight
      });

      this.tiling.canvasShiftY = t.height;
      this.tiling.canvasShiftX = 0;

      let r = 0,
        dir = 1,
        idx = 0;

      // The new backend solution
      tilingApi.alignTiles(this.tiling.alignment.rows, "byRow", res => {
        tilingApi.listTiles(tiles => {
          console.log("Fetch the list again");
          console.log(tiles);
        });
      });

      // The lines below are deprecated
      while (r < this.tiling.alignment.rows) {
        let c = 0;
        while (c < this.tiling.alignment.cols) {
          idx = r * this.tiling.alignment.cols + c;
          if (idx >= this.filesSortByField.length) break;

          let image = this.filesSortByField[idx].imageData;

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

          if (image && imageWidth && typeof image == "object") {
            this.tiling.drawList.push({
              x,
              y,
              drawX: x,
              drawY: y,
              width: imageWidth,
              height: imageHeight,
              image,
              imageDataCache: null,
              occupied: true,
              drawingOrder: this.drawingOrder,
              orgIdx: idx,
              row: row,
              col: col
            });
            this.drawingOrder++;
          }

          c++;
        }
        if (idx >= this.files.length) break;

        r++;
        dir *= -1;
      }
    },
    getScaledImage(imgData) {
      const copyImg = Object.assign({}, imgData);
      copyImg.width = copyImg.width * this.coordinateScale;
      copyImg.height = copyImg.height * this.coordinateScale;
      return copyImg;
    },
    /**
     * 获取当前x,y坐标
     * @param x
     * @param y
     * @returns {number[]}
     */
    getPosition(x, y) {
      return [this.coordinateScale * x, this.coordinateScale * y];
    },
    coordinateTranslate: function(params, scale = this.coordinateScale) {
      let copy = Object.assign({}, params);
      if (typeof copy.width !== "undefined")
        copy.width = Math.ceil(copy.width * this.tiling.canvasScale);
      if (typeof copy.height !== "undefined")
        copy.height = Math.ceil(copy.height * this.tiling.canvasScale);
      if (typeof copy.x !== "undefined") {
        copy.x =
          copy.x * this.tiling.canvasScale +
          this.translateX -
          this.tiling.canvasLeft;
      }
      if (typeof copy.y !== "undefined") {
        copy.y =
          copy.y * this.tiling.canvasScale +
          this.translateY -
          this.tiling.canvasTop;
      }
      return copy;
    },

    coordinateTranslateReverse(params, scale = this.coordinateScale) {
      let canvasShiftY =
        this.tiling.totalImagesHeight * scale -
        TILING_CANVAS_SIZE -
        this.tiling.canvasShiftY;

      if (canvasShiftY < 0) canvasShiftY = 0;

      let copy = Object.assign({}, params);
      if (typeof copy.width !== "undefined") copy.width = copy.width / scale;
      if (typeof copy.height !== "undefined") copy.height = copy.height / scale;
      if (typeof copy.x !== "undefined")
        copy.x = copy.x / this.tiling.canvasScale + this.translateX;
      if (typeof copy.y !== "undefined")
        copy.y = copy.y / this.tiling.canvasScale + this.translateY;
      return copy;
    },

    performDrawing() {
      const ctx = this.tiling.preview;
      this.tiling.preview.clearRect(
        0,
        0,
        TILING_CANVAS_SIZE,
        TILING_CANVAS_SIZE
      );
      for (let idx in this.tiling.drawList) {
        let params = this.coordinateTranslate(this.tiling.drawList[idx]);
        if (
          params.x < this.tiling.preview.canvas.width &&
          params.y < this.tiling.preview.canvas.height &&
          params.x + params.width >= 0 &&
          params.y + params.height >= 0
        ) {
          let imgData = this.img2ImageData(params);
          if (params.lumRatio && params.lumRatio != 0) {
            imgData = changeImageLuminance(
              imgData,
              params.lumRatio + this.luminance
            );
          } else if (this.luminance !== 0) {
            changeImageLuminance(imgData, this.luminance);
          } else if (this.autoFit) {
            autoFitLuminance(imgData);
          }
          this.tiling.preview.putImageData(
            imgData,
            params.x,
            params.y,
            0,
            0,
            params.width,
            params.height
          );
        }
      }
      for (let lineIdx in this.tiling.bonding.lines) {
        let line = this.tiling.bonding.lines[lineIdx];
        this.tiling.preview.strokeStyle = "green";
        this.tiling.preview.lineWidth = Math.ceil(
          1 * this.tiling.canvasScaleRatio
        );

        // Draw a green box
        let leftTop = this.coordinateTranslate({ x: line.x1, y: line.y1 });
        let bottomRight = this.coordinateTranslate({ x: line.x2, y: line.y3 });

        this.tiling.preview.beginPath();
        this.tiling.preview.moveTo(leftTop.x, leftTop.y);
        this.tiling.preview.lineTo(leftTop.x, bottomRight.y);
        this.tiling.preview.lineTo(bottomRight.x, bottomRight.y);
        this.tiling.preview.lineTo(bottomRight.x, leftTop.y);
        this.tiling.preview.lineTo(leftTop.x, leftTop.y);
        this.tiling.preview.stroke();
      }
    },

    getCursorXY(e) {
      const screenWidth = this.canvas.offsetWidth;
      const canvasWidth = this.canvas.width;
      this.tiling.canvasScaleRatio = canvasWidth / screenWidth;

      const scaleRatio = this.tiling.canvasScaleRatio;

      const rect = this.canvas.getBoundingClientRect();
      const mouseX = (e.clientX - rect.left) * scaleRatio; // e.offsetX;
      const mouseY = (e.clientY - rect.top) * scaleRatio; // e.offsetY;
      return { mouseX, mouseY };
    },

    exportTiledImage() {
      console.log("exportTiledImage");

      tilingApi.exportTiles(response => {
        console.log(response.data);
        let blob = new Blob([response.data]);
        var link = document.createElement("a");
        link.href = window.URL.createObjectURL(blob);
        link.download = "resulted tiles.png";
        link.click();
        console.log("clicked");
      });
    },
    mouseDown(e) {
      const { mouseX, mouseY } = this.getCursorXY(e);
      let drawList = [...this.tiling.drawList].reverse();
      for (let idx in drawList) {
        let params = this.coordinateTranslate(drawList[idx]);
        if (mouseX > params.x && mouseX < params.x + params.width) {
          if (mouseY > params.y && mouseY < params.y + params.height) {
            // Start cursor position which is used to calculate the dragging offset.
            this.tiling.mouse.startX = mouseX;
            this.tiling.mouse.startY = mouseY;
            this.tiling.mouse.imgOriginX = drawList[idx].x;
            this.tiling.mouse.imgOriginY = drawList[idx].y;
            this.tiling.mouse.catchImg = true;

            // Place the image being dragging upfront.
            let movingImg = this.tiling.drawList[drawList.length - idx - 1];
            movingImg.drawingOrder = this.drawingOrder;
            this.drawingOrder++;
            this.tiling.drawList = [...this.tiling.drawList].sort(
              function compareFn(f, e) {
                return f.drawingOrder - e.drawingOrder;
              }
            );

            // The image that wille be dragged - the last one on the top.
            this.tiling.mouse.draggingImgIdx = this.tiling.drawList.length - 1;
            break;
          }
        }
      }
    },

    mouseUp() {
      if (this.tiling.mouse.catchImg) {
        this.tiling.mouse.catchImg = false;
        if (
          this.tiling.bonding.offsetX != 0 ||
          this.tiling.bonding.offsetY != 0
        ) {
          // Move image if bonding turned on.
          let movingImg = this.tiling.drawList[this.tiling.drawList.length - 1];
          if (this.tiling.bonding.offsetX != 0) {
            movingImg.x += this.tiling.bonding.offsetX;
          }
          if (this.tiling.bonding.offsetY != 0) {
            movingImg.y += this.tiling.bonding.offsetY;
          }
          this.performDrawing();
        }
      }

      // Reset bonding offset.
      this.tiling.bonding.offsetX = 0;
      this.tiling.bonding.offsetY = 0;
      this.tiling.bonding.lines = [];
    },

    mouseMove(e) {
      if (this.tiling.result.select) {
        this.canvas.style.cursor = "crosshair";
      } else {
        this.canvas.style.cursor = "grab";
      }

      if (!this.tiling.mouse.catchImg) return;
      if (
        this.tiling.mouse.moveTime &&
        Date.now() - this.tiling.mouse.moveTime < 16
      )
        return; // throttle
      const { mouseX, mouseY } = this.getCursorXY(e);

      let movingImg = this.tiling.drawList[this.tiling.drawList.length - 1];
      let movingParam = this.coordinateTranslateReverse({
        width: mouseX - this.tiling.mouse.startX,
        height: mouseY - this.tiling.mouse.startY
      });

      let newImgX = this.tiling.mouse.imgOriginX + movingParam.width;
      let newImgY = this.tiling.mouse.imgOriginY + movingParam.height;

      movingImg.x = newImgX;
      movingImg.y = newImgY;

      if (this.tiling.bonding.snapToEdge || this.tiling.bonding.patternMatch) {
        this.calculateBondingOffsets(movingImg);
      }
      this.performDrawing();
    },
    mouseScroll(e) {
      e.preventDefault();
      e.stopPropagation();
      const { wheelDelta, offsetX, offsetY } = e;
      const step = wheelDelta > 0 ? 0.01 : -0.01;
      const currentScale = +(this.tiling.canvasScale + step).toFixed(2);
      this.tiling.canvasScale = currentScale;
      if (this.overflowCanvas) {
        this.translateX =
          offsetX -
          ((offsetX - this.translateX) * currentScale) / this.frontScale;
        this.translateY =
          offsetY -
          ((offsetY - this.translateY) * currentScale) / this.frontScale;
      } else {
        this.translateX = 0;
        this.translateY = 0;
      }
      this.performDrawing();
      this.frontScale = currentScale;
    },

    // All coordinates are in real HD image sizes.
    calculateBondingOffsets(movingImg) {
      this.tiling.bonding.offsetX = 0;
      this.tiling.bonding.offsetY = 0;

      let withinHorizontal = this.tiling.drawList.filter(item => {
        return imgYDistance(item, movingImg) < movingImg.height / 3;
        // return (
        //   (item.y >= movingImg.y && item.y < movingImg.y + movingImg.height) ||
        //   (item.y + item.height > movingImg.y &&
        //     item.y + item.height <= movingImg.y + movingImg.height)
        // );
      });
      // console.log("withinHorizontal: " + withinHorizontal.map(i => i.orgIdx));
      let withinVertical = this.tiling.drawList.filter(item => {
        return imgXDistance(item, movingImg) < movingImg.width / 3;
        // return (
        //   (item.x >= movingImg.x && item.x < movingImg.x + movingImg.width) ||
        //   (item.x + item.width > movingImg.x &&
        //     item.x + item.width <= movingImg.x + movingImg.width)
        // );
      });

      let horizonItemsAll = withinHorizontal.filter(i => {
        let cross = withinVertical.filter(j => {
          return j.orgIdx == i.orgIdx;
        });
        return cross.length == 0;
      });
      let horizontalOneside =
        horizonItemsAll.filter(item => item.x >= movingImg.x).length ==
          horizonItemsAll.length ||
        horizonItemsAll.filter(item => item.x <= movingImg.x).length ==
          horizonItemsAll.length;

      let verticalItemsAll = withinVertical.filter(i => {
        let cross = withinHorizontal.filter(j => {
          return j.orgIdx == i.orgIdx;
        });
        return cross.length == 0;
      });
      let verticalOneside =
        verticalItemsAll.filter(item => item.y >= movingImg.y).length ==
          verticalItemsAll.length ||
        verticalItemsAll.filter(item => item.y <= movingImg.y).length ==
          verticalItemsAll.length;

      // let crossItems = withinVertical.filter(i => {
      //   let cross = withinHorizontal.filter(j => {
      //     return j.orgIdx == i.orgIdx
      //   });
      //   return cross.length != 0;
      // });

      let minHorizonDistance = Math.min(
        ...horizonItemsAll.map(item => {
          return imgHorizontalDistance(item, movingImg);
        })
      );
      let horizonItems = horizonItemsAll.filter(item => {
        return imgHorizontalDistance(item, movingImg) == minHorizonDistance;
      });

      let minVerticalDistance = Math.min(
        ...verticalItemsAll.map(item => {
          return imgVerticalDistance(item, movingImg);
        })
      );
      let verticalItems = verticalItemsAll.filter(
        item => imgVerticalDistance(item, movingImg) == minVerticalDistance
      );

      let horizonItem = horizonItems.length > 0 ? horizonItems[0] : null;
      let verticalItem = verticalItems.length > 0 ? verticalItems[0] : null;

      // if (horizonItems.length == 1) {
      //   console.log("Strange 1!!!");
      //   console.log(horizonItemsAll.map(i => imgXDistance(i, movingImg)));
      //   console.log("min dis:" + minHorizonDistance);
      // }
      // if (verticalItems.length == 1) {
      //   console.log("Strange 1!!!");
      //   console.log(verticalItemsAll.map(i => imgYDistance(i, movingImg)));
      //   console.log("min dis:" + minVerticalDistance);
      // }

      // console.log(
      //   "horizonItems.len : " +
      //     horizonItems.length +
      //     "\n  verticalItems.len: " +
      //     verticalItems.length
      // );

      if (horizonItem != null) {
        if (horizontalOneside) {
          let edgeDis =
            horizonItem.x > movingImg.x
              ? movingImg.x
              : this.tiling.totalImagesWith - movingImg.x - movingImg.width;

          let itemDis = imgXDistance(horizonItem, movingImg);

          this.tiling.bonding.offsetX =
            edgeDis < itemDis
              ? horizonItem.x > movingImg.x
                ? -movingImg.x
                : this.tiling.totalImagesWith - movingImg.x - movingImg.width
              : horizonItem.x > movingImg.x
              ? horizonItem.x - movingImg.x - movingImg.width
              : horizonItem.x - movingImg.x + horizonItem.width;
        } else {
          this.tiling.bonding.offsetX =
            horizonItem.x > movingImg.x
              ? horizonItem.x - movingImg.x - movingImg.width
              : horizonItem.x - movingImg.x + horizonItem.width;
        }
      } else {
        let rightDis =
          this.tiling.totalImagesWith - movingImg.x - movingImg.width;
        let leftDis = movingImg.x;
        this.tiling.bonding.offsetX = rightDis > leftDis ? -leftDis : rightDis;
      }

      if (Math.abs(this.tiling.bonding.offsetX) > movingImg.width) {
        this.tiling.bonding.offsetX = 0;
      }

      if (verticalItem != null) {
        if (verticalOneside) {
          let edgeDis =
            verticalItem.y > movingImg.y
              ? movingImg.y
              : this.tiling.totalImagesWith - movingImg.y - movingImg.height;

          let itemDis =
            Math.abs(verticalItem.y - movingImg.y) - movingImg.height;

          this.tiling.bonding.offsetY =
            edgeDis < itemDis
              ? verticalItem.y > movingImg.y
                ? -movingImg.y
                : this.tiling.totalImagesWith - movingImg.y - movingImg.height
              : verticalItem.y > movingImg.y
              ? verticalItem.y - movingImg.y - movingImg.height
              : verticalItem.y - movingImg.y + verticalItem.height;
        } else {
          this.tiling.bonding.offsetY =
            verticalItem.y > movingImg.y
              ? verticalItem.y - movingImg.y - movingImg.height
              : verticalItem.y - movingImg.y + verticalItem.height;
        }
      } else {
        let topDis = movingImg.y;
        let bottomDis =
          this.tiling.totalImagesWith - movingImg.y - movingImg.height;
        this.tiling.bonding.offsetY = topDis > bottomDis ? bottomDis : -topDis;
      }

      if (Math.abs(this.tiling.bonding.offsetY) > movingImg.height) {
        this.tiling.bonding.offsetY = 0;
      }

      if (this.tiling.bonding.patternMatch) {
        let partternMatchOffsets = this.calculatePatternMatch(
          movingImg,
          horizonItems,
          verticalItems
        );
        if (
          Math.abs(this.tiling.bonding.offsetX) >
          Math.abs(this.tiling.bonding.offsetY)
        ) {
          this.tiling.bonding.offsetX = partternMatchOffsets.offsetX;
        } else {
          this.tiling.bonding.offsetY = partternMatchOffsets.offsetY;
        }
      } else {
        // console.log("SN: " + this.tiling.bonding.offsetY);
      }

      if (
        this.tiling.bonding.offsetX != 0 ||
        this.tiling.bonding.offsetY != 0
      ) {
        this.tiling.bonding.lines = [];
        this.tiling.bonding.lines.push({
          x1: movingImg.x + this.tiling.bonding.offsetX,
          y1: movingImg.y + this.tiling.bonding.offsetY,
          x2: movingImg.x + this.tiling.bonding.offsetX + movingImg.width,
          y2: movingImg.y + this.tiling.bonding.offsetY + movingImg.height
        });
      } else {
        this.tiling.bonding.lines = [];
      }
    },

    // Apply pattern matching algorithms
    calculatePatternMatch(movingImg, horizonImgs, verticalImgs) {
      // console.log("calculatePatternMatch");
      // console.log("horizonImgs Ys: " + horizonImgs.map(i => i.y));
      if (horizonImgs.length > 1) {
        horizonImgs = [...horizonImgs]
          .sort(function(a, b) {
            return Math.abs(a.y - movingImg.y) - Math.abs(b.y - movingImg.y);
          })
          .slice(0, 1);
      } else {
        console.log("horizonImgs.length is 1");
      }
      // console.log("hImage picked Y: " + horizonImgs[0].y);

      // console.log("verticalImgs Xs: " + verticalImgs.map(i => i.x));

      if (verticalImgs.length > 1) {
        verticalImgs = [...verticalImgs]
          .sort(function(a, b) {
            return Math.abs(a.x - movingImg.x) - Math.abs(b.x - movingImg.x);
          })
          .slice(0, 1);
      } else {
        console.log("verticalImgs.length is 1");
      }
      // console.log("vImage picked X: " + verticalImgs[0].x);

      // Get row Image data
      if (movingImg.imageDataCache == null) {
        movingImg.imageDataCache = this.img2ImageData(movingImg);
      }
      for (let idx in horizonImgs) {
        let img = horizonImgs[idx];
        if (img.imageDataCache == null) {
          img.imageDataCache = this.img2ImageData(img);
        }
      }
      for (let idx in verticalImgs) {
        let img = verticalImgs[idx];

        if (img.imageDataCache == null) {
          img.imageDataCache = this.img2ImageData(img);
        }
      }
      // Get row Image data end....

      // Get the vertical matching line
      const verticalMatchingLine = [];
      var verticalMatchingLineY = 0;
      var verticalLine = [];
      if (horizonImgs.length > 0) {
        horizonImgs = [...horizonImgs].sort(function(a, b) {
          return a.y - b.y;
        });

        // console.log("org idx: ");
        // console.log(horizonImgs.map(i => i.orgIdx));
        // console.log(horizonImgs.map(i => i.y));

        verticalMatchingLineY = horizonImgs[0].y;

        horizonImgs.forEach(function(img, index, arr) {
          if (img.x > movingImg.x) {
            verticalMatchingLine.push(...getImageEdge(img.imageDataCache, 4));
          } else {
            verticalMatchingLine.push(...getImageEdge(img.imageDataCache, 2));
          }
        });
        // console.log(
        //   "verticalMatchingLine.length: " + verticalMatchingLine.length
        // );

        if (horizonImgs[0].x > movingImg.x) {
          verticalLine = getImageEdge(movingImg.imageDataCache, 2);
        } else {
          verticalLine = getImageEdge(movingImg.imageDataCache, 4);
        }
      }

      // Get the horizontal matching line
      const horizontalMatchingLine = [];
      var horizontalMatchingLineX = 0;
      var horizontalLine = [];
      if (verticalImgs.length > 0) {
        verticalImgs = [...verticalImgs].sort(function(a, b) {
          return a.x - b.x;
        });
        horizontalMatchingLineX = verticalImgs[0].x;

        verticalImgs.forEach(function(img, index, arr) {
          if (img.y > movingImg.y) {
            horizontalMatchingLine.push(...getImageEdge(img.imageDataCache, 1));
          } else {
            horizontalMatchingLine.push(...getImageEdge(img.imageDataCache, 3));
          }
        });
        // console.log(
        //   "horizontalMatchingLine.length: " + horizontalMatchingLine.length
        // );

        if (verticalImgs[0].y > movingImg.y) {
          horizontalLine = getImageEdge(movingImg.imageDataCache, 3);
        } else {
          horizontalLine = getImageEdge(movingImg.imageDataCache, 1);
        }
      }

      // console.log("verticalMatchingLine: " + verticalMatchingLine.length);
      // console.log("verticalLine: " + verticalLine.length);

      // console.log("horizontalMatchingLine: " + horizontalMatchingLine.length);
      // console.log("horizontalLine: " + horizontalLine.length);

      var offsetY = 0;
      if (verticalMatchingLine.length > 0) {
        // console.log("verticalMatchingLine about to call matchPixcels");
        let verticalPMOffset = matchPixels(verticalMatchingLine, verticalLine);
        offsetY = verticalMatchingLineY + verticalPMOffset - movingImg.y;
      }

      var offsetX = 0;
      if (horizontalMatchingLine.length > 0) {
        // console.log("horizontalMatchingLine about to call matchPixcels");
        let horizontalPMOffset = matchPixels(
          horizontalMatchingLine,
          horizontalLine
        );
        offsetX = horizontalMatchingLineX + horizontalPMOffset - movingImg.x;
      }

      return {
        offsetX: offsetX,
        offsetY: offsetY
      };
    },

    mouseLeave() {
      this.tiling.mouse.catchImg = false;
    },

    doMatch(item1, item2, direction, overlap) {
      let horizontalMatch = direction == 0;
      let img1 = cv.imread(item1.image);
      let img2 = cv.imread(item2.image);

      let totalRow = Math.min(img1.rows, img2.rows);
      let totalCol = Math.min(img1.cols, img2.cols);
      let overlapDepth = horizontalMatch ? totalCol : totalRow;
      let loopDepth = horizontalMatch ? totalRow : totalCol;

      if (overlap > overlapDepth) overlap = overlapDepth;

      const tryOffset = Math.ceil(overlapDepth / 10);
      let matchRes = [];
      for (let i = -tryOffset; i <= tryOffset; i++) {
        matchRes.push([]);
      }

      let step = Math.round(overlap / 5);
      if (step == 0) step = 1;
      for (let overlapPt2 = 0; overlapPt2 < overlap; overlapPt2 += step) {
        let overlapPt1 = overlapDepth - overlap + overlapPt2;

        for (let ofs = -tryOffset; ofs <= tryOffset; ofs++) {
          // console.log("ofs: " + ofs + " c1:" + c1 + " c2:" + c2);
          for (let loopPt1 = 0; loopPt1 < loopDepth; loopPt1++) {
            let loopPt2 = loopPt1 - ofs;

            if (
              loopPt1 < 0 ||
              loopPt2 < 0 ||
              loopPt1 >= loopDepth ||
              loopPt2 >= loopDepth
            ) {
              continue;
            }

            // console.log("(" + r1 + "," + c1 + ") - (" + r2 + "," + c2 + ")");
            let pixel1 = horizontalMatch
              ? img1.ucharPtr(loopPt1, overlapPt1)
              : img1.ucharPtr(overlapPt1, loopPt1);
            let pixel2 = horizontalMatch
              ? img2.ucharPtr(loopPt2, overlapPt2)
              : img2.ucharPtr(overlapPt2, loopPt2);

            let totalDiff = 0;
            for (let i = 0; i < 3; i++) {
              totalDiff += Math.abs(pixel1[i] - pixel2[i]);
            }
            matchRes[ofs + tryOffset].push(totalDiff);
          }
        }
      }

      // console.log(matchRes);
      matchRes = matchRes.map(diffs => {
        let total = diffs.reduce((prev, curr) => {
          return prev + curr;
        }, 0);
        return Math.round((total / diffs.length) * 10000);
      });

      let minDiff = Math.min(...matchRes);
      let bestOff = matchRes.findIndex(element => {
        return element == minDiff;
      });
      bestOff = bestOff - tryOffset;

      // console.log(matchRes);
      // console.log("minDiff: " + minDiff);
      // console.log("bestIdx: " + bestOff);

      img1.delete();
      img2.delete();
      return bestOff;
    },

    async autoPatternMathing() {
      let that = this;
      that.drawImages2();

      let rowOffsets = [];
      for (let r = 0; r < this.tiling.alignment.rows; r++) {
        rowOffsets.push([]);
      }
      let colOffsets = [];
      for (let c = 0; c < this.tiling.alignment.cols; c++) {
        colOffsets.push([]);
      }

      for (let r = 0; r < this.tiling.alignment.rows; r++) {
        for (let c = 0; c < this.tiling.alignment.cols; c++) {
          let targetItem = this.tiling.drawList.find(function(drawItem) {
            return drawItem.row == r && drawItem.col == c;
          });
          let leftItem = this.tiling.drawList.find(function(drawItem) {
            return drawItem.row == r && drawItem.col == c - 1;
          });
          let topItem = this.tiling.drawList.find(function(drawItem) {
            return drawItem.row == r - 1 && drawItem.col == c;
          });

          if (targetItem && leftItem) {
            if (leftItem) {
              let verticalOffset = this.doMatch(
                leftItem,
                targetItem,
                0,
                this.tiling.bonding.overlapX
              );
              colOffsets[c].push(verticalOffset);
            }
          } else if (targetItem) {
            colOffsets[c].push(0);
          }

          if (targetItem && topItem) {
            if (topItem) {
              let horizontalOffset = this.doMatch(
                topItem,
                targetItem,
                1,
                this.tiling.bonding.overlapY
              );
              rowOffsets[r].push(horizontalOffset);
            }
          } else if (targetItem) {
            rowOffsets[r].push(0);
          }
        }
      }

      function avgValues(offsValues) {
        if (offsValues.length == 0) return 0;

        return offsValues.map(offValues => {
          if (offValues.length == 0) return 0;
          let sum = offValues.reduce((prev, v) => {
            return prev + v;
          });

          if (sum == 0) return 0;

          return Math.round(sum / offValues.length);
        });
      }

      rowOffsets = avgValues(rowOffsets);
      colOffsets = avgValues(colOffsets);

      function cumulate(offsValues, overlap) {
        let cumulatedValue = overlap;
        return offsValues.map(item => {
          cumulatedValue += item;
          cumulatedValue - overlap;
          return cumulatedValue;
        });
      }

      console.log(rowOffsets);
      console.log(colOffsets);

      rowOffsets = cumulate(rowOffsets, this.tiling.bonding.overlapX);
      colOffsets = cumulate(colOffsets, this.tiling.bonding.overlapY);

      console.log(rowOffsets);
      console.log(colOffsets);

      // this.tiling.bonding.overlapX;
      // this.tiling.bonding.overlapY;
      // Apply the offsets
      for (let r = 0; r < this.tiling.alignment.rows; r++) {
        for (let c = 0; c < this.tiling.alignment.cols; c++) {
          let targetItem = this.tiling.drawList.find(function(drawItem) {
            return drawItem.row == r && drawItem.col == c;
          });

          if (targetItem) {
            targetItem.x += rowOffsets[r];

            targetItem.y += colOffsets[c];
          }
        }
      }

      // this.tiling.drawList.forEach(function(item) {
      //   that.calculateBondingOffsets(item);
      //   if (that.tiling.bonding.offsetX != 0) {
      //     item.x += that.tiling.bonding.offsetX;
      //   }
      //   if (that.tiling.bonding.offsetY != 0) {
      //     item.y += that.tiling.bonding.offsetY;
      //   }
      // });
      // this.findImageTo(this.tiling.drawList, )
      //
      // this.performDrawing();
      // if (this.tiling.alignment.rows > 0 && this.tiling.alignment.cols > 0) {
      //   const r = this.tiling.alignment.rows;
      //   const c = this.tiling.alignment.cols;
      // }
    }
  },

  // Find the image to the top/left/boom/right of the target image in the list.
  // the list to loop through
  // direction - 0: top, 1: right, 2: bottom, 3: left.
  // imageIdx - The target img
  // return the found image idx;
  findImageTo(imgList, imageIdx, direction) {
    let targetItem = imgList[imageIdx];

    let findBig = direction == 0 || direction == 3;
    let compareX = direction == 1 || direction == 3;

    let targetV = compareX ? targetItem.x : targetItem.y;

    var lastV = -1;
    var foundIdx = -1;

    imgList.forEach(function(item, idx) {
      let itemV = compareX ? item.x : item.y;

      let found =
        lastV < 0 ||
        (findBig
          ? itemV > lastV && itemV < targetV
          : itemV < lastV && itemV > targetV);

      if (found) {
        lastV = itemV;
        foundIdx = idx;
      }
    });

    return foundIdx;
  },

  created() {
    this.filesWatch = this.$store.watch(
      (state, getters) => getters["files/position/getFilesUpdatedCount"],
      async count => {
        if (this.tiling.preview) {
          this.translateX = 0;
          this.translateY = 0;
          this.frontScale = 1;
          this.tiling.canvasScale = TILING_SCALE_OPTIONS[2] / 100;
          this.drawImages();
        }
      }
    );
  },

  beforeDestroy() {
    this.filesWatch();
  },

  renderTriggered({ key, target, type }) {
    // console.log("callback debug renderTriggered !!!!");
    // console.log({ key, target, type });
  },

  updated() {
    // console.log("callback debug updated !!!!");
    this.$nextTick(function() {});
  },

  mounted() {
    this.$nextTick(function() {
      if (this.tiling.preview == null) {
        this.canvas = document.getElementById("canvas");
        this.canvas.width = TILING_CANVAS_SIZE;
        this.canvas.height = TILING_CANVAS_SIZE;
        this.tiling.preview = this.canvas.getContext("2d");

        this.canvas.addEventListener("mousedown", this.mouseDown); // 鼠标按下
        this.canvas.addEventListener("mouseup", this.mouseUp); // 鼠标释放弹起
        this.canvas.addEventListener("mousemove", this.mouseMove);
        this.canvas.addEventListener("mouseleave", this.mouseLeave);
        this.canvas.addEventListener("mousewheel", this.mouseScroll);
      }

      if (this.files && this.files.length) {
        this.getImageSize();
        this.drawImages(); // 刷新drawingIntervalNeedRedraw
      }

      /* For some reason the previous dev is calling this every second for the
       * life of the component */
      if (this.drawingIntervalHd == null) {
        let that = this;
        this.drawingIntervalHd = setInterval(function() {
          if (that.drawingIntervalNeedPerformingDrawing) {
            that.performDrawing();
            that.drawingIntervalNeedPerformingDrawing = false;
          }
          if (that.drawingIntervalNeedRedraw) {
            that.drawImages2();
            that.drawingIntervalNeedRedraw = false;
          }
        }, 1000);
      }
    });
  },

  beforeUnmount() {
    if (this.drawingIntervalHd) {
      clearInterval(this.drawingIntervalHd);
      this.drawingIntervalHd = null;
    }
    if (this.canvas) {
      this.canvas.removeEventListener("mousedown", this.mouseDown); // 鼠标按下
      this.canvas.removeEventListener("mouseup", this.mouseUp); // 鼠标释放弹起
      this.canvas.removeEventListener("mousemove", this.mouseMove);
      this.canvas.removeEventListener("mouseleave", this.mouseLeave);
      this.canvas?.removeEventListener("mousescroll", this.mouseScroll);

      // console.log("drag events removed");
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
  width: calc(100% - 520px);
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
</style>
