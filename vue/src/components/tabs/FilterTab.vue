<template>
  <tab-item title="Filter" :buttons="true" @refresh="refresh" @help="help">
    <Filters />
    <v-divider class="my-2"></v-divider>
    <AddSub />
    <v-divider class="my-2"></v-divider>
    <Dec2D />
    <v-divider class="my-2"></v-divider>
    <Dec3D />
    <v-divider class="my-2"></v-divider>
    <FocusStack />
    <!-- <v-divider class="my-2"></v-divider>
    <DPC /> -->
  </tab-item>
</template>

<script>
import TabItem from "../custom/TabItem.vue";
import Filters from "./contents/filter/Filters";
import AddSub from "./contents/filter/AddSub";
import Dec2D from "./contents/filter/Dec2D";
import Dec3D from "./contents/filter/Dec3D";
import FocusStack from "./contents/filter/FocusStack";
// import DPC from "./contents/filter/DPC";

export default {
  name: "FilterTab",

  components: {
    TabItem,
    Filters,
    AddSub,
    Dec2D,
    Dec3D,
    FocusStack,
    // DPC
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
