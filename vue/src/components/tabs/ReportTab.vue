<template>
  <tab-item title="Report">
    <small-card title="Save">
      <custom-button
        icon="cloud-upload-outline"
        label="Cloud"
        @click="onClick1"
      />
      <custom-button icon="microsoft-excel" label="Excel" @click="onClick2" />
      <custom-button
        icon="file-delimited-outline"
        label="CSV"
        @click="onClick3"
      />
      <custom-button icon="file-code-outline" label="HDF5" @click="onClick4" />
    </small-card>
    <v-divider class="my-2"></v-divider>
    <small-card title="View">
      <custom-button
        icon="chart-timeline-variant-shimmer"
        label="Visual"
        @click="onClick5"
      />
      <custom-button
        icon="tablet-dashboard"
        label="Tableau"
        @click="onClick6"
      />
    </small-card>
  </tab-item>
</template>

<script>
import TabItem from "../custom/TabItem";
import SmallCard from "../custom/SmallCard";
import CustomButton from "../custom/CustomButton";

export default {
  name: "ReportTab",

  components: { TabItem, SmallCard, CustomButton },

  data: () => ({}),

  methods: {
    onClick1: function () {
      console.log("Click1");
    },
    onClick2: function () {
      console.log("Click2");
    },
    onClick3: function () {
      console.log("Click3");
    },
    onClick4: function () {
      console.log("Click4");
    },
    onClick5: function () {
      console.log("Click5");
    },
    onClick6: function () {
      console.log("Click6");
    },
  },
};
</script>
