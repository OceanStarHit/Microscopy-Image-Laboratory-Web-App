<template>
  <div class="d-flex justify-center px-3 my-1">
    <v-sheet class="wafer-box" :width="rect.width" :height="rect.height">
      <v-sheet
        class="rounded-circle wafer-box"
        :class="
          check
            ? activeWafer
              ? selectedWafer
                ? 'selected'
                : 'active'
              : ''
            : selectedWafer
            ? 'selected'
            : ''
        "
        :width="radius"
        :height="radius"
        :ripple="interaction"
        @click="clicked"
      ></v-sheet>
    </v-sheet>
  </div>
</template>

<script>
import {
  VESSEL_WAFER_RATIO,
  VESSEL_WAFER_MAX_HEIGHT,
  VESSEL_WAFER_GAP,
  VESSEL_WAFER_MAX_SIZE
} from "../../utils/constants";

export default {
  name: "Wafer",

  components: {},

  props: {
    size: {
      type: Number,
      default: 1
    },
    width: {
      type: Number,
      default: 0
    },
    active: {
      type: Boolean,
      default: false
    },
    selected: {
      type: Boolean,
      default: false
    },
    check: {
      type: Boolean,
      default: false
    },
    interaction: {
      type: Boolean,
      default: true
    }
  },

  data: function() {
    return {
      rect: {
        width: 0,
        height: 0
      },
      radius: 0,
      selectedWafer: this.selected,
      activeWafer: this.active
    };
  },

  watch: {
    size: {
      handler() {
        this.resize();
        this.selectedWafer = false;
      },
      deep: true,
      immediate: true
    },
    width: {
      handler() {
        this.resize();
      },
      deep: true,
      immediate: true
    }
  },

  methods: {
    resize: function() {
      if (this.width * VESSEL_WAFER_RATIO > VESSEL_WAFER_MAX_HEIGHT) {
        this.rect.height = VESSEL_WAFER_MAX_HEIGHT;
        this.rect.width = this.height / VESSEL_WAFER_RATIO;
      } else {
        this.rect.width = this.width;
        this.rect.height = this.width * VESSEL_WAFER_RATIO;
      }

      const max_radius = this.rect.height - VESSEL_WAFER_GAP;

      this.radius =
        this.size > VESSEL_WAFER_MAX_SIZE
          ? max_radius
          : Math.abs(Math.ceil(this.size * max_radius) / VESSEL_WAFER_MAX_SIZE);
    },

    clicked: function() {
      if (!this.interaction) return;

      if (this.check) {
        if (this.activeWafer) {
          this.selectedWafer = !this.selectedWafer;
          this.$emit("click");
        }
      } else {
        this.selectedWafer = !this.selectedWafer;
        this.$emit("click");
      }
    }
  }
};
</script>

<style scoped>
.wafer-box {
  border: 2px solid black !important;
  display: flex;
  align-items: center;
  justify-content: center;
}
.wafer-box.active {
  background-color: cyan !important;
}
.wafer-box.selected {
  background-color: magenta !important;
}
</style>
