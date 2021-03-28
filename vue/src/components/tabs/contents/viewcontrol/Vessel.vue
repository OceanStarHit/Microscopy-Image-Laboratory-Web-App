<template>
  <v-card ref="frame" class="pa-1" flat v-resize="onResize">
    <v-row class="px-5 py-0 my-1">
      <h5>{{ vesselTitle }}</h5>
    </v-row>
    <slide
      v-if="currentVessel.type === 'Slide'"
      :width="width"
      :count="currentVessel.count"
    ></slide>
    <well-plate
      v-if="currentVessel.type === 'WellPlate'"
      :width="width"
      :rows="currentVessel.rows"
      :cols="currentVessel.cols"
    ></well-plate>
    <dish
      v-if="currentVessel.type === 'Dish'"
      :width="width"
      :size="currentVessel.size"
    ></dish>
    <wafer
      v-if="currentVessel.type === 'Wafer'"
      :width="width"
      :size="currentVessel.size"
    ></wafer>
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

<script>
import { mapGetters } from "vuex";

import { VESSELS, getVesselById } from "../../../../utils/vessel-types";

import CustomButton from "../../../custom/CustomButton";
import Dish from "../../../vessels/Dishes.vue";
import Slide from "../../../vessels/Slides";
import Wafer from "../../../vessels/Wafers";
import WellPlate from "../../../vessels/WellPlates";
import VesselSelectDialog from "../../../vessels/SelectDialog";
import VesselExpansionDialog from "../../../vessels/ExpansionDialog";

export default {
  name: "Vessel",

  components: {
    CustomButton,
    VesselSelectDialog,
    VesselExpansionDialog,
    Slide,
    Dish,
    Wafer,
    WellPlate,
  },

  data: () => ({
    width: 0,
    selectDialog: false,
    expansionDialog: false,
    vessels: VESSELS,
  }),

  created() {
    this.currentPageDataWatch = this.$store.watch(
      (state, getters) => getters["image/currentPageInfo"],
      (info) => {
        this.$store.dispatch("vessel/setVesselId", info);
      }
    );
  },

  beforeDestroy() {
    this.currentPageDataWatch();
  },

  computed: {
    ...mapGetters("vessel", {
      currentVesselId: "currentVesselId",
      // activeHoles: "activeHoles",
      // activeHole: "activeHole"
    }),
    currentVessel() {
      return getVesselById(this.currentVesselId);
    },
    vesselTitle() {
      const vessel = this.currentVessel;
      return `${vessel.title} - ${vessel.type}`;
    },
  },

  mounted() {
    this.$nextTick(function () {
      this.width = this.getWidth();
    });
  },

  methods: {
    getWidth: function () {
      const frame = this.$refs.frame;
      const frameSize = frame.$el.getBoundingClientRect();
      const width = Math.trunc(frameSize.width);

      return width;
    },
    onResize: function () {
      this.width = this.getWidth();
    },
    select2: function () {
      console.log("Select-2");
    },
    select3: function () {
      console.log("Select-3");
    },
  },
};
</script>
