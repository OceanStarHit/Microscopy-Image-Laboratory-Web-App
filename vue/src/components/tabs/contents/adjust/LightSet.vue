<template>
  <small-card title="Light Set">
    <custom-button icon="creation" label="Auto" @click="select1" />
    <custom-button icon="hdr" label="HRD" @click="select2" />
    <custom-button icon="thumb-up-outline" label="Go" @click="select3" />
    <custom-button icon="cog" label="Set" @click="select4" />
  </small-card>
</template>

<script>
import SmallCard from "../../../custom/SmallCard";
import CustomButton from "../../../custom/CustomButton";

export default {
  name: "LightSet",

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
  },
};
</script>
