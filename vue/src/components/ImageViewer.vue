<template>
  <v-container class="pa-0" style="width: 100%; height: 100%" fluid>
    <img id="gambar" hidden/>
    <div
      id="openseadragon"
      class="drop"
      :class="getClasses"
      style="width: 100%; height: 100%"
      @dragover.prevent="dragOver"
      @dragleave.prevent="dragLeave"
      @drop.prevent="drop($event)"
    ></div>
    <p>{{ demoPic ? demoPic.name : "No pic" }}</p>
  </v-container>
</template>

<script>
import OpenSeadragon from "openseadragon";
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

          // console.log("Show pic: " + this.demoPic.imageData.src); 
          var gambar = document.getElementById("gambar");
          gambar.src = this.demoPic.imageData.src;
          this.imageView.world.removeAll();
          this.imageView.addTiledImage(opt);
          // console.log(opt);
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
    // this.imageView.addHandler('tile-loaded', function(event) {
    //     var image = document.getElementById("gambar");
    //     var canvas = document.createElement('canvas');
    //     var scale = 8;
    //     scale *= 0.01;

    //     canvas.width = image.width;
    //     canvas.height = image.height;

    //     var scaledW = canvas.width * scale;
    //     var scaledH = canvas.height * scale;

    //     event.tile.context2D = canvas.getContext('2d');
    //     event.tile.context2D.mozImageSmoothingEnabled = false;
    //     event.tile.context2D.webkitImageSmoothingEnabled = false;
    //     event.tile.context2D.imageSmoothingEnabled = false;

    //     event.tile.context2D.drawImage(img, 0, 0, scaledW, scaledH);
    //     event.tile.context2D.drawImage(canvas, 0, 0, scaledW, scaledH, 0, 0, event.image.width, event.image.height);
    // });

    // this.imageView = viewer;
    
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
