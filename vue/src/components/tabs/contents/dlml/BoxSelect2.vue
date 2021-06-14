<template>
  <small-card title="Box Select">
    <custom-button icon="near-me" @click="select1" />
    <custom-button icon="pencil" @click="select2" />
    <custom-button icon="checkbox-blank-circle-outline" @click="select3" />
    <custom-button icon="dots-vertical" @click="select4" />
    <custom-button icon="vector-rectangle" @click="select5" />
    <custom-button icon="square-edit-outline" @click="select6" />
    <custom-button icon="trash-can-outline" @click="select7" />
  </small-card>
</template>

<script>
import SmallCard from "../../../custom/SmallCard";
import CustomButton from "../../../custom/CustomButton";

export default {
  name: "BoxSelect2",

  components: {
    SmallCard,
    CustomButton,
  },

  data: () => ({}),

  methods: {
    select1: () => {
      console.log("Select-1");
    },
    select2: () => {
      console.log("Select-2");
    },
    select3: () => {
      console.log("Select-3");
    },
    select4: () => {
      console.log("Select-4");
    },
    select5: () => {
      console.log("Select-5");
    },
    select6: () => {
      console.log("Select-6");
    },
    select7: () => {
      console.log("Select-7");
    },
  },
};
</script>
