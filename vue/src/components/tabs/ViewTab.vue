<template>
  <tab-item title="View">
    <v-row justify="center">
      <v-container class="max-width pagenation">
        <v-pagination
          v-model="page"
          class="my-4 pagenation"
          total-visible="5"
          :length="1"
        ></v-pagination>
      </v-container>
    </v-row>
    <v-divider></v-divider>
    <Vessel />
    <v-divider></v-divider>
    <Objective />
    <v-divider></v-divider>
    <Channel />
    <v-divider></v-divider>
    <ImageAdjust />
    <!-- <div v-if="seriesCount > 1">
      <v-divider></v-divider>
      <ImageSeries />
    </div> -->
    <div v-if="sizeZ > 0">
      <v-divider></v-divider>
      <ZPosition />
    </div>
    <div v-if="sizeT > 0">
      <v-divider></v-divider>
      <Timeline />
    </div>
  </tab-item>
</template>

<script>
import { mapGetters } from "vuex";

import TabItem from "../custom/TabItem";
import Vessel from "./contents/viewcontrol/Vessel";
import Objective from "./contents/viewcontrol/Objective";
import Channel from "./contents/viewcontrol/Channel";
import ImageAdjust from "./contents/viewcontrol/ImageAdjust";
// import ImageSeries from "./contents/viewcontrol/ImageSeries";
import ZPosition from "./contents/viewcontrol/ZPosition";
import Timeline from "./contents/viewcontrol/Timeline";

export default {
  name: "ViewTab",

  components: {
    TabItem,
    Vessel,
    Objective,
    Channel,
    ImageAdjust,
    // ImageSeries,
    ZPosition,
    Timeline
  },

  data: () => ({
    page: 1
  }),

  computed: {
    ...mapGetters("image", {
      seriesCount: "seriesCount",
      sizeZ: "sizeZ",
      sizeT: "sizeT"
    })
  }
};
</script>

<style scoped>
.pagenation {
  padding: 0px !important;
}
.pagenation >>> button {
  width: 24px;
  height: 24px;
  min-width: 24px;
}
</style>
