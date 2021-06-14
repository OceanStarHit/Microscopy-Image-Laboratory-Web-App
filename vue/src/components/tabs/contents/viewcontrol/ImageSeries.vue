<template>
  <v-card class="pa-2" flat>
    <h4>Series</h4>
    <v-slider
      class="mt-12"
      v-model="s_value"
      prepend-icon="mdi-image-text"
      :min="1"
      :max="s_max == 1 ? 10 : s_max"
      :readonly="s_max == 1"
      thumb-label="always"
      ticks="always"
      tick-size="2"
      @end="onChange"
    ></v-slider>
  </v-card>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  name: "ImageSeries",

  components: {},

  data: () => ({
    s_value: 1,
  }),

  computed: {
    ...mapGetters("image", {
      s_max: "seriesCount",
    }),
  },

  created() {
    this.unwatch = this.$store.watch(
      (state, getters) => getters["image/imageId"],
      (newValue) => (this.s_value = newValue + 1)
    );
  },

  methods: {
    onChange: function (s) {
      if (s !== this.$store.state.image.imageId + 1)
        this.$store.dispatch("image/changeImage", s);
    },
  },

  beforeDestroy() {
    this.unwatch();
  },
};
</script>
