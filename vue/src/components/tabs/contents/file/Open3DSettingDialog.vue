<template>
  <div style="display: none">
    <!-- <input id="uploadFile" type="file" @change="requestUploadFile" /> -->
    <v-dialog v-model="visibleDialog" max-width="560">
      <simple-dialog
        title="2D Setting"
        :single-button="false"
        ok-title="Set"
        @select="onSet"
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
    // isDragging: false,
    // newFile: null,
    // imageData: null
  }),

  computed: {
    visibleDialog: {
      get() {
        return this.value;
      },
      set(val) {
        this.$emit("input", val);
      }
    },
  },

  methods: {
    onSet() {
      this.visibleDialog = false;
    },

    onCancel() {
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
