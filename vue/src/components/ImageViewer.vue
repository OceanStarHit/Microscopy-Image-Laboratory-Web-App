<template>
  <v-container class="pa-0" style="width: 100%; height: 100%;" fluid>
    <div
      id="openseadragon"
      class="drop"
      :class="getClasses"
      style="width: 100%; height: 100%;"
      @dragover.prevent="dragOver"
      @dragleave.prevent="dragLeave"
      @drop.prevent="drop($event)"
    ></div>
  </v-container>
</template>

<script>
/* eslint-disable no-unused-vars */
import OpenSeadragon from "openseadragon";

export default {
  name: "ImageViewer",

  components: {},

  data: () => ({
    isDragging: false,
    imageView: null,
    imageSource: null,
    publicPath: process.env.VUE_APP_STATIC_URL
      ? process.env.VUE_APP_STATIC_URL
      : "/"
  }),
  created() {
    this.unwatch = this.$store.watch(
      (state, getters) => getters["image/imageData"],
      newValue => {
        if (this.imageView && newValue.url) {
          const opt = {
            tileSource: {
              type: "image",
              url: newValue.url
            }
          };

          if (!newValue.isNew) {
            opt.index = 0;
            opt.replace = true;
          } else {
            this.imageView.world.removeAll();
          }

          this.imageView.addTiledImage(opt);
        }
      }
    );
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

  computed: {
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
      let files = e.dataTransfer.files;
      this.imageSource = files[0];

      this.isDragging = false;
    },

    onRequestUploadFiles() {}
  },

  beforeDestroy() {
    this.unwatch();
  }
};
</script>

<style scoped>
.isDragging {
  background-color: #999;
  border-color: #fff;
}
</style>
