<template>
  <tab-item title="Learning" :buttons="true" @refresh="refresh" @help="help">
    <v-expansion-panels v-model="panel" focusable>
      <expansion-panel title="Deep Learning">
        <Judge />
        <v-divider></v-divider>
        <MethodSelect />
        <v-divider></v-divider>
        <BoxSelect />
        <v-divider></v-divider>
        <ObjectSelect />
        <v-divider></v-divider>
        <ObjectClass />
        <v-divider></v-divider>
        <ClassObjectStatus />
      </expansion-panel>

      <expansion-panel title="Machine Learning">
        <MethodSelect2 />
        <v-divider></v-divider>
        <BoxSelect2 />
        <v-divider></v-divider>
        <ObjectSelect2 />
        <v-divider></v-divider>
        <Count />
        <v-divider></v-divider>
        <ObjectClass2 />
        <v-divider></v-divider>
        <ClassObjectStatus2 />
      </expansion-panel>
    </v-expansion-panels>
  </tab-item>
</template>

<script>
import TabItem from "../custom/TabItem.vue";
import ExpansionPanel from "../custom/ExpansionPanel.vue";
import Judge from "./contents/dlml/Judge";
import MethodSelect from "./contents/dlml/MethodSelect";
import BoxSelect from "./contents/dlml/BoxSelect";
import ObjectSelect from "./contents/dlml/ObjectSelect";
import ObjectClass from "./contents/dlml/ObjectClass";
import ClassObjectStatus from "./contents/dlml/ClassObjectStatus";
import MethodSelect2 from "./contents/dlml/MethodSelect2";
import BoxSelect2 from "./contents/dlml/BoxSelect2";
import ObjectSelect2 from "./contents/dlml/ObjectSelect2";
import Count from "./contents/dlml/Count";
import ObjectClass2 from "./contents/dlml/ObjectClass2";
import ClassObjectStatus2 from "./contents/dlml/ClassObjectStatus2";

export default {
  name: "DLMLTab",

  components: {
    TabItem,
    ExpansionPanel,
    Judge,
    MethodSelect,
    BoxSelect,
    ObjectSelect,
    ObjectClass,
    ClassObjectStatus,
    MethodSelect2,
    BoxSelect2,
    ObjectSelect2,
    Count,
    ObjectClass2,
    ClassObjectStatus2,
  },

  data: () => ({
    panel: 0,
  }),

  methods: {
    refresh: function () {
      console.log("Refresh");
    },
    help: function () {
      console.log("Help");
    },
  },
};
</script>
