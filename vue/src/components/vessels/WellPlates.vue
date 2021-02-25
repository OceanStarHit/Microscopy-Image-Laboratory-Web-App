<template>
  <div class="d-flex justify-center px-3 my-1">
    <v-sheet class="plate-box" :width="rect.width" :height="rect.height">
      <v-row
        v-if="showName"
        class="d-inline-flex  align-center justify-space-around pa-0 ma-0"
        style="overflow: hidden;"
      >
        <div
          v-for="c in showName ? cols + 1 : cols"
          :key="c"
          class="text-center"
          :style="{ 'font-size': fontSize + 'px', width: radius + 'px' }"
        >
          {{ showName ? (c > 1 ? c - 1 : "") : c }}
        </div>
      </v-row>
      <v-row
        v-for="r in rows"
        :key="r"
        class="align-center justify-space-around pa-0 ma-0"
      >
        <div
          v-if="showName"
          class="pa-0 ma-0 text-center"
          :style="{ 'font-size': fontSize + 'px', width: radius + 'px' }"
        >
          {{ String.fromCharCode(64 + r) }}
        </div>
        <v-sheet
          v-for="c in cols"
          :key="c"
          class="rounded-circle hole"
          :class="checkActive(r, c)"
          :width="radius"
          :height="radius"
          :ripple="interaction"
          @click="clicked(r, c)"
        >
          <div
            v-if="showNumber"
            class="primary--text"
            :style="{ 'font-size': fontSize - 1 + 'px' }"
          >
            {{ holeNumber(r, c) }}
          </div>
        </v-sheet>
      </v-row>
    </v-sheet>
  </div>
</template>

<script>
const RATIO = 0.6;
const MAX_HEIGHT = 1000;
const MAX_FONTSIZE = 14;

export default {
  name: "WellPlate",

  components: {},

  props: {
    width: {
      type: Number,
      default: 0
    },
    showName: {
      type: Boolean,
      default: true
    },
    showNumber: {
      type: Boolean,
      default: false
    },
    rows: {
      type: Number,
      default: 1
    },
    cols: {
      type: Number,
      default: 1
    },
    actives: {
      type: Array,
      default: () => []
    },
    selected: {
      type: Number,
      default: -1
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
      fontSize: 5,
      selectedHole: this.selected,
      activeHoles: this.actives
    };
  },

  computed: {
    size() {
      const { rows, cols } = this;
      return {
        rows,
        cols
      };
    },
    checkActive() {
      return (row, col) => {
        const index = (row - 1) * this.cols + col - 1;
        return this.check
          ? this.activeHoles.indexOf(index) > -1
            ? this.selectedHole === index
              ? "selected"
              : "active"
            : ""
          : this.selectedHole === index
          ? "selected"
          : "";
      };
    },
    holeNumber() {
      return (row, col) => {
        return (row - 1) * this.cols + col;
      };
    }
  },

  watch: {
    size: {
      handler() {
        this.resize();
        this.selectedHole = -1;
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
      if (this.width * RATIO > MAX_HEIGHT) {
        this.rect.height = MAX_HEIGHT;
        this.rect.width = this.rect.height / RATIO;
      } else {
        this.rect.width = this.width;
        this.rect.height = this.width * RATIO;
      }

      const a_rows = this.rows + (this.showName ? 1 : 0);
      const a_cols = this.cols + (this.showName ? 1 : 0);
      let radius =
        this.rect.width / a_cols > this.rect.height / a_rows
          ? this.rect.height / a_rows
          : this.rect.width / a_cols;
      this.radius = Math.floor(Math.floor(radius) * 0.9);

      this.fontSize = radius / 2 > MAX_FONTSIZE ? MAX_FONTSIZE : radius / 2;
    },

    clicked: function(row, col) {
      if (!this.interaction) return;

      const index = (row - 1) * this.cols + col - 1;

      if (this.check) {
        const pos = this.activeHoles.indexOf(index);
        if (pos > -1) {
          this.selectedHole = this.selectedHole !== index ? index : -1;
          this.$emit("click", { row, col });
        }
      } else {
        this.selectedHole = this.selectedHole !== index ? index : -1;
        this.$emit("click", { row, col });
      }
    }
  }
};
</script>

<style scoped>
.plate-box {
  width: 100%;
  border: 1px solid black !important;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
.hole {
  width: 100%;
  border: 1px solid black !important;
  display: flex;
  align-items: center;
  justify-content: center;
}
.hole.active {
  background-color: cyan !important;
}
.hole.selected {
  background-color: magenta !important;
}
</style>
