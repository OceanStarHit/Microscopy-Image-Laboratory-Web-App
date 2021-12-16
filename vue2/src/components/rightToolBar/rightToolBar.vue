<template>
  <v-col cols="2">
    <v-container
      class="px-1 py-0 auto-scroll"
      :style="{
        height: height + 'px'
      }"
    >
      <v-tabs v-model="selectedTab" grow>
        <v-tab href="#1" class="primary--text">
          <v-icon>mdi-microscope</v-icon>
        </v-tab>

        <v-tab href="#2" class="primary--text">
          <v-icon>mdi-pencil-ruler</v-icon>
        </v-tab>

        <v-tab href="#3" class="primary--text">
          <v-icon>mdi-poll</v-icon>
        </v-tab>

        <v-tab href="#4" class="primary--text">
          <v-icon>mdi-cogs</v-icon>
        </v-tab>
      </v-tabs>

      <v-tabs-items v-model="selectedTab">
        <!--        <v-tab-item value="1">-->
        <!--          <ViewTab />-->
        <!--        </v-tab-item>-->
        <v-tab-item value="2">
          <MeasureTab />
        </v-tab-item>
        <v-tab-item value="3">
          <ReportTab />
        </v-tab-item>
        <v-tab-item value="4">
          <SettingsTab />
        </v-tab-item>
      </v-tabs-items>
    </v-container>
  </v-col>
</template>
<script lang="ts">
import Component from 'vue-class-component';
import Vue from 'vue';
// import ViewTab from '@/components/rightToolBar/tabs/ViewTab.vue';
import MeasureTab from '@/components/rightToolBar/tabs/MeasureTab.vue';
import ReportTab from '@/components/rightToolBar/tabs/ReportTab.vue';
import SettingsTab from '@/components/rightToolBar/tabs/SettingsTab.vue';

@Component({
  components: {
    // ViewTab,
    MeasureTab,
    ReportTab,
    SettingsTab
  }
})
export default class LeftToolBarComponent extends Vue {
  get height(): number {
    return this.$store.state.view.windowSize.heightPx;
  }

  get selectedTab(): string {
    return this.$store.state.toolBarView.rightToolBarSelectedTab;
  }

  set selectedTab(tab: string) {
    console.log(tab);
    this.$store.dispatch('toolBarView/actionChangeRightToolBarTab', tab);
  }
}
</script>

<style scoped>

</style>
