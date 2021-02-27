<template>
  <div style="display:none;">
    <input type="file" id="uploadFile" @change="requestUploadFile" />
    <v-dialog v-model="visibleDialog" max-width="980">
      <simple-dialog
        title="File"
        :singleButton="false"
        okTitle="Select"
        @select="onSelect"
        @close="onCancel"
      >
        <v-sheet
          class="drop pa-5"
          height="350"
          :class="getClasses"
          @dragover.prevent="dragOver"
          @dragleave.prevent="dragLeave"
          @drop.prevent="drop($event)"
        >
          <v-btn class="d-block text-none" color="primary" text>
            <v-icon class="mr-3">
              mdi-folder
            </v-icon>
            Use f for closed files
          </v-btn>
          <v-btn
            class="d-block text-none"
            color="primary"
            text
            @click="openFile"
          >
            <v-icon class="mr-3">
              mdi-folder-open
            </v-icon>
            Use F for opened files
          </v-btn>
          <div
            class="d-flex align-center justify-center"
            style="height: 250px;"
          >
            <p v-if="!imageSource" class="text-h4 grey--text text--lighten-2">
              Open or drop your file.
            </p>
            <v-row v-else class="align-center justify-center">
              <v-img
                :src="imageURL"
                :style="
                  imageURL.startsWith('data:')
                    ? {}
                    : {
                        border: '1px solid grey'
                      }
                "
                max-width="150"
                width="150"
                height="150"
                contain
              />
              <p class="ms-5">
                {{ imageSource.name }}
              </p>
            </v-row>
          </div>
        </v-sheet>
      </simple-dialog>
    </v-dialog>
  </div>
</template>

<script>
// import { mapGetters } from "vuex";
import tiff from "tiff.js";
import atob from "atob";

import SimpleDialog from "../../../custom/SimpleDialog";

export default {
  name: "OpenFileDialog",

  components: { SimpleDialog },

  data: () => ({
    isDragging: false,
    imageSource: null,
    imageData: null
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
    },
    imageURL() {
      return this.imageData
        ? this.imageData
        : require("../../../../assets/images/no-preview.png");
    }
  },

  methods: {
    base64ToArrayBuffer(base64) {
      var binary_string = atob(base64);
      var len = binary_string.length;
      var bytes = new Uint8Array(len);
      for (var i = 0; i < len; i++) {
        bytes[i] = binary_string.charCodeAt(i);
      }
      return bytes.buffer;
    },
    openFile() {
      this.$el.querySelector("#uploadFile").click();
    },
    dragOver() {
      this.isDragging = true;
    },
    dragLeave() {
      this.isDragging = false;
    },
    drop(e) {
      this.isDragging = false;

      // const entry = e.dataTransfer.items[0].webkitGetAsEntry();
      // alert(entry.fullPath);

      const fileInput = this.$el.querySelector("#uploadFile");
      fileInput.files = e.dataTransfer.files;

      this.requestUploadFile();

      e.preventDefault();
    },
    requestUploadFile() {
      const fileInput = this.$el.querySelector("#uploadFile");

      if (fileInput.files && fileInput.files.length > 0) {
        this.imageSource = fileInput.files[0];
        this.imageData = null;

        if (
          this.imageSource &&
          this.imageSource.type.startsWith("image/") &&
          this.imageSource.size < 2 * 1024 * 1024
        ) {
          var self = this;
          const reader = new FileReader();
          reader.onload = function() {
            if (self.imageSource.type.startsWith("image/tif")) {
              const buffer = self.base64ToArrayBuffer(
                reader.result.substring(23)
              );
              const tiff_data = new tiff({ buffer });
              self.imageData = tiff_data.toDataURL();
            } else {
              self.imageData = reader.result;
            }
          };
          reader.readAsDataURL(this.imageSource);
        }
      }
    },
    onSelect() {
      this.visibleDialog = false;

      if (this.imageSource) {
        var formData = new FormData();
        formData.append("sourceImage", this.imageSource);
        this.$store.dispatch("image/setImage", formData);
      }

      if (this.imageSource) this.imageSource = null;
      if (this.imageData) this.imageData = null;
    },
    onCancel() {
      if (this.imageSource) this.imageSource = null;
      if (this.imageData) this.imageData = null;

      this.visibleDialog = false;
    }
  }
};
</script>

<style scoped>
.isDragging {
  background-color: #e0f2f1;
  border-color: #fff;
}
#uploadFile {
  display: none;
}
</style>
