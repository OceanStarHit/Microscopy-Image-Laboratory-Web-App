<template>
  <v-dialog v-model="visibleDialog" max-width="980">
    <simple-dialog title="Vessel Select" @select="visibleDialog = false">
      <v-tabs v-model="selectedTab" fixed-tabs>
        <v-tab
          v-for="i in vesselTypes.length"
          :key="i"
          :href="`#tabs-${i}`"
          class="primary--text"
          >{{ vesselTypes[i - 1] }}</v-tab
        >
        <v-tab :href="`#tabs-${vesselTypes.length + 1}`" class="primary--text"
          >Custom</v-tab
        >
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
                vessels[v_idx - 1][i - 1].id === currentVesselId ? 'active' : ''
              "
              width="160"
              height="150"
              color="teal"
              @click="onSelectVessel(v_idx, i)"
            >
              <div v-if="v_idx == 1">
                <slide
                  :width="140"
                  :count="vessels[v_idx - 1][i - 1].count"
                  :interaction="false"
                />
                <div class="mt-3 text-center text-capitalize">
                  {{ vessels[v_idx - 1][i - 1].title }}
                </div>
              </div>
              <div v-if="v_idx == 2">
                <well-plate
                  :width="140"
                  :showName="vessels[v_idx - 1][i - 1].showName"
                  :rows="vessels[v_idx - 1][i - 1].rows"
                  :cols="vessels[v_idx - 1][i - 1].cols"
                  :interaction="false"
                />
                <div class="mt-3 text-center text-capitalize">
                  {{ vessels[v_idx - 1][i - 1].title }}
                </div>
              </div>
              <div v-if="v_idx == 3">
                <dish
                  :width="140"
                  :size="vessels[v_idx - 1][i - 1].size"
                  :interaction="false"
                />
                <div class="mt-3 text-center text-capitalize">
                  {{ vessels[v_idx - 1][i - 1].title }}
                </div>
              </div>
              <div v-if="v_idx == 4">
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
          <v-row class="pa-5" style="height: 220px"></v-row>
        </v-tab-item>
      </v-tabs-items>
    </simple-dialog>
  </v-dialog>
</template>

<script>
import { mapGetters } from "vuex";

import SimpleDialog from "../custom/SimpleDialog";
import Slide from "./Slides";
import Dish from "./Dishes.vue";
import WellPlate from "./WellPlates";
import Wafer from "./Wafers";

import { VESSEL_TYPES, VESSELS } from "../../utils/vessel-types";

export default {
  name: "SelectDialog",

  components: {
    SimpleDialog,
    Slide,
    Dish,
    Wafer,
    WellPlate,
  },

  data: () => ({
    vesselTypes: VESSEL_TYPES,
    vessels: VESSELS,
    selectedTab: null,
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
