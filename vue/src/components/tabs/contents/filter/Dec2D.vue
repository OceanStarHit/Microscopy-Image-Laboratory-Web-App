<template>
  <small-card title="2D Deconvolution">
    <custom-button icon="play-circle" label="2D-Go" @click="select1" />
    <custom-button icon="cog" label="Set" @click="select2" />
  </small-card>
</template>

<script>
import SmallCard from "../../../custom/SmallCard";
import CustomButton from "../../../custom/CustomButton";

export default {
  name: "Dec2D",

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
