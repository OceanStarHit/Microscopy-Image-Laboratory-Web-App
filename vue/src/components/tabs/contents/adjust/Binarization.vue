<template>
  <small-card title="Binarization">
    <custom-button icon="creation" label="Auto" @click="select1" />
    <custom-button icon="tune-vertical" label="Adjust" @click="select2" />
  </small-card>
</template>

<script>
import SmallCard from "../../../custom/SmallCard";
import CustomButton from "../../../custom/CustomButton";

export default {
  name: "Binarization",

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
