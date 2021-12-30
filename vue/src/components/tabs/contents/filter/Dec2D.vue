<template>
  <small-card title="2D Deconvolution">
    <custom-button icon="play-circle" label="2D-Go" @click="select1" />
    <custom-button icon="cog" label="Setting" @click="settingDialog = true" />
    <open-2D-setting-dialog v-model="settingDialog" />
  </small-card>
</template>

<script>
import SmallCard from "../../../custom/SmallCard";
import Open2DSettingDialog from "../file/Open2DSettingDialog";
import CustomButton from "../../../custom/CustomButton";

export default {
  name: "Dec2D",

  components: {
    SmallCard,
    Open2DSettingDialog,
    CustomButton
  },

  data: () => ({
    settingDialog: false
  }),

  methods: {
    select1: function() {
      console.log("Select-1");
    }
    // select2: function() {
    //   console.log("Select-2");
    // }
  }
};
</script>
