<template>
  <tab-item title="View">
    <v-row justify="center">
      <v-container class="max-width pagenation">
        <v-pagination
          v-model="curPageIdx"
          class="my-4 pagenation"
          total-visible="5"
          :length="allData.length"
          @input="handlePageChange"
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
import { mapGetters, mapState } from "vuex";

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
    Timeline,
  },

  data: () => ({
    totalPageCnt: 0,
    curPageIdx: 0,
  }),

  created() {
    this.curPageIdxWatch = this.$store.watch(
      (state, getters) => getters["image/currentPageIndex"],
      (res) => {
        this.curPageIdx = res;
      }
    );
  },

  beforeDestroy() {
    this.curPageIdxWatch();
  },

  computed: {
    ...mapGetters("image", {
      seriesCount: "seriesCount",
      sizeZ: "sizeZ",
      sizeT: "sizeT",
    }),
    ...mapState({
      allData: (state) => state.image.allData,
    }),
  },

  methods: {
    handlePageChange(idx) {
      this.$store.dispatch("image/changeCurrentPage", idx);
    },
  },
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
