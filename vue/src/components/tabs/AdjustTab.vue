<template>
  <tab-item title="Adjust" :buttons="true" @refresh="refresh" @help="help">
    <BitConversion />
    <v-divider class="my-1"></v-divider>
    <MergeSplit />
    <v-divider class="my-1"></v-divider>
    <LightSet />
    <!-- <v-divider class="my-1"></v-divider>
    <Binarization /> -->
    <v-divider class="my-1"></v-divider>
    <Scale />
    <v-divider class="my-1"></v-divider>
    <FVO />
  </tab-item>
</template>

<script>
import TabItem from "../custom/TabItem.vue";
import BitConversion from "./contents/adjust/BitConversion";
import MergeSplit from "./contents/adjust/MergeSplit";
import LightSet from "./contents/adjust/LightSet";
// import Binarization from "./contents/adjust/Binarization";
import Scale from "./contents/adjust/Scale";
import FVO from "./contents/adjust/FVO";

export default {
  name: "AdjustTab",

  components: {
    TabItem,
    BitConversion,
    MergeSplit,
    LightSet,
    // Binarization,
    Scale,
    FVO,
  },

  data: () => ({}),

  methods: {
    refresh: function () {
      console.log("Refresh");
    },
    help: function () {
      console.log("Help");
    },
  },
};
</script>
