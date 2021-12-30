<template>
  <v-container class="pa-0" style="width: 100%; height: 100%" fluid>
    <div
      style="width: 100%; height: 100%"
    >
    <!-- <img v-bind:src="'data:image/png;base64,'+imageUri" style="width:100%;height:100%;"> -->
    <img src="http://localhost:8000/static/scan_Top%20Slide_D_p00_0_A01f322d4.JPG/static/scan_Top Slide_D_p00_0_A01f322d4.JPG" style="width:100%;height:100%;">
    </div>
    <p>{{ demoPic ? demoPic.name : "No pic" }}</p>
  </v-container>
</template>
<script>
/* eslint-disable no-unused-vars */
import OpenSeadragon from "openseadragon";
import config from "../../vue.config";
import { mapState, mapGetters, mapActions } from "vuex";
import { createNamespacedHelpers } from "vuex";
const positionModule = createNamespacedHelpers("files/position");
var path = require("path");

export default {
  name: "ImageViewer",

  components: {},

  data: () => ({
    isDragging: false,
    imageView: null,
    imageSource: null,
    publicPath:
      process.env.VUE_APP_STATIC_URL === undefined ||
      process.env.VUE_APP_STATIC_URL === null
        ? "../../"
        : process.env.VUE_APP_STATIC_URL
  }),

  computed: {
    ...positionModule.mapGetters({
      filesAtSelection: "getFilesAtSelection"
    }),
    demoPic: function() {
      if (this.filesAtSelection.length > 0) {
        return this.filesAtSelection[0];
      }
      return null;
    },
    getClasses() {
      return { isDragging: this.isDragging };
    },
    imageUri() {
      console.log("Here is imageUri function");
      var image_src = btoa(unescape(encodeURIComponent(this.$store.state.image.imageUri)));
      console.log(image_src);
      return image_src;
    }
  },

  created() {
    this.imageDataWatch = this.$store.watch(
      (state, getters) => getters["files/position/getFilesAtSelection"],
      data => {
        if (this.imageView && this.demoPic) {
          const opt = {
            tileSource: {
              type: "image",
              url: this.demoPic.imageData.src
            }
          };

          console.log("Show pic: " + this.demoPic.name);
          this.imageView.world.removeAll();
          this.imageView.addTiledImage(opt);
        }
      }
    );

  },
  beforeDestroy() {
    this.imageDataWatch();
  },

  mounted() {
    this.imageView = OpenSeadragon({
      id: "openseadragon",
      prefixUrl: `${this.publicPath}openseadragon/images/`,
      visibilityRatio: 1.0,
      constrainDuringPan: true,
      defaultZoomLevel: 1,
      minZoomLevel: 0.1,
      maxZoomLevel: 10,
      minZoomPixelRatio: 0.1,
      maxZoomPixelRatio: 10
    });
  },

  methods: {
    dragOver() {
      this.isDragging = true;
    },
    dragLeave() {
      this.isDragging = false;
    },
    drop(e) {
      let files = e.dataTransfer.files;
      this.imageSource = files[0];

      this.isDragging = false;
    }
  }
};
</script>

<style scoped>
.isDragging {
  background-color: #999;
  border-color: #fff;
}
</style>
