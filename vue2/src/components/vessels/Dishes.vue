<template>
  <div class="d-flex justify-center px-3 my-1">
    <v-sheet
      class="dish-box"
      :width="rect.width"
      :height="rect.height"
    >
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
      />
    </v-sheet>
  </div>
</template>

<script lang="ts">
import Component from 'vue-class-component';
import Vue from 'vue';
import {VESSEL_DISH_GAP, VESSEL_DISH_MAX_HEIGHT, VESSEL_DISH_MAX_SIZE, VESSEL_DISH_RATIO} from '@/utils/constants';
import {Watch} from 'vue-property-decorator';



const DishProps = Vue.extend({
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
  }
})

@Component({})
export default class Dish extends DishProps {

  rect = {
    width: 0,
    height: 0
  }

  radius = 0;
  selectedDish = this.selected;
  activeDish = this.active;

  resize() {
    if (this.width * VESSEL_DISH_RATIO > VESSEL_DISH_MAX_HEIGHT) {
      this.rect.height = VESSEL_DISH_MAX_HEIGHT;
      this.rect.width = this.rect.height / VESSEL_DISH_RATIO;
    } else {
      this.rect.width = this.width;
      this.rect.height = this.width * VESSEL_DISH_RATIO;
    }

    const maxRadius = this.rect.height - VESSEL_DISH_GAP;

    this.radius =
        this.size > VESSEL_DISH_MAX_SIZE
            ? maxRadius
            : Math.abs(Math.ceil(this.size * maxRadius) / VESSEL_DISH_MAX_SIZE);
  }

  clicked() {
    if (!this.interaction) return;

    if (this.check) {
      if (this.activeDish) {
        this.selectedDish = !this.selectedDish;
        this.$emit('click');
      }
    } else {
      this.selectedDish = !this.selectedDish;
      this.$emit('click');
    }
  }


  // watch: {
  //   size: {
  //     handler() {
  //       this.resize();
  //       this.selectedDish = false;
  //     },
  //     deep: true,
  //     immediate: true
  //   },
  //   width: {
  //     handler() {
  //       this.resize();
  //     },
  //     deep: true,
  //     immediate: true
  //   }
  // },


}
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
