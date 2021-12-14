<template>
  <tab-item
    title="Adjust"
    :buttons="true"
    @refresh="refresh"
    @help="help"
  >
    <BitConversion />
    <v-divider class="my-1" />
    <MergeSplit />
    <v-divider class="my-1" />
    <LightSet />
    <!-- <v-divider class="my-1"></v-divider>
    <Binarization /> -->
    <v-divider class="my-1" />
    <Scale />
    <v-divider class="my-1" />
    <FVO />
  </tab-item>
</template>

<script lang="ts">
import Component from 'vue-class-component';
import Vue from 'vue';

import TabItem from '@/components/custom/TabItem.vue';
import BitConversion from '@/components/tabs/contents/adjust/BitConversion.vue';
import MergeSplit from '@/components/tabs/contents/adjust/MergeSplit.vue';
import LightSet from '@/components/tabs/contents/adjust/LightSet.vue';
// import Binarization from "./contents/adjust/Binarization";
import Scale from '@/components/tabs/contents/adjust/Scale.vue';
import FVO from '@/components/tabs/contents/adjust/FVO.vue';

@Component({
  components: {
    TabItem,
    BitConversion,
    MergeSplit,
    LightSet,
    // Binarization,
    Scale,
    FVO
  }
})
export default class AdjustTab extends Vue {

  refresh(): void {
    console.log('Refresh');
  }

  help(): void {
    console.log('Help');
  }
}
</script>
