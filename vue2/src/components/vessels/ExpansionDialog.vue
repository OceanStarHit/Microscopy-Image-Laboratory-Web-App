<template>
  <v-dialog
    v-model="isShowProp"
    :max-width="width"
    :max-height="width"
  >
    <simple-dialog title="Vessel Expansion" @select="visibleDialog = false">
      <div class="pa-4">
        <slide
          v-if="currentVessel.type === 'Slide'"
          :width="width"
          :count="currentVessel.count"
          :show-number="true"
        />
        <well-plate
          v-if="currentVessel.type === 'WellPlate'"
          :width="width"
          :rows="currentVessel.rows"
          :cols="currentVessel.cols"
          :show-number="true"
        />
        <dish
          v-if="currentVessel.type === 'Dish'"
          :width="width"
          :size="currentVessel.size"
        />
        <wafer
          v-if="currentVessel.type === 'Wafer'"
          :width="width"
          :size="currentVessel.size"
        />
      </div>
    </simple-dialog>
  </v-dialog>
</template>

<script lang="ts">
import Component from 'vue-class-component';
import Vue from 'vue';

import {VESSELS, getVesselById, VesselBaseModel} from '@/utils/vessel-types';

import SimpleDialog from '../custom/SimpleDialog.vue';
import Slide from './Slides.vue';
import Dish from './Dishes.vue';
import WellPlate from './WellPlates.vue';
import Wafer from './Wafers.vue';

const ExpansionDialogProps = Vue.extend({
  props: {
    isShow: {
      type: Boolean,
      default: false
    }
  }
})

@Component({
  components: {
    SimpleDialog,
    Slide,
    Dish,
    Wafer,
    WellPlate
  }
})
export default class ExpansionDialog extends ExpansionDialogProps {
  width = 800;

  get currentVessel(): VesselBaseModel | null {
    return this.$store.getters['vessel/currentVessel'];
  }

  get isShowProp(): boolean {
    return this.isShow
  }

  set isShowProp(val: boolean) {
    this.$emit('input', val);
  }

  onSelectVessel(vesselTypeIndex: number, vesselIndex: number) {
    const vessel= VESSELS[vesselTypeIndex - 1][vesselIndex - 1];
    if (this.currentVessel && this.currentVessel.id !== vessel.id) {
      this.$store.dispatch('vessel/selectVessel', vessel.id);
    }
  }
}
</script>

<style scoped>
.active {
  border: 2px solid #4db6ac !important;
}
</style>
