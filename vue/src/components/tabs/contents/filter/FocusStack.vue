<template>
  <small-card title="Focus Stack">
    <custom-button icon="play-circle" label="Go" @click="select1" />
    <custom-button
      icon="format-align-center"
      label="Alignment"
      @click="select2"
    />
    <custom-button icon="cog" label="Set" @click="select3" />
  </small-card>
</template>

<script>
import SmallCard from "../../../custom/SmallCard";
import CustomButton from "../../../custom/CustomButton";

export default {
  name: "FocusStack",

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
  },
};
</script>
