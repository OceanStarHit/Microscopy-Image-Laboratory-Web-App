<template>
  <small-card title="Field of View Optimization">
    <custom-button icon="chart-areaspline" label="AVG" @click="select1" />
    <custom-button icon="contrast-circle" label="DPC" @click="select2" />
    <custom-button icon="alpha-w-box-outline" label="WB" @click="select3" />
    <custom-button icon="alpha-b-box-outline" label="BB" @click="select4" />
    <custom-button icon="cog" label="Set" @click="select5" />
  </small-card>
</template>

<script>
import SmallCard from "../../../custom/SmallCard";
import CustomButton from "../../../custom/CustomButton";

export default {
  name: "FVO",

  components: {
    SmallCard,
    CustomButton,
  },

  data: () => ({}),

  methods: {
    select1: function () {
      console.log("Select-1");
    },
    select2: function () {
      console.log("Select-2");
    },
    select3: function () {
      console.log("Select-3");
    },
    select4: function () {
      console.log("Select-4");
    },
    select5: function () {
      console.log("Select-5");
    },
  },
};
</script>
