<template>
  <v-dialog v-model="visibleDialog" max-width="980">
    <simple-dialog title="Position" @select="visibleDialog = false">
      <v-tabs v-model="selectedTab" fixed-tabs>
        <v-tab href="#tabs-1" class="primary--text">Images</v-tab>
        <v-tab href="#tabs-2" class="primary--text">Tiling</v-tab>
        <v-tab href="#tabs-3" class="primary--text">Metadata</v-tab>
        <v-tab href="#tabs-4" class="primary--text">Names & Types</v-tab>
      </v-tabs>

      <v-tabs-items v-model="selectedTab">
        <v-tab-item value="tabs-1">
          <v-row class="pa-5" style="height: 220px;">Images</v-row>
        </v-tab-item>
        <v-tab-item value="tabs-2"
          ><v-row class="pa-5" style="height: 220px;">Tiling</v-row></v-tab-item
        >
        <v-tab-item value="tabs-3"
          ><v-row class="pa-5" style="height: 220px;"
            >Metadata</v-row
          ></v-tab-item
        >
        <v-tab-item value="tabs-4"
          ><v-row class="pa-5" style="height: 220px;"
            >Names & Types</v-row
          ></v-tab-item
        >
      </v-tabs-items>
    </simple-dialog>
  </v-dialog>
</template>

<script>
// import { mapGetters } from "vuex";

import SimpleDialog from "../../../custom/SimpleDialog";

export default {
  name: "OpenPositionDialog",

  components: { SimpleDialog },

  data: () => ({
    selectedTab: null
  }),

  props: {
    value: {
      type: Boolean,
      default: false
    }
  },

  computed: {
    visibleDialog: {
      get() {
        return this.value;
      },
      set(val) {
        this.$emit("input", val);
      }
    }
  },

  methods: {
    onClick: function() {
      //
    }
  }
};
</script>

<style scoped></style>
