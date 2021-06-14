<template>
  <small-card title="Class & Object Status">
    <custom-button icon="square-rounded-outline" label="Area" @click="onArea" />
    <custom-button icon="palette-outline" label="Color" @click="onColor" />
    <custom-button icon="palette-swatch-outline" label="Int" @click="onInt" />
    <custom-button icon="cog" label="Set" @click="onSet" />
  </small-card>
</template>

<script>
import SmallCard from "../../../custom/SmallCard";
import CustomButton from "../../../custom/CustomButton";

export default {
  name: "ClassObjectStatus2",

  components: {
    SmallCard,
    CustomButton,
  },

  data: () => ({}),

  methods: {
    onArea: () => {
      console.log("onArea");
    },
    onColor: () => {
      console.log("onColor");
    },
    onInt: () => {
      console.log("onInt");
    },
    onSet: () => {
      console.log("onSet");
    },
  },
};
</script>
