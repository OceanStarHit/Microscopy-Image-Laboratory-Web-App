<template>
  <v-card
    ref="frame"
    v-resize="onResize"
    class="pa-1"
    flat
  > 
    <v-row class="px-5 py-0 my-1">
      <h5>{{ vesselTitle }}</h5>
    </v-row>
    <slide
      v-if="currentVessel.type === 'Slide'"
      :width="widthProp"
      :count="currentVessel.count"
    />
    <well-plate
      v-if="currentVessel.type === 'WellPlate'"
      :width="widthProp"
      :rows="currentVessel.rows"
      :cols="currentVessel.cols"
    />
    <dish
      v-if="currentVessel.type === 'Dish'"
      :width="widthProp"
      :size="currentVessel.size"
    />
    <wafer
      v-if="currentVessel.type === 'Wafer'"
      :width="widthProp"
      :size="currentVessel.size"
    />
    <v-card-actions>
      <v-row
        class="mt-1"
        justify="space-around"
        style="border-top: 1px solid #f2f2f2"
      >
        <CustomButton icon="swap-horizontal" @click="selectDialog = true" />
        <CustomButton icon="focus-field" @click="expansionDialog = true" />
        <vessel-select-dialog v-model="selectDialog" />
        <vessel-expansion-dialog v-model="expansionDialog" />
      </v-row>
    </v-card-actions>
  </v-card>
</template>

<script lang="ts">
import Component from 'vue-class-component';
import Vue from 'vue';

import { VESSELS } from '@/utils/vessel_types';

import CustomButton from '../../../custom/CustomButton.vue';
import Dish from '../../../vessels/Dishes.vue';
import Slide from '../../../vessels/Slides.vue';
import Wafer from '../../../vessels/Wafers.vue';
import WellPlate from '../../../vessels/WellPlates.vue';
import VesselSelectDialog from '../../../vessels/SelectDialog.vue';
import VesselExpansionDialog from '../../../vessels/ExpansionDialog.vue';
import {VesselBaseModel} from '@/store/vessel.module';

const VesselProps = Vue.extend({
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

@Component({
  components: {
    CustomButton,
    VesselSelectDialog,
    VesselExpansionDialog,
    Slide,
    Dish,
    Wafer,
    WellPlate
  },
})
export default class Vessel extends VesselProps {

  selectDialog= false;
  expansionDialog= false;
  vessels= VESSELS


  get currentVessel(): VesselBaseModel | null {
    return this.$store.getters['vessel/currentVessel'];
  }

  get vesselTitle(): string {
    const vessel = this.currentVessel;
    if (vessel) {
      return `${vessel.title} - ${vessel.type}`;
    }
    return '';
  }

  mounted() {
    // eslint-disable-next-line @typescript-eslint/no-this-alias
    const that = this;
    const hd = setInterval(function(){
      that.width = that.widthProp;
      if (that.width != 0) {
        clearInterval(hd);
      }
    },100);
    // this.$nextTick(function() {
    //   this.width = this.getWidth();
    // });
  }

  get widthProp(): number {
    if (this.$refs && this.$refs.frame) {
      const frame: Vue = this.$refs.frame as Vue;
      const frameSize = frame.$el.getBoundingClientRect();
      const width = Math.trunc(frameSize.width);
      return width;
    }
    return 0;
  }


  onResize() {
    this.width = this.widthProp;
  }

  select2() {
    console.log('Select-2');
  }

  select3() {
    console.log('Select-3');
  }

}
</script>
