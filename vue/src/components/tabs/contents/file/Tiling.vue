<template>
  <v-sheet class="drop pa-5" height="600">
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
                <v-checkbox
                  v-model="tiling.bonding.snapToEdge"
                  label="Snap To Edge"
                  color="primary"
                  :value="true"
                  hide-details
                  :disabled="
                    tiling.alignment.disables[tiling.alignment.activeMode].chkLR
                  "
                  @change="changeSnapToEdge"
                ></v-checkbox>
              </div>
            </v-card>
            <!-- Shading -->
            <v-card v-else-if="tiling.activeMenuItem == 3" flat>
              <v-card-title class="pa-1">Shading</v-card-title>
              <div class="inside"></div>
            </v-card>
            <!-- Display -->
            <v-card v-else-if="tiling.activeMenuItem == 4" flat>
              <v-card-title class="pa-1">Display</v-card-title>
              <div class="inside">
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
              </div>
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
          <canvas id="canvas" class="mt-15 canvas" ref="canvasElement"></canvas>
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
import { changeImageLuminance } from "../../../../utils/img-chg";
import {
  POSITION_DIALOG_CANVAS_MAX_PIXEL,
  POSITION_DIALOG_COL_COUNT,
  POSITION_DIALOG_CELL_SIZE
  // POSITION_DIALOG_STROKE_WIDTH
} from "../../../../utils/constants";

const positionModule = createNamespacedHelpers("files/position");

