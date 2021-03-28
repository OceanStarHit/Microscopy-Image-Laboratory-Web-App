<template>
  <v-dialog v-model="visibleDialog" :max-width="width" :max-height="width">
    <simple-dialog title="Vessel Expansion" @select="visibleDialog = false">
      <div class="pa-4">
        <slide
          v-if="currentVessel.type == 'Slide'"
          :width="width"
          :count="currentVessel.count"
          :showNumber="true"
        ></slide>
        <well-plate
          v-if="currentVessel.type == 'WellPlate'"
          :width="width"
          :rows="currentVessel.rows"
          :cols="currentVessel.cols"
          :showNumber="true"
        ></well-plate>
        <dish
          v-if="currentVessel.type == 'Dish'"
          :width="width"
          :size="currentVessel.size"
        ></dish>
        <wafer
          v-if="currentVessel.type == 'Wafer'"
          :width="width"
          :size="currentVessel.size"
        ></wafer>
      </div>
    </simple-dialog>
  </v-dialog>
</template>

<script>
import { mapGetters } from "vuex";

import { VESSELS, getVesselById } from "../../utils/vessel-types";

import SimpleDialog from "../custom/SimpleDialog";
import Slide from "./Slides";
import Dish from "./Dishes.vue";
import WellPlate from "./WellPlates";
import Wafer from "./Wafers";

export default {
  name: "ExpansionDialog",

  components: {
    SimpleDialog,
    Slide,
    Dish,
    Wafer,
    WellPlate,
  },

  data: () => ({
    vessels: VESSELS,
    width: 800,
  }),

  props: {
    value: {
      type: Boolean,
      default: false,
    },
  },

  computed: {
    ...mapGetters("vessel", {
      currentVesselId: "currentVesselId",
    }),
    currentVessel() {
      return getVesselById(this.currentVesselId);
    },
    visibleDialog: {
      get() {
        return this.value;
      },
      set(val) {
        this.$emit("input", val);
      },
    },
  },

  methods: {
    onSelectVessel: function (v_idx, idx) {
      const vesselId = this.vessels[v_idx - 1][idx - 1].id;
      if (this.currentVesselId !== vesselId) {
        this.$store.dispatch("vessel/selectVessel", vesselId);
      }
    },
  },
};
</script>

<style scoped>
.active {
  border: 2px solid #4db6ac !important;
}
</style>
