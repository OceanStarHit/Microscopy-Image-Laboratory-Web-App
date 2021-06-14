<template>
  <small-card title="Count">
    <custom-button icon="calculator" label="Count" @click="onCount" />
    <custom-button icon="replay" label="Back" @click="onBack" />
    <custom-button
      icon="arrow-collapse-vertical"
      label="Split"
      @click="onSplit"
    />
  </small-card>
</template>

<script>
import SmallCard from "../../../custom/SmallCard";
import CustomButton from "../../../custom/CustomButton";

export default {
  name: "Count",

  components: {
    SmallCard,
    CustomButton,
  },

  data: () => ({}),

  methods: {
    onCount: () => {
      console.log("Count");
    },
    onBack: () => {
      console.log("Back");
    },
    onSplit: () => {
      console.log("Split");
    },
  },
};
</script>
