<template>
  <small-card title="Box Select">
    <CustomButton image="mono" label="8" @click="select1" />
    <CustomButton image="mono" label="16" @click="select2" />
    <CustomButton image="mono" label="32" @click="select3" />
    <CustomButton image="color" label="8" @click="select4" />
    <CustomButton image="color" label="16" @click="select5" />
    <CustomButton image="color" label="32" @click="select6" />
  </small-card>
</template>

<script>
import SmallCard from "../../../custom/SmallCard";
import CustomButton from "../../../custom/CustomButton";

export default {
  name: "BitConversion",

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
    select6: function () {
      console.log("Select-6");
    },
  },
};
</script>
