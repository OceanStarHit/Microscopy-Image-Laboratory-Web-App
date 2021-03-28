<template>
  <v-container class="pa-0" fluid>
    <v-row no-gutters>
      <!-- Left Sidebar -->
      <v-col cols="2">
        <v-container
          class="px-3 py-0 auto-scroll d-flex flex-column justify-space-between"
          :style="{
            height: windowHeight + 'px',
          }"
        >
          <div>
            <v-tabs v-model="selectedTab1" class="margin: 0;" grow>
              <v-tab href="#tabs-1-1" class="primary--text">
                <v-icon>mdi-school</v-icon>
              </v-tab>

              <v-tab href="#tabs-1-2" class="primary--text">
                <v-icon>mdi-tune</v-icon>
              </v-tab>

              <v-tab href="#tabs-1-3" class="primary--text">
                <v-icon>mdi-filter</v-icon>
              </v-tab>

              <v-tab href="#tabs-1-4" class="primary--text">
                <v-icon>mdi-file</v-icon>
              </v-tab>
            </v-tabs>

            <v-tabs-items v-model="selectedTab1">
              <v-tab-item value="tabs-1-1">
                <DLMLTab />
              </v-tab-item>
              <v-tab-item value="tabs-1-2">
                <AdjustTab />
              </v-tab-item>
              <v-tab-item value="tabs-1-3">
                <FilterTab />
              </v-tab-item>
              <v-tab-item value="tabs-1-4">
                <FileTab />
              </v-tab-item>
            </v-tabs-items>
          </div>
          <v-progress-linear
            class="mb-8"
            color="light-blue"
            height="15"
            value="40"
            rounded
            striped
          ></v-progress-linear>
        </v-container>
      </v-col>

      <!--  -->
      <v-col
        class="grey lighten-3"
        cols="8"
        :style="{
          height: windowHeight + 'px',
        }"
        style="border-left: 1px dotted gray; border-right: 1px dotted gray"
      >
        <ImageViewer />
      </v-col>

      <!-- Right Sidebar -->
      <v-col cols="2">
        <v-container
          class="px-1 py-0 auto-scroll"
          :style="{
            height: windowHeight + 'px',
          }"
        >
          <v-tabs v-model="selectedTab2" grow>
            <v-tab href="#tabs-2-1" class="primary--text">
              <v-icon>mdi-microscope</v-icon>
            </v-tab>

            <v-tab href="#tabs-2-2" class="primary--text">
              <v-icon>mdi-pencil-ruler</v-icon>
            </v-tab>

            <v-tab href="#tabs-2-3" class="primary--text">
              <v-icon>mdi-poll-box</v-icon>
            </v-tab>

            <v-tab href="#tabs-2-4" class="primary--text">
              <v-icon>mdi-cogs</v-icon>
            </v-tab>
          </v-tabs>

          <v-tabs-items v-model="selectedTab2">
            <v-tab-item value="tabs-2-1">
              <ViewTab />
            </v-tab-item>
            <v-tab-item value="tabs-2-2">
              <MeasureTab />
            </v-tab-item>
            <v-tab-item value="tabs-2-3">
              <ReportTab />
            </v-tab-item>
            <v-tab-item value="tabs-2-4">
              <SettingsTab />
            </v-tab-item>
          </v-tabs-items>
        </v-container>
      </v-col>
    </v-row>
    <loading
      :active.sync="loading"
      :can-cancel="false"
      :is-full-page="true"
      :opacity="0.6"
    >
      <v-container class="text-center">
        <v-progress-circular
          :size="50"
          color="teal"
          indeterminate
        ></v-progress-circular>
        <div class="title mt-4 teal--text">Loading...</div>
      </v-container>
    </loading>
  </v-container>
</template>

<script>
import { mapState } from "vuex";
import Loading from "vue-loading-overlay";
import "vue-loading-overlay/dist/vue-loading.css";

import ImageViewer from "./ImageViewer";
import DLMLTab from "./tabs/DLMLTab";
import AdjustTab from "./tabs/AdjustTab";
import FilterTab from "./tabs/FilterTab";
import FileTab from "./tabs/FileTab";
import ViewTab from "./tabs/ViewTab";
import MeasureTab from "./tabs/MeasureTab";
import ReportTab from "./tabs/ReportTab";
import SettingsTab from "./tabs/SettingsTab";

export default {
  name: "MainFrame",

  components: {
    Loading,

    ImageViewer,
    DLMLTab,
    AdjustTab,
    FilterTab,
    FileTab,
    ViewTab,
    MeasureTab,
    ReportTab,
    SettingsTab,
  },

  data() {
    var self = this;
    return {
      selectedTab1: "tabs-1-4",
      selectedTab2: null,
      windowHeight: self.getWindowHeight(),
    };
  },

  computed: {
    ...mapState({
      loading: (state) => state.image.loading,
    }),
  },

  mounted() {
    window.onresize = () => {
      this.windowHeight = this.getWindowHeight();
    };
  },

  methods: {
    getWindowHeight: function () {
      try {
        return (
          window.innerHeight -
          parseInt(document.getElementsByTagName("header")[0].style.height)
        );
      } catch (err) {
        return window.innerHeight - 64;
      }
    },
  },
};
</script>

<style scoped>
.auto-scroll {
  overflow: auto;
}
</style>
