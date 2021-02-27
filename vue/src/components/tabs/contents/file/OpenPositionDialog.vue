<template>
  <div style="display:none;">
    <input type="file" id="uploadFile" @change="requestUploadFile" />
    <v-dialog v-model="visibleDialog" max-width="980">
      <simple-dialog
        title="Position"
        :singleButton="false"
        okTitle="Select"
        @select="visibleDialog = false"
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

        <v-tabs-items v-model="selectedTab">
          <v-tab-item value="tabs-images">
            <v-sheet
              class="drop pa-5"
              height="350"
              :class="getClasses"
              @dragover.prevent="dragOver"
              @dragleave.prevent="dragLeave"
              @drop.prevent="drop($event)"
            >
              <div
                class="d-flex align-center justify-center"
                style="height: 200px;"
              >
                <p
                  v-if="!imgFiles.length"
                  class="text-h4 grey--text text--lighten-2"
                >
                  Drag and Drop.
                </p>
                <v-row v-else class="align-center justify-center row-style">
                  <div
                    class="img-align"
                    v-for="(imgFile, idx) in imgFiles"
                    :key="idx"
                    @click="selectImage(idx)"
                    :style="
                      idx === curImgIdx
                        ? { background: 'rgb(204,232,255)' }
                        : {}
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
              </div>
            </v-sheet>
          </v-tab-item>
          <v-tab-item value="tabs-tiling">
            <v-sheet
              class="drop pa-5"
              height="350"
              :class="getClasses"
              @dragover.prevent="dragOver"
              @dragleave.prevent="dragLeave"
              @drop.prevent="drop($event)"
            >
              <div
                class="d-flex align-center justify-center"
                style="height: 200px;"
              >
                <p
                  v-if="!imageSource"
                  class="text-h4 grey--text text--lighten-2"
                >
                  Drag and Drop.
                </p>
              </div>
            </v-sheet>
          </v-tab-item>
          <v-tab-item value="tabs-metadata">
            <v-sheet
              class="drop pa-5"
              height="350"
              :class="getClasses"
              @dragover.prevent="dragOver"
              @dragleave.prevent="dragLeave"
              @drop.prevent="drop($event)"
            >
              <div
                class="d-flex align-center justify-center"
                style="height: 200px;"
              >
                <p
                  v-if="!imageSource"
                  class="text-h4 grey--text text--lighten-2"
                >
                  Drag and Drop.
                </p>
              </div>
            </v-sheet>
          </v-tab-item>
          <v-tab-item value="tabs-name-type">
            <v-sheet
              class="drop pa-5"
              height="350"
              :class="getClasses"
              @dragover.prevent="dragOver"
              @dragleave.prevent="dragLeave"
              @drop.prevent="drop($event)"
            >
              <div
                class="d-flex align-center justify-center"
                style="height: 200px;"
              >
                <p
                  v-if="!imageSource"
                  class="text-h4 grey--text text--lighten-2"
                >
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
    imageSource: null,
    imageData: null,
    selectedTab: null,
    imgFiles: [],
    imgDatas: [],
    curImgIdx: -1
  }),

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
          if (
            file &&
            file.type.startsWith("image/") &&
            !file.type.startsWith("image/tif")
          ) {
            this.imgFiles.push(file);

            var self = this;
            const reader = new FileReader();
            reader.onload = function() {
              let res = reader.result;
              if (res) {
                self.imgDatas.push(res);
              }
            };
            reader.readAsDataURL(file);
          }
        }
      }
    },
    onSelect() {
      this.visibleDialog = false;

      if (this.curImgIdx < this.imgFiles.length) {
        let imgFile = this.imgFiles[this.curImgIdx];
        if (imgFile) {
          var formData = new FormData();
          formData.append("sourceImage", imgFile);
          this.$store.dispatch("image/setImage", formData);
        }
      }
    },
    onCancel() {
      this.imgFiles = null;
      this.imgDatas = null;

      this.visibleDialog = false;
    },
    selectImage(idx) {
      this.curImgIdx = idx;
      console.log(this.curImgIdx);
    }
  },
  watch: {
    imageURL(idx) {
      return this.imgDatas.length > idx
        ? this.imgDatas[idx]
                : require("../../../../assets/images/no-preview.png");
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
.row-style {
  margin-top: 150px;
  margin-bottom: 20px;
  overflow: auto;
  height: 330px;
}
#uploadFile {
  display: none;
}
</style>
