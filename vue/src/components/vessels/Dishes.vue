<template>
  <div class="d-flex justify-center px-3 my-1">
    <v-sheet class="dish-box" :width="rect.width" :height="rect.height">
      <v-sheet
        class="rounded-circle dish-box"
        :class="
          check
            ? activeDish
              ? selectedDish
                ? 'selected'
                : 'active'
              : ''
            : selectedDish
            ? 'selected'
            : ''
        "
        :width="radius"
        :height="radius"
        :ripple="interaction"
        @click="clicked"
      >
      </v-sheet>
    </v-sheet>
  </div>
</template>

<script>
import {
  VESSEL_DISH_RATIO,
  VESSEL_DISH_MAX_HEIGHT,
  VESSEL_DISH_GAP,
  VESSEL_DISH_MAX_SIZE
} from "../../utils/constants";

export default {
  name: "Dish",

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
    },
    requsetRender: {
      type: Boolean,
      default: false
    }
  },

  data: function() {
    return {
      rect: {
        width: 0,
        height: 0
      },
      radius: 0,
      selectedDish: this.selected,
      activeDish: this.active
    };
  },

  watch: {
    size: {
      handler() {
        this.resize();
        this.selectedDish = false;
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
      if (this.width * VESSEL_DISH_RATIO > VESSEL_DISH_MAX_HEIGHT) {
        this.rect.height = VESSEL_DISH_MAX_HEIGHT;
        this.rect.width = this.rect.height / VESSEL_DISH_RATIO;
      } else {
        this.rect.width = this.width;
        this.rect.height = this.width * VESSEL_DISH_RATIO;
      }

      const max_radius = this.rect.height - VESSEL_DISH_GAP;

      this.radius =
        this.size > VESSEL_DISH_MAX_SIZE
          ? max_radius
          : Math.abs(Math.ceil(this.size * max_radius) / VESSEL_DISH_MAX_SIZE);
    },

    clicked: function() {
      if (!this.interaction) return;

      if (this.check) {
        if (this.activeDish) {
          this.selectedDish = !this.selectedDish;
          this.$emit("click");
        }
      } else {
        this.selectedDish = !this.selectedDish;
        this.$emit("click");
      }
    }
  }
};
</script>

<style scoped>
.dish-box {
  position: relative;
  width: 100%;
  border: 2px solid black !important;
  display: flex;
  align-items: center;
  justify-content: center;
}
.dish-box.active {
  background-color: cyan !important;
}
.dish-box.selected {
  background-color: magenta !important;
}
</style>
