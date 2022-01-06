<template>
  <v-container class="pa-0" style="width: 100%; height: 100%" fluid>
    

    <!-- <div id="slideno" style="display:none; position:absolute;"> </div>
    <div style="position:absolute;margin-top:30px;"><img src="" id="image_loading" /></div>
    <div id="scroll" style="height:500px; overflow:auto; display:block;" @scroll="viewImage()">
        <div class="previewBlock" style='height:0px;' id="scrollinterDiv">
            <img src="" id="image_div" style="position:fixed; width:600px; height:485px; z-index:-1;display:block;border:black solid 1px;" ref="song" />
        </div>
    </div> -->


    <div style="width: 100%; height: 100%">
      <img v-bind:src="imageUri" style="width:100%;height:100%;">
    </div>
    <p>{{ demoPic ? demoPic.name : "No pic" }}</p>
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
    },
    imageUri() {
      var src_path = this.$store.state.image.imageUri;
      var image_path = "http://localhost:8000/static/" + src_path[0];
      // process_response(src_path);
      return image_path;
    }
  },
  // created() {
  //   this.imageDataWatch = this.$store.watch(
  //     (state, getters) => getters["files/position/getFilesAtSelection"],
  //     data => {
  //       if (this.imageView && this.demoPic) {
  //         const opt = {
  //           tileSource: {
  //             type: "image",
  //             url: this.demoPic.imageData.src
  //           }
  //         };

  //         console.log("Show pic: " + this.demoPic.name);
  //         this.imageView.world.removeAll();
  //         this.imageView.addTiledImage(opt);
  //       }
  //     });

  // },

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
    // a function to view images
    viewImage() {
        var scrollDiv =  document.getElementById('scroll');
        var scrollinterDiv =  document.getElementById('scrollinterDiv');
        var scrollinterdivheight = parseInt(scrollinterDiv.style.height.replace('px',''));
        var scrollpercent = scrollDiv.scrollTop / scrollinterdivheight;
        slice_no = scrollpercent * response_var.data.N_images;
        slice_no = Math.round(slice_no);
        document.getElementById('slideno').style.display = 'block';
        document.getElementById('slideno').innerHTML =  'Slice ' + (slice_no+1).toString() + ' / ' + response_var.data.N_images.toString();
        document.getElementById('image_div').src = 'http://localhost:8000/static/' + response_var.data.path_images[slice_no]; 
    },
    process_response()
    {
      response_var = this.$store.state.image.imageUri;
      var response = response_var
      document.getElementById('image_loading').src = '';
      // document.getElementById('image_div').style.display = 'block';
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
  }
};
// function process_response(response)
// {
//     response_var = response;
//     console.log("Here is process_response function!!!");

//     document.getElementById('image_loading').src = '';
//     // document.getElementById('image_div').style.display = 'block';
//     if (response.data.path_images.length==1) {
//         document.getElementById('scroll').style.overflow = 'hidden';
//         document.getElementById('image_div').src = 'http://localhost:8000/static/'+response.data.path_images[0]; /////////////////////////////
//         document.getElementById('scrollinterDiv').style.height = (response.data.N_images * 500)+'px';
        
//     }
//     else {
//         console.log(response); 
//         document.getElementById('scroll').style.overflow = 'auto';
//         document.getElementById('image_div').src = 'http://localhost:8000/static/' + response.data.path_images[slice_no]; /////////////////////////////
//         document.getElementById('scrollinterDiv').style.height = (response.data.N_images * 500)+'px';
//         console.log(document.getElementById('image_div').src);

//     }
// }
</script>

<style scoped>
.isDragging {
  background-color: #999;
  border-color: #fff;
}
</style>
