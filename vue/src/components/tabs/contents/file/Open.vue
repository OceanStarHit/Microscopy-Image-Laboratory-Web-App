<template>
  <small-card title="Open">
    <input type="file" id="uploadFile" @change="requestUploadFile" />
    <custom-button
      icon="cloud-download-outline"
      label="Cloud"
      @click="onCloud"
    />
    <custom-button icon="email-newsletter" label="File" @click="onFile" />
    <custom-button
      icon="folder-open-outline"
      label="Folder"
      @click="onFolder"
    />
    <custom-button icon="dots-grid" label="Position" @click="onPosition" />
  </small-card>
</template>

<script>
import SmallCard from "../../../custom/SmallCard";
import CustomButton from "../../../custom/CustomButton";

export default {
  name: "Open",

  components: {
    SmallCard,
    CustomButton,
  },

  data: () => ({
    imageSource: null,
  }),

  computed: {},

  methods: {
    onCloud: function () {
      console.log("Cloud");
    },
    onFile: function () {
      this.$el.querySelector("#uploadFile").click();
    },
    onFolder: function () {
      console.log("Folder");
    },
    onPosition: function () {
      console.log("Position");
    },
  },
};
</script>

<style scoped>
#uploadFile {
  display: none;
}
</style>
