<template>
  <v-btn
    class="px-0"
    min-width="24"
    :height="label ? 38 : 28"
    @click="clicked"
    text
    color="teal"
  >
    <div class="ma-0">
      <div v-if="image" class="pa-1">
        <v-img style="margin: 0 auto" width="12" height="12" :src="imageUrl" />
      </div>
      <v-icon v-if="icon" class="ma-0" :dense="true">mdi-{{ icon }}</v-icon>
      <div class="label-text caption">{{ label }}</div>
    </div>
  </v-btn>
</template>

<script>
export default {
  name: "CustomButton",

  data: () => ({}),

  props: ["icon", "image", "label"],

  computed: {
    imageUrl() {
      return require("../../assets/images/" + this.image + ".png");
    },
  },

  methods: {
    clicked: function () {
      this.$emit("click");
    },
  },
};
</script>

<style scoped>
.label-text {
  text-transform: capitalize !important;
  line-height: 0.75rem;
}
</style>
