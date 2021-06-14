<template>
  <small-card title="Addition / Subtraction">
    <custom-button icon="plus-thick" label="Add" @click="select1" />
    <custom-button icon="minus-thick" label="Sub" @click="select2" />
    <custom-button icon="check-circle" label="Correction" @click="select3" />
    <custom-button icon="tune-variant" label="Options" @click="select4" />
  </small-card>
</template>

<script>
import SmallCard from "../../../custom/SmallCard";
import CustomButton from "../../../custom/CustomButton";

export default {
  name: "AddSub",

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