export default {
  name: "Tiling",
  components: {
    OpenPositionViewTab
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
      canvas: null,
      preview: null,
      canvasScaleRatio: 1,
      activeMenuItem: 0,
      bonding: {
        snapToEdge: false,
        lines: [],
        offsetX: 0,
        offsetY: 0
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
      mouse: {
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
    progressBarMaxValue: 0,
    luminance: 0.0
  }),

  computed: {
    ...positionModule.mapGetters({
      files: "getFiles",
      filesSortByField: "getFilesSortByField",
      channelOptions: "getChannelOptions"
    }),
    alignButtonImage() {
      return index =>
        require(`../../../../assets/images/pos_align_${index - 1}.png`);
    }
  },

  methods: {
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
    changeSnapToEdge() {
      this.performDrawing();
    },
    async getImageSize() {
      // 得到每个小图片的尺寸
      // let image = await loadImage();
      if (this.files.length > 0) {
        let image = this.files[0].imageData;
        this.imageWidth = image.width;
        this.imageHeight = image.height;
        // console.log(this.files);
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
        switch (this.tiling.alignment.activeMode) {
          case 0:
            this.drawCascade(); // 瀑布展示
            break;
          case 1:
            this.drawHeightDecreasing(); // 图片高度降序排列
            break;
          case 2:
            this.drawHeightIncreasing(); // 图片高度升序排列
            break;
          case 3:
            this.drawByXYZ();
            break;
          case 4:
            this.drawByColumns(); // 固定列数排列
            break;
          case 5:
            this.drawByRows(); // 固定行数排列
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
      this.updateImageLuminance();
    },

    updateImageLuminance: function() {
      let c = document.getElementById("canvas");
      if (this.tiling.preview == null) {
        this.tiling.preview = c.getContext("2d");
      }
      let imageData = this.tiling.preview.getImageData(0, 0, c.width, c.height);
      imageData = changeImageLuminance(imageData, this.luminance);
      // this.tiling.preview.clearRect(0,0,c.width,c.height);
      this.tiling.preview.putImageData(imageData, 0, 0);
    },

    // 增加图像亮度
    increaseImgLuminance: function() {
      this.luminance += 0.1;
      this.drawImages();
    },

    // 降低图像亮度
    decreaseImgLuminance() {
      this.luminance -= 0.1;
      this.performDrawing();
    },

    drawInit(mode, setNull = true) {
      // 初始化画布
      // console.log(mode);

      if (setNull) {
        this.tiling.alignment.rows = null;
        this.tiling.alignment.cols = null;
      }
    },

    drawCascade() {
      // 瀑布展示图片方法
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
          occupied: true,
          drawingOrder: this.drawingOrder,
          orgIdx: idx
        });
        this.drawingOrder++;

        idx++;
      }
    },

    drawHeightDecreasing() {
      // 图片高度降序排列方法
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
            occupied: true,
            drawingOrder: this.drawingOrder,
            orgIdx: idx
          });
          this.drawingOrder++;

          col++;
        }
        if (idx >= this.files.length) break;

        row++;
      }
    },

    drawHeightIncreasing() {
      // 图片高度升序排列
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
            occupied: true,
            drawingOrder: this.drawingOrder,
            orgIdx: idx
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

    drawByColumns() {
      // 固定列数排列
      this.drawInit("ByColumns", false); // 初始化画布，不删除宽高

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
            occupied: true,
            drawingOrder: this.drawingOrder,
            orgIdx: idx
          });
          this.drawingOrder++;

          r++;
        }
        if (idx >= this.files.length) break;

        c++;
        dir *= -1;
      }
    },

    drawByRows() {
      // 固定行数排列
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
              width: imageWidth,
              height: imageHeight,
              image,
              occupied: true,
              drawingOrder: this.drawingOrder,
              orgIdx: idx
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

    performDrawing() {
      this.tiling.preview.clearRect(
        0,
        0,
        this.tiling.preview.canvas.width,
        this.tiling.preview.canvas.height
      );

      for (let idx in this.tiling.drawList) {
        let params = this.tiling.drawList[idx];
        if (params.occupied) {
          this.tiling.preview.drawImage(
            params.image,
            params.x,
            params.y,
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

        // console.log(line);
        // draw a red line
        this.tiling.preview.beginPath();
        this.tiling.preview.moveTo(line.x1, line.y1);
        this.tiling.preview.lineTo(line.x1, line.y2);
        this.tiling.preview.lineTo(line.x2, line.y2);
        this.tiling.preview.lineTo(line.x2, line.y1);
        this.tiling.preview.lineTo(line.x1, line.y1);
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

    mouseDown(e) {
      const { mouseX, mouseY } = this.getCursorXY(e);
      let drawList = [...this.tiling.drawList].reverse();
      for (let idx in drawList) {
        let params = drawList[idx];
        if (params.occupied) {
          if (mouseX > params.x && mouseX < params.x + params.width) {
            if (mouseY > params.y && mouseY < params.y + params.height) {
              // Start cursor position which is used to calculate the dragging offset.
              this.tiling.mouse.startX = mouseX;
              this.tiling.mouse.startY = mouseY;
              this.tiling.mouse.imgOriginX = params.x;
              this.tiling.mouse.imgOriginY = params.y;
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
              this.tiling.mouse.draggingImgIdx =
                this.tiling.drawList.length - 1;
              break;
            }
          }
        }
      }
    },

    mouseUp() {
      if (this.tiling.mouse.catchImg) {
        this.tiling.mouse.catchImg = false;

        if (this.tiling.bonding.snapToEdge) {
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
      if (this.tiling.mouse.catchImg) {
        const { mouseX, mouseY } = this.getCursorXY(e);

        let movingImg = this.tiling.drawList[this.tiling.drawList.length - 1];

        let newImgX =
          this.tiling.mouse.imgOriginX + mouseX - this.tiling.mouse.startX;
        let newImgY =
          this.tiling.mouse.imgOriginY + mouseY - this.tiling.mouse.startY;

        movingImg.x = Math.round(newImgX);
        movingImg.y = Math.round(newImgY);

        if (this.tiling.bonding.snapToEdge) {
          this.calculateBondingOffsets(movingImg);
        }

        this.performDrawing();

        // this.drawingIntervalNeedPerformingDrawing = true;
      }
    },

    calculateBondingOffsets(movingImg) {
      let withinHorizontal = this.tiling.drawList.filter(item => {
        return (
          (item.y >= movingImg.y && item.y < movingImg.y + movingImg.height) ||
          (item.y + item.height > movingImg.y &&
            item.y + item.height <= movingImg.y + movingImg.height)
        );
      });
      let withinVertical = this.tiling.drawList.filter(item => {
        return (
          (item.x >= movingImg.x && item.x < movingImg.x + movingImg.width) ||
          (item.x + item.width > movingImg.x &&
            item.x + item.width <= movingImg.x + movingImg.width)
        );
      });

      let horizonItems = withinHorizontal.filter(i => {
        let cross = withinVertical.filter(j => {
          return j.orgIdx == i.orgIdx;
        });
        return cross.length == 0;
      });

      let verticalItems = withinVertical.filter(i => {
        let cross = withinHorizontal.filter(j => {
          return j.orgIdx == i.orgIdx;
        });
        return cross.length == 0;
      });

      // let crossItems = withinVertical.filter(i => {
      //   let cross = withinHorizontal.filter(j => {
      //     return j.orgIdx == i.orgIdx
      //   });
      //   return cross.length != 0;
      // });

      let minHorizonDistance = Math.min(...horizonItems.map(item => {
          return Math.abs(item.x - movingImg.x);
        })
      );
      horizonItems = horizonItems.filter(
        item => Math.abs(item.x - movingImg.x) == minHorizonDistance
      );

      let minVerticalDistance = Math.min(...verticalItems.map(item => {
          return Math.abs(item.y - movingImg.y);
        })
      );
      verticalItems = verticalItems.filter(
        item => Math.abs(item.y - movingImg.y) == minVerticalDistance
      );

      let horizonItem = horizonItems.length > 0 ? horizonItems[0] : null;
      let verticalItem = verticalItems.length > 0 ? verticalItems[0] : null;

      if (horizonItem != null) {
        this.tiling.bonding.offsetX =
          horizonItem.x > movingImg.x
            ? horizonItem.x - movingImg.x - movingImg.width
            : horizonItem.x - movingImg.x + horizonItem.width;
        if (Math.abs(this.tiling.bonding.offsetX) > movingImg.width) {
          this.tiling.bonding.offsetX = 0;
        }
      }

      if (verticalItem != null) {
        this.tiling.bonding.offsetY =
          verticalItem.y > movingImg.y
            ? verticalItem.y - movingImg.y - movingImg.height
            : verticalItem.y - movingImg.y + verticalItem.height;
        if (Math.abs(this.tiling.bonding.offsetY) > movingImg.height) {
          this.tiling.bonding.offsetY = 0;
        }
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

    mouseLeave() {
      this.tiling.mouse.catchImg = false;
    }
  },

  created() {
    this.filesWatch = this.$store.watch(
      (state, getters) => getters["files/position/getFilesUpdatedCount"],
      async count => {
        if (this.tiling.preview) {
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
        this.tiling.preview = this.canvas.getContext("2d");

        this.canvas.addEventListener("mousedown", this.mouseDown); // 鼠标按下
        this.canvas.addEventListener("mouseup", this.mouseUp); // 鼠标释放弹起
        this.canvas.addEventListener("mousemove", this.mouseMove);
        this.canvas.addEventListener("mouseleave", this.mouseLeave);
      }

      if (this.files && this.files.length) {
        this.getImageSize();
        this.drawImages();
      }

      if (this.drawingIntervalHd == null) {
        let that = this;
        this.drawingIntervalHd = setInterval(function() {
          if (that.drawingIntervalNeedPerformingDrawing) {
            // console.log("Need performing drawing!");
            that.performDrawing();
            that.drawingIntervalNeedPerformingDrawing = false;
          }
          if (that.drawingIntervalNeedRedraw) {
            // console.log("Need redraw!");
            that.drawImages2();
            that.drawingIntervalNeedRedraw = false;
          }
        }, 300);
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
</style>
