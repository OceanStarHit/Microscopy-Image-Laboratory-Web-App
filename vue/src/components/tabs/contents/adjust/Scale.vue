<template>
  <small-card title="Scale">
    <custom-button icon="ruler" label="ScaleBar" @click="select1" />
    <custom-button icon="grid" label="Grid" @click="select2" />
    <custom-button icon="cog" label="Set" @click="scaleSetDialog = true" />
    
    <open-scale-set-dialog v-model="scaleSetDialog" />

  </small-card>
</template>

<script>
import SmallCard from "../../../custom/SmallCard";
import CustomButton from "../../../custom/CustomButton";
import OpenScaleSetDialog from "./OpenScaleSetDialog";
export default {
  name: "Scale",

  components: {
    SmallCard,
    CustomButton,
    OpenScaleSetDialog
  },

  data: () => ({
    scaleSetDialog: false,    
  }),

  methods: {
    select1: function() {
      console.log("Select-1");
    },
    select2: function() {
      console.log("Select-2");
    },
    select3: function() {
      console.log("Select-3");
    }
  }
};
</script>
