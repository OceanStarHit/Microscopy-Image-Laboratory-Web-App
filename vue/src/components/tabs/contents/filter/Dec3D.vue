<template>
  <small-card title="3D Deconvolution">
    <custom-button icon="play-circle" label="3D-Go" @click="DDDConvolve" />
    <custom-button icon="cog" label="Set" @click="select2" />
  </small-card>
</template>

<script>
import SmallCard from "../../../custom/SmallCard";
import CustomButton from "../../../custom/CustomButton";

export default {
  name: "Dec3D",

  components: {
    SmallCard,
    CustomButton
  },

  data: () => ({}),

  methods: {
    DDDConvolve: function() {
      console.log("Thing to do")
    },
    select2: function() {
      console.log("Select-2");
    }
  }
};
</script>
