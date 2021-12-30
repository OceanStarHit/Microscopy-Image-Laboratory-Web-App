<template>
  <div style="display: none">
    <!-- <input id="uploadFile" type="file" @change="requestUploadFile" /> -->
    <v-dialog v-model="visibleDialog" max-width="560">
      <simple-dialog
        title="2D Setting"
        :single-button="false"
        ok-title="Set"
        @select="onSelect"
        @close="onCancel"
      >
        <v-row class="slider" >
          <div>
              <p>Sigma</p>
              <v-space></v-space>
              <v-slider
                v-model="t_value"
                class="ml-2"
                :min="sigma_min"
                :max="sigma_max"
                :readonly="sigma_max < 1"
                dense
                hide-details
                @end="changeSelectsByTimeline(timeList[t_value])"
              ></v-slider> 
          </div>
           
        </v-row>
        
      </simple-dialog>
    </v-dialog>
  </div>
</template>

<script>
// import { mapGetters } from "vuex";
import tiff from "tiff.js";
import atob from "atob";
import axios from 'axios';
import SimpleDialog from "../../../custom/SimpleDialog";

export default {
  name: "Open3DSettingDialog",

  components: { SimpleDialog },

  props: {
    value: {
      type: Boolean,
      default: false
    }
  },

  data: () => ({
    isDragging: false,
    newFile: null,
    imageData: null
  }),

  computed: {
    // sigma_max() {
    //   var rs = [];
    //   if (this.timeList.length != 0) { // 如果存在图片
    //     for (let idx in this.filesAtRowCol) {
    //       let f = this.filesAtRowCol[idx];
    //       if (f.metaData) {
    //         rs.push(f.metaData.timeline);
    //       }
    //     }
    //     var length = rs.length-1;
    //     console.log('当前t_value:',this.t_value);
    //     console.log("滑轮最大值:",String(length));
    //   }
    //   return length;
    // },
    // sigma_min() {
    //   return 0;
    // }
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

  created() {
    this.newResWatch = this.$store.watch(
      (state, getters) => getters["image/newRes"],
      res => {
        const filteredData = [];
        for (var key in res) {
          if (key == "file_0" && res[key]) {
            filteredData.push({
              filename: this.newFile.name,
              metadata: res[key]
            });
          }
          break;
        }

        if (filteredData.length > 0) {
          this.$store.dispatch("image/addData", filteredData);
        }

        this.newFile = null;
        this.imageData = null;
      }
    );
  },

  beforeDestroy() {
    this.newResWatch();
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

      const fileInput = this.$el.querySelector("#uploadFile");
      fileInput.files = e.dataTransfer.files;

      this.requestUploadFile();

      e.preventDefault();
    },
    requestUploadFile() {
      const fileInput = this.$el.querySelector("#uploadFile");

      if (fileInput.files && fileInput.files.length > 0) {
        this.newFile = fileInput.files[0];
        this.imageData = null;

        if (
          this.newFile &&
          this.newFile.type.startsWith("image/") &&
          this.newFile.size < 2 * 1024 * 1024
        ) {
          var self = this;
          const reader = new FileReader();
          reader.onload = function() {
            if (self.newFile.type.startsWith("image/tif")) {
              const buffer = self.base64ToArrayBuffer(
                reader.result.substring(23)
              );
              const tiff_data = new tiff({ buffer });
              self.imageData = tiff_data.toDataURL();
            } else {
              self.imageData = reader.result;
            }
          };
          reader.readAsDataURL(this.newFile);
        }
      }
    },

    onSelect() {
      this.visibleDialog = false;

      if (this.newFile) {
        var formData = new FormData();
        var baseURL="http://127.0.0.1:8000"
        formData.append("files", this.newFile);
        this.$store.dispatch("image/setNewFiles", formData); 
      }
    },

    onCancel() {
      if (this.newFile) this.newFile = null;
      if (this.imageData) this.imageData = null;

      this.visibleDialog = false;
    }
  }
};
</script>

<style scoped>
.slider {
  margin-left: 10%;
  margin-right: 10%;
  width: 90%;
  padding-top: 5px;
  padding-bottom: 5px;
}
.isDragging {
  background-color: #e0f2f1;
  border-color: #fff;
}
#uploadFile {
  display: none;
}
</style>
