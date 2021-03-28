<template>
  <v-container class="pa-0" style="width: 100%; height: 100%" fluid>
    <div
      id="openseadragon"
      class="drop"
      :class="getClasses"
      style="width: 100%; height: 100%"
      @dragover.prevent="dragOver"
      @dragleave.prevent="dragLeave"
      @drop.prevent="drop($event)"
    ></div>
  </v-container>
</template>

<script>
/* eslint-disable no-unused-vars */
import OpenSeadragon from "openseadragon";
import config from "../../vue.config";
var path = require("path");

export default {
  name: "ImageViewer",

  components: {},

  data: () => ({
    isDragging: false,
    imageView: null,
    imageSource: null,
    publicPath: path.join("../", config.publicPath),
  }),

  created() {
    this.imageDataWatch = this.$store.watch(
      (state, getters) => getters["image/metaData"],
      (data) => {
        if (this.imageView && data) {
          const opt = {
            tileSource: {
              type: "image",
              url: data,
            },
          };

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
      prefixUrl: `${this.publicPath}/openseadragon/images/`,
      visibilityRatio: 1.0,
      constrainDuringPan: true,
      defaultZoomLevel: 1,
      minZoomLevel: 0.1,
      maxZoomLevel: 10,
      minZoomPixelRatio: 0.1,
      maxZoomPixelRatio: 10,
    });
  },

  computed: {
    getClasses() {
      return { isDragging: this.isDragging };
    },
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
    },
  },
};
</script>

<style scoped>
.isDragging {
  background-color: #999;
  border-color: #fff;
}
</style>
