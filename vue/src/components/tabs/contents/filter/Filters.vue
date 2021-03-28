<template>
  <small-card title="Filter">
    <custom-button icon="numeric-2-box" label="2-D" @click="select1" />
    <custom-button icon="numeric-3-box" label="3-D" @click="select2" />
  </small-card>
</template>

<script>
import SmallCard from "../../../custom/SmallCard";
import CustomButton from "../../../custom/CustomButton";

export default {
  name: "Filters",

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
  },
};
</script>
