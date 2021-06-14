<template>
  <v-card class="pa-1" flat>
    <div
      style="display: flex; justify-content: space-between; align-items: center"
    >
      <h5>Image Adjust</h5>
      <div>
        <v-spacer></v-spacer>
        <v-btn class="pa-1" height="20" color="primary" small @click="onReset">
          Reset
        </v-btn>
      </div>
    </div>
    <v-container class="px-3 py-0" fluid>
      <v-col class="pa-0" cols="12">
        <v-slider
          v-model="brightness"
          prepend-icon="mdi-brightness-5"
          :min="-255"
          :max="255"
          :readonly="imageData.url == null"
          @end="onChangeB"
          dense
          hide-details
        >
          <template v-slot:append>
            <v-text-field
              v-model="brightness"
              class="ma-0 pa-0 no-underline"
              style="width: 40px; border"
              readonly
              dense
              hide-details
            ></v-text-field>
          </template>
        </v-slider>
      </v-col>

      <v-col class="pa-0" cols="12">
        <v-slider
          v-model="contrast"
          prepend-icon="mdi-circle-half-full"
          :min="-127"
          :max="127"
          :readonly="imageData.url == null"
          @end="onChangeC"
          dense
          hide-details
        >
          <template v-slot:append>
            <v-text-field
              v-model="contrast"
              class="ma-0 pa-0 no-underline"
              style="width: 40px; border"
              readonly
              dense
              hide-details
            ></v-text-field>
          </template>
        </v-slider>
      </v-col>

      <v-col class="pa-0" cols="12">
        <v-slider
          v-model="gamma"
          prepend-icon="mdi-weather-sunny"
          :min="0"
          :max="100"
          :readonly="imageData.url == null"
          @end="onChangeG"
          dense
          hide-details
        >
          <template v-slot:append>
            <v-text-field
              v-model="gamma"
              class="ma-0 pa-0 no-underline"
              style="width: 40px; border"
              readonly
              dense
              hide-details
            ></v-text-field>
          </template>
        </v-slider>
      </v-col>
    </v-container>
  </v-card>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  name: "ImageAdjust",

  components: {},

  data: () => ({
    brightness: 0,
    contrast: 0,
    gamma: 0,
  }),

  computed: {
    ...mapGetters("image", {
      imageData: "imageData",
    }),
  },

  created() {
    this.unwatch = this.$store.watch(
      (state, getters) => getters["image/imageParams"],
      (newValue) => {
        this.brightness = newValue.brightness;
        this.contrast = newValue.contrast;
        this.gamma = newValue.gamma;
      }
    );
  },

  methods: {
    onChangeB: function (b) {
      if (b !== this.$store.state.image.parameters.brightness)
        this.$store.dispatch("image/adjustImageByBrightness", b);
    },
    onChangeC: function (c) {
      if (c !== this.$store.state.image.parameters.contrast)
        this.$store.dispatch("image/adjustImageByContrast", c);
    },
    onChangeG: function (g) {
      if (g !== this.$store.state.image.parameters.gamma)
        this.$store.dispatch("image/adjustImageByGamma", g);
    },
    onReset: function () {
      this.$store.dispatch("image/resetAdjust");
    },
  },

  beforeDestroy() {
    this.unwatch();
  },
};
</script>

<style scoped>
.no-underline >>> .v-input__slot::before {
  border-style: none !important;
}
</style>
