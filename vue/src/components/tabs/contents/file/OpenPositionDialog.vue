<template>
  <div style="display:none;">
    <input type="file" id="uploadFile" @change="requestUploadFile" />
    <v-dialog v-model="visibleDialog" max-width="980">
      <simple-dialog
        title="Position"
        :singleButton="false"
        okTitle="Select"
        @select="onSelect"
        @close="onCancel"
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
                v-if="!allFiles.length"
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
                    v-if="curFileIdx == allFiles.length - 1"
                    depressed
                    disabled
                  >
                    Update
                  </v-btn>
                  <v-btn v-else depressed color="primary" @click="update">
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
                  :headers="headers"
                  :items="contents"
                  :search="search"
                  item-key="no"
                >
                  <template v-slot:body="{ items }">
                    <tbody>
                      <tr
                        :style="
                          key === curMetaIdx
                            ? { background: 'rgb(204,232,255)' }
                            : {}
                        "
                        @click="selected(key)"
                        v-for="(item, key) in items"
                        :key="item.no"
                      >
                        <td>{{ item.no }}</td>
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
                v-if="!typeFiles.length"
                class="d-flex align-center justify-center"
                style="height: 200px;"
              >
                <p class="text-h4 grey--text text--lighten-2">
                  Drag and Drop.
                </p>
              </div>
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
    allFiles: [],
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

    // for filename type
    typeFiles: [],
    typeDatas: [],
    curTypeIdx: -1,

    search: "",
    headers: [
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
    contents: []
  }),

  created() {
    this.unwatch = this.$store.watch(
      (state, getters) => getters["image/metadatas"],
      res => {
        for (var key in res) {
          this.curFileIdx = parseInt(key.split("_")[1]);
          if (this.curFileIdx < this.allFiles.length) {
            if (res[key]) {
              this.metaFiles.push(this.allFiles[this.curFileIdx]);
              this.metaDatas.push(res[key]);

              let coreMetadata = res[key].coreMetadata;
              this.contents.push({
                no: this.metaDatas.length,
                filename: this.allFiles[this.curFileIdx].name,
                series: coreMetadata.seriesCount,
                frame: coreMetadata.imageCount,
                c: coreMetadata.currentSeries,
                size_c: coreMetadata.sizeC,
                size_t: coreMetadata.sizeT,
                size_x: coreMetadata.sizeX,
                size_y: coreMetadata.sizeY,
                size_z: coreMetadata.sizeZ
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
            this.allFiles.push(file);
          }
        }
      }
    },
    onSelect() {
      switch (this.selectedTab) {
        case "tabs-images":
          if (-1 < this.curImgIdx && this.curImgIdx < this.imgFiles.length) {
            let imgData = this.imgDatas[this.curImgIdx];
            if (imgData) {
              this.$store.dispatch("image/setImageDataFromPosition", imgData);
            }
          }
          break;

        case "tabs-metadata":
          if (-1 < this.curMetaIdx && this.curMetaIdx < this.metaFiles.length) {
            let metadata = this.metaDatas[this.curMetaIdx];
            if (metadata) {
              this.$store.dispatch("image/setMetadataFromPosition", metadata);
              this.visibleDialog = false;
            }
          }
          break;
      }

      this.visibleDialog = false;
    },
    onCancel() {
      this.imgFiles = null;
      this.imgDatas = null;

      this.visibleDialog = false;
    },
    selectImage(idx) {
      this.curImgIdx = idx;
    },
    selected(key) {
      this.curMetaIdx = key;
    },
    update() {
      if (this.curFileIdx < this.allFiles.length - 1) {
        var formData = new FormData();
        for (var i = this.curFileIdx + 1; i < this.allFiles.length; i++) {
          formData.append("metafile" + "_" + i, this.allFiles[i]);
        }
        this.$store.dispatch("image/setMetaFiles", formData);
      }
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
</style>
