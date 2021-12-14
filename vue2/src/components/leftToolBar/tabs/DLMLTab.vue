<template>
  <TabItem
    :title="'Learning'"
    :is-buttons="true"
    @refresh="refresh"
    @help="help"
  >
    <v-expansion-panels v-model="panel" focusable>
      <expansion-panel title="Deep Learning">
        <Judge />
        <v-divider />
        <MethodSelect />
        <v-divider />
        <BoxSelect />
        <v-divider />
        <ObjectSelect />
        <v-divider />
        <ObjectClass />
        <v-divider />
        <ClassObjectStatus />
      </expansion-panel>

      <expansion-panel title="Machine Learning">
        <MethodSelect />
        <v-divider />
        <BoxSelect />
        <v-divider />
        <ObjectSelect />
        <v-divider />
        <Count />
        <v-divider />
        <ObjectClass />
        <v-divider />
        <ClassObjectStatus />
      </expansion-panel>
    </v-expansion-panels>
  </TabItem>
</template>

<script lang="ts">
import Component from 'vue-class-component';
import Vue from 'vue';

import TabItem from '@/components/custom/TabItem.vue';
import ExpansionPanel from '@/components/custom/ExpansionPanel.vue';
import Judge from '@/components/tabs/contents/dlml/Judge.vue';
import MethodSelect from '@/components/tabs/contents/dlml/MethodSelect.vue';
import BoxSelect from '@/components/tabs/contents/dlml/BoxSelect.vue';
import ObjectSelect from '@/components/tabs/contents/dlml/ObjectSelect.vue';
import ObjectClass from '@/components/tabs/contents/dlml/ObjectClass.vue';
import ClassObjectStatus from '@/components/tabs/contents/dlml/ClassObjectStatus.vue';
import Count from '@/components/tabs/contents/dlml/Count.vue';

@Component({
  components: {
    TabItem,
    ExpansionPanel,
    Judge,
    MethodSelect,
    BoxSelect,
    ObjectSelect,
    ObjectClass,
    ClassObjectStatus,
    Count,
  },
})
export default class DLMLTab extends Vue {

  panel = 0;

  refresh(): void {
    console.log('refresh');
  }

  help(): void {
    console.log('help');
  }
}
</script>
