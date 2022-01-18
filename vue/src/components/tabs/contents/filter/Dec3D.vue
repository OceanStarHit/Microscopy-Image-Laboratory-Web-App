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
      var formData = new FormData();
      var image_name = this.$store.state.image.imageUri
      formData.append("files_name", image_name.data.path_images[0]);
      this.$store.dispatch("image/convol3D", formData); 
    },
    select2: function() {
      console.log("Select-2");
    }
  }
};
</script>
