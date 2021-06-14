<template>
  <v-card class="pa-1" flat>
    <h5>Object Select</h5>
    <small-card title="Object Brightness" :child="true">
      <custom-button icon="lightbulb-outline" label="Light" @click="onLight" />
      <custom-button icon="lightbulb" label="Black" @click="onBlack" />
    </small-card>
    <small-card title="Select Target" :child="true">
      <custom-button icon="gesture-tap" label="Object" @click="onObject" />
      <custom-button icon="layers-triple" label="Area" @click="onArea" />
      <custom-button icon="gesture-tap-button" label="Back" @click="onBack" />
      <custom-button icon="cog" label="Set" @click="onSet" />
    </small-card>
  </v-card>
</template>

<script>
import SmallCard from "../../../custom/SmallCard";
import CustomButton from "../../../custom/CustomButton";

export default {
  name: "ObjectSelect",

  components: {
    SmallCard,
    CustomButton,
  },

  data: () => ({}),

  methods: {
    onLight: () => {
      console.log("Light");
    },
    onBlack: () => {
      console.log("Black");
    },
    onObject: () => {
      console.log("Object");
    },
    onArea: () => {
      console.log("Area");
    },
    onBack: () => {
      console.log("Back");
    },
    onSet: () => {
      console.log("Set");
    },
  },
};
</script>
