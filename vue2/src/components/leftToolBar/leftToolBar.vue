<template>
  <v-col cols="2">
    <v-container
      class="px-3 py-0 auto-scroll d-flex flex-column justify-space-between"
      :style="{ height: height + 'px' }"
    >
      <div>
        <v-tabs
          v-model="selectedTab"
          class="margin: 0;"
          grow
        >
          <v-tab href="#1" class="primary--text">
            <v-icon>mdi-school</v-icon>
          </v-tab>

          <v-tab href="#2" class="primary--text">
            <v-icon>mdi-tune</v-icon>
          </v-tab>

          <v-tab href="#3" class="primary--text">
            <v-icon>mdi-filter</v-icon>
          </v-tab>

          <v-tab href="#4" class="primary--text">
            <v-icon>mdi-file</v-icon>
          </v-tab>
        </v-tabs>

        <v-tabs-items v-model="selectedTab">
          <v-tab-item value="1">
            <DLMLTab />
          </v-tab-item>
          <v-tab-item value="2">
            <AdjustTab />
          </v-tab-item>
          <v-tab-item value="3">
            <FilterTab />
          </v-tab-item>
          <v-tab-item value="4">
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
      />
    </v-container>
  </v-col>
</template>

<script lang="ts">
import Component from 'vue-class-component';
import Vue from 'vue';
import DLMLTab from '@/components/leftToolBar/tabs/DLMLTab.vue';
import AdjustTab from '@/components/leftToolBar/tabs/AdjustTab.vue';
import FilterTab from '@/components/leftToolBar/tabs/FilterTab.vue';
import FileTab from '@/components/leftToolBar/tabs/FileTab.vue';

@Component({
  components: {
    DLMLTab,
    AdjustTab,
    FilterTab,
    FileTab,
  }
})
export default class LeftToolBarComponent extends Vue {

  get height(): number {
    return this.$store.state.view.windowSize.heightPx;
  }

  get selectedTab(): string {
    return this.$store.state.toolBarView.leftToolBarSelectedTab;
  }

  set selectedTab(tab: string) {
    console.log(tab);
    this.$store.dispatch('toolBarView/actionChangeLeftToolBarTab', tab);
  }
}
</script>

<style scoped>

</style>
