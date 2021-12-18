<template>
  <v-dialog v-model="isShowProp" max-width="980">
    <simple-dialog title="Vessel Select" @select="isShowProp = false">
      <v-tabs v-model="selectedTab" fixed-tabs>
        <v-tab
          v-for="i in vesselTypes.length"
          :key="i"
          :href="`#tabs-${i}`"
          class="primary--text"
        >
          {{ vesselTypes[i - 1] }}
        </v-tab>
        <v-tab
          :href="`#tabs-${vesselTypes.length + 1}`"
          class="primary--text"
        >
          Custom
        </v-tab>
      </v-tabs>

      <v-tabs-items v-model="selectedTab">
        <v-tab-item
          v-for="v_idx in vessels.length"
          :key="v_idx"
          :value="`tabs-${v_idx}`"
        >
          <v-row class="d-flex align-center px-5" style="height: 220px">
            <v-btn
              v-for="i in vessels[v_idx - 1].length"
              :key="i"
              text
              class="pa-0 ma-0"
              :class="
                vessels[v_idx - 1][i - 1].id === currentVessel.id ? 'active' : ''
              "
              width="160"
              height="150"
              color="teal"
              @click="onSelectVessel(v_idx, i)"
            >
              <div v-if="v_idx === 1">
                <slide
                  :width="140"
                  :count="vessels[v_idx - 1][i - 1].count"
                  :interaction="false"
                />
                <div class="mt-3 text-center text-capitalize">
                  {{ vessels[v_idx - 1][i - 1].title }}
                </div>
              </div>
              <div v-if="v_idx === 2">
                <well-plate
                  :width="140"
                  :show-name="vessels[v_idx - 1][i - 1].showName"
                  :rows="vessels[v_idx - 1][i - 1].rows"
                  :cols="vessels[v_idx - 1][i - 1].cols"
                  :interaction="false"
                />
                <div class="mt-3 text-center text-capitalize">
                  {{ vessels[v_idx - 1][i - 1].title }}
                </div>
              </div>
              <div v-if="v_idx === 3">
                <dish
                  :width="140"
                  :size="vessels[v_idx - 1][i - 1].size"
                  :interaction="false"
                />
                <div class="mt-3 text-center text-capitalize">
                  {{ vessels[v_idx - 1][i - 1].title }}
                </div>
              </div>
              <div v-if="v_idx === 4">
                <wafer
                  :width="140"
                  :size="vessels[v_idx - 1][i - 1].size"
                  :interaction="false"
                />
                <div class="mt-3 text-center text-capitalize">
                  {{ vessels[v_idx - 1][i - 1].title }}
                </div>
              </div>
            </v-btn>
          </v-row>
        </v-tab-item>
        <v-tab-item :value="`tabs-${vesselTypes.length + 1}`">
          <v-row class="pa-5" style="height: 220px" />
        </v-tab-item>
      </v-tabs-items>
    </simple-dialog>
  </v-dialog>
</template>

<script lang="ts">
import Component from 'vue-class-component';
import Vue from 'vue';

import SimpleDialog from '../custom/SimpleDialog.vue';
import Slide from './Slides.vue';
import Dish from './Dishes.vue';
import WellPlate from './WellPlates.vue';
import Wafer from './Wafers.vue';
import {VESSEL_TYPES, VesselBaseModel, VESSELS} from '@/utils/vessel_types';

const SelectDialogProps = Vue.extend({
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
  },
})
export default class SelectDialog extends SelectDialogProps {
  selectedTab = null;

  vesselTypes = VESSEL_TYPES;
  vessels = VESSELS;

  get isShowProp(): boolean {
    return this.isShow
  }

  set isShowProp(val: boolean) {
    this.isShow = val;
    this.$emit('input', val);
  }

  get currentVessel(): VesselBaseModel | null {
    return this.$store.getters['vessel/currentVessel'];
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
