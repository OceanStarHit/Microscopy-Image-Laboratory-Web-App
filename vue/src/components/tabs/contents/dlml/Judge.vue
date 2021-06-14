<template>
  <small-card title="Judge">
    <custom-button icon="play-circle-outline" label="Go" @click="onGo" />
    <custom-button icon="thumb-up-outline" label="Good" @click="onGood" />
    <custom-button icon="thumb-down-outline" label="No" @click="onNo" />
    <custom-button icon="keyboard-return" label="Return" @click="onReturn" />
  </small-card>
</template>

<script>
import SmallCard from "../../../custom/SmallCard";
import CustomButton from "../../../custom/CustomButton";

export default {
  name: "Judge",

  components: {
    SmallCard,
    CustomButton,
  },

  data: () => ({}),

  methods: {
    onGo: () => {
      console.log("Go");
    },
    onGood: () => {
      console.log("Good");
    },
    onNo: () => {
      console.log("No");
    },
    onReturn: () => {
      console.log("Return");
    },
  },
};
</script>
