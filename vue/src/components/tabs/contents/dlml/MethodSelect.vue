<template>
  <small-card title="Method Select">
    <custom-button icon="plus-box" label="New" @click="onNew" />
    <custom-button icon="play-box" label="Call" @click="onCall" />
  </small-card>
</template>

<script>
import SmallCard from "../../../custom/SmallCard";
import CustomButton from "../../../custom/CustomButton";

export default {
  name: "MethodSelect",

  components: {
    SmallCard,
    CustomButton,
  },

  data: () => ({}),

  methods: {
    onNew: () => {
      console.log("New");
    },
    onCall: () => {
      console.log("Call");
    },
  },
};
</script>
