<template>
  <small-card title="2D Deconvolution">
    <custom-button icon="play-circle" label="2D-Go" @click="DDConvolve" />
    <custom-button icon="cog" label="Set" @click="select2" />
  </small-card>
</template>

<script>
import SmallCard from "../../../custom/SmallCard";
import CustomButton from "../../../custom/CustomButton";

export default {
  name: "Dec2D",

  components: {
    SmallCard,
    CustomButton
  },

  data: () => ({}),

  methods: {
    DDConvolve: function() {
      console.log("Thing to do")
    },
    select2: function() {
      console.log("Select-2");
    }
  }
};
</script>
