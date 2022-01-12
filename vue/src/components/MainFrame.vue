<template>
  <v-container class="pa-0" fluid>
    <v-row no-gutters>
      <!-- Left Sidebar -->
      <v-col cols="2">
        <v-container
          class="px-3 py-0 auto-scroll d-flex flex-column justify-space-between"
          :style="{ height: windowHeight + 'px' }"
        >
          <div>
            <v-tabs v-model="selectedTabLeft" class="margin: 0;" grow>
              <v-tab href="#tabs-1-2" class="primary--text">
                <v-icon>mdi-school</v-icon>
              </v-tab>

              <v-tab href="#tabs-1-3" class="primary--text">
                <v-icon>mdi-tune</v-icon>
              </v-tab>

              <v-tab href="#tabs-1-4" class="primary--text">
                <v-icon>mdi-filter</v-icon>
              </v-tab>

              <v-tab href="#tabs-1-1" class="primary--text">
                <v-icon>mdi-file</v-icon>
              </v-tab>

              
            </v-tabs>

            <v-tabs-items v-model="selectedTabLeft">
              <v-tab-item value="tabs-1-1">
                <FileTab />
              </v-tab-item>
              <v-tab-item value="tabs-1-2">
                <DLMLTab />
              </v-tab-item>
              <v-tab-item value="tabs-1-3">
                <AdjustTab />
              </v-tab-item>
              <v-tab-item value="tabs-1-4">
                <FilterTab />
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

      <!-- Center  -->
      <v-col
        class="grey lighten-3"
        cols="8"
        :style="{
          height: windowHeight + 'px'
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
            height: windowHeight + 'px'
          }"
        >
          <v-tabs v-model="selectedTabRight" grow>
            <v-tab href="#tabs-2-1" class="primary--text">
              <v-icon>mdi-microscope</v-icon>
            </v-tab>

            <v-tab href="#tabs-2-2" class="primary--text">
              <v-icon>mdi-pencil-ruler</v-icon>
            </v-tab>

            <v-tab href="#tabs-2-3" class="primary--text">
              <v-icon>mdi-poll</v-icon> 
            </v-tab>

            <v-tab href="#tabs-2-4" class="primary--text">
              <v-icon>mdi-cogs</v-icon>
            </v-tab>
          </v-tabs>

          <v-tabs-items v-model="selectedTabRight">
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

    <!-- <loading
      :active.sync="loading_count_gt_zero"
      :can-cancel="false"
      :is-full-page="true"
      :opacity="0.8"
    >
      <v-container class="text-center loading-progress-bar">
        <v-progress-linear
          color="light-blue"
          height="15"
          :value="loading_bar_value"
          striped
        ></v-progress-linear>
        <div class="title mt-4 teal--text">In update ...</div>
      </v-container>
    </loading>

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
    </loading> -->
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
    // Loading,

    ImageViewer,
    DLMLTab,
    AdjustTab,
    FilterTab,
    FileTab,
    ViewTab,
    MeasureTab,
    ReportTab,
    SettingsTab
  },

  data() {
    var self = this;
    return {
      selectedTabLeft: null,
      selectedTabRight: null,
      windowHeight: self.getWindowHeight()
    };
  },

  computed: {
    ...mapState({
      loading: state => state.image.loading,
      loading_count: state => state.image.loading_count,
      loading_count_max: state => state.image.loading_count_max
    }),
    loading_count_gt_zero: function() {
      return this.loading_count > 0;
    },
    loading_bar_value: function() {
      let v = 0;
      if (this.loading_count_max != 0) {
        v =
          100 *
          ((this.loading_count_max - this.loading_count) /
            this.loading_count_max);
      }
      console.log(this.loading_count_max + " " + this.loading_count + " " + v);
      return v;
    }
  },

  mounted() {
    window.onresize = () => {
      this.windowHeight = this.getWindowHeight();
    };
  },

  methods: {
    getWindowHeight: function() {
      return window.innerHeight - 64;
      // try {
      //   return (
      // if (document.getElementsByTagName("header")[0]) {
      //   window.innerHeight -
      //   parseInt(document.getElementsByTagName("header")[0].style.height);
      // } else {
      //   return window.innerHeight;
      // }

      //   );
      // } catch (err) {
      //   return window.innerHeight - 64;
      // }
    }
  }
};
</script>

<style scoped>
v-tab {
  padding: 0px !important;
}
.auto-scroll {
  overflow: auto;
}
.loading-progress-bar {
  width: 300pt;
}
.v-tab{
  min-width: 50px;
}
.v-slide-group__content{
  height: 2px;
  left: 0px;
  width: 50px;
}
</style>
