<template>
  <div style="display: none">
    <v-dialog v-model="visibleDialog" max-width="560">
      <simple-dialog
        title="Setting"
        :single-button="false"
        ok-title="Set"
        @select="onSet"
        @close="onCancel"
      >
        <v-row class="slider">
          <p>Sigma</p>
          <v-space></v-space>
          <v-slider
            v-model="t_value"
            class="ml-2"
            :min="t_min"
            :max="t_max"
            :readonly="t_max < 1"
            dense
            hide-details
          ></v-slider>
        </v-row>
      </simple-dialog>
    </v-dialog>
  </div>
</template>

<script>
import SimpleDialog from "../../../custom/SimpleDialog";

export default {
  name: "Open2DSettingDialog",

  components: { SimpleDialog },

  props: {
    value: {
      type: Boolean,
      default: false
    }
  },

  data: () => ({
    t_min: 0,
    t_max: 100
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
    }
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
  margin-top: 5px;
  margin-bottom: 5px;
}
.isDragging {
  background-color: #e0f2f1;
  border-color: #fff;
}
#uploadFile {
  display: none;
}
</style>
