<template>
  <tab-item
    title="Filter"
    :buttons="true"
    @refresh="refresh"
    @help="help"
  >
    <Filters />
    <v-divider class="my-2" />
    <AddSub />
    <v-divider class="my-2" />
    <Dec2D />
    <v-divider class="my-2" />
    <Dec3D />
    <v-divider class="my-2" />
    <FocusStack />
    <!-- <v-divider class="my-2"></v-divider>
    <DPC /> -->
  </tab-item>
</template>

<script>
import TabItem from '../../custom/TabItem.vue';
import Filters from '../../tabs/contents/filter/Filters';
import AddSub from '../../tabs/contents/filter/AddSub';
import Dec2D from '../../tabs/contents/filter/Dec2D';
import Dec3D from '../../tabs/contents/filter/Dec3D';
import FocusStack from '../../tabs/contents/filter/FocusStack';
// import DPC from "./contents/filter/DPC";

export default {
  name: 'FilterTab',

  components: {
    TabItem,
    Filters,
    AddSub,
    Dec2D,
    Dec3D,
    FocusStack
    // DPC
  },

  data: () => ({}),

  methods: {
    refresh: function() {
      console.log('Refresh');
    },
    help: function() {
      console.log('Help');
    }
  }
};
</script>
