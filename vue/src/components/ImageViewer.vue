<template>
  <v-container class="pa-0" style="width: 100%; height: 100%;" fluid>
    <div id="scroll" style="height:100%; overflow:auto; display:block;" @scroll="viewImage()">
        <div class="previewBlock" style='height:0px;' id="scrollinterDiv">
          <img src="" id="image_div" style="position:fixed; width:65%; height:85%; margin-top: 30px;z-index:1;display:block;border:black solid 1px;" ref="song" />
        </div>
    </div>
  </v-container>
</template>
<script>
import OpenSeadragon from "openseadragon";
import { createNamespacedHelpers } from "vuex";
const positionModule = createNamespacedHelpers("files/position");
var path = require("path");

let slice_no = 0;
let response_var;
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
  beforeDestroy() {
    this.imageDataWatch();
  },

  created() {
    this.unwatch = this.$store.watch(
      (state, getters) => getters["files/position/getchangedz"],
      newValue => {
        slice_no = newValue - 1;
        document.getElementById('image_div').src = 'http://localhost:8000/static/' + response_var.data.path_images[slice_no]; 
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

  methods: {
    // a function to view images
    viewImage() {
        var scrollDiv =  document.getElementById('scroll');
        var scrollinterDiv =  document.getElementById('scrollinterDiv');
        var scrollinterdivheight = parseInt(scrollinterDiv.style.height.replace('px',''));
        var scrollpercent = scrollDiv.scrollTop / scrollinterdivheight;
        slice_no = scrollpercent * response_var.data.N_images;
        slice_no = Math.round(slice_no);
        this.$store.dispatch("files/position/changeSelectsByZ", slice_no);
        document.getElementById('image_div').src = 'http://localhost:8000/static/' + response_var.data.path_images[slice_no]; 
    },
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
  },
  watch: {
    "$store.state.image.imageUri"(nv) {
        process_response(nv);
    },
  }
};
function process_response(response)
{
    response_var = response;
    if (response.data.path_images.length==1) {
      document.getElementById('scroll').style.overflow = 'hidden';
      document.getElementById('image_div').src = 'http://localhost:8000/static/'+response.data.path_images[0]; /////////////////////////////
      document.getElementById('scrollinterDiv').style.height = (response.data.N_images * 500)+'px';        
    }
    else {
      document.getElementById('scroll').style.overflow = 'auto';
      document.getElementById('image_div').src = 'http://localhost:8000/static/' + response.data.path_images[slice_no]; /////////////////////////////
      document.getElementById('scrollinterDiv').style.height = (response.data.N_images * 500)+'px';
    }
}
</script>

<style scoped>
.isDragging {
  border-color: #fff;
}
</style>
