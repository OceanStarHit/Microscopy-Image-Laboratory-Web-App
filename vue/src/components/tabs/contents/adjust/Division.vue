<template>
  <small-card title="Division">
    <custom-button icon="eye-outline" label="view method" @click="select1" />
    <custom-button icon="undo" label="undo" @click="select2" />
  </small-card>
</template>

<script>
import SmallCard from "../../../custom/SmallCard";
import CustomButton from "../../../custom/CustomButton";

export default {
  name: "Division",

  components: {
    SmallCard,
    CustomButton
  },

  data: () => ({}),

  methods: {
    select1: function() {
      console.log("Select-1");
    },
    select2: function() {
      console.log("Select-2");
    }
  }
};
</script>
