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
const RATIO = 0.5;
const MAX_HEIGHT = 1000;
const GAP = 10;
const MAX_SIZE = 300;

export default {
  name: "Wafer",

  components: {},

  props: {
    size: {
      type: Number,
      default: 1,
    },
    width: {
      type: Number,
      default: 0,
    },
    active: {
      type: Boolean,
      default: false,
    },
    selected: {
      type: Boolean,
      default: false,
    },
    check: {
      type: Boolean,
      default: false,
    },
    interaction: {
      type: Boolean,
      default: true,
    },
  },

  data: function () {
    return {
      rect: {
        width: 0,
        height: 0,
      },
      radius: 0,
      selectedWafer: this.selected,
      activeWafer: this.active,
    };
  },

  watch: {
    size: {
      handler() {
        this.resize();
        this.selectedWafer = false;
      },
      deep: true,
      immediate: true,
    },
    width: {
      handler() {
        this.resize();
      },
      deep: true,
      immediate: true,
    },
  },

  methods: {
    resize: function () {
      if (this.width * RATIO > MAX_HEIGHT) {
        this.rect.height = MAX_HEIGHT;
        this.rect.width = this.height / RATIO;
      } else {
        this.rect.width = this.width;
        this.rect.height = this.width * RATIO;
      }

      const max_radius = this.rect.height - GAP;

      this.radius =
        this.size > MAX_SIZE
          ? max_radius
          : Math.abs(Math.ceil(this.size * max_radius) / MAX_SIZE);
    },

    clicked: function () {
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
    },
  },
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
