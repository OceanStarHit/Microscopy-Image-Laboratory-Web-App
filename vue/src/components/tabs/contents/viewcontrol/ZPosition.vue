<template>
  <v-card class="pa-1" flat>
    <div
      style="display: flex; justify-content: space-between; align-items: center"
    >
      <h5>Z Position</h5>
      <div>
        <v-spacer></v-spacer>
        <v-btn class="pa-1" height="20" color="primary" small @click="on3DView">
          3-D View
        </v-btn>
      </div>
    </div>
    <v-slider
      v-model="z_value"
      prepend-icon="mdi-swap-vertical"
      onscroll="myScroll()"
      :min="z_min"
      :max="z_max"
      :readonly="z_max == 1"
      dense
      hide-details
      @end="changeSelectsByZ"
    >
      <template v-slot:append>
        <v-text-field
          v-model="z_value"
          class="ma-0 pa-0 no-underline"
          style="width: 20px; border"
          readonly
          dense
          hide-details
        ></v-text-field>
      </template>
    </v-slider>
  </v-card>
</template>

<script>
import { mapState, mapGetters, mapActions } from "vuex";

export default {
  name: "ZPosition",

  components: {},

  computed: {
    ...mapGetters("files/position", {
      filesAtRowCol: "getFilesAtRowCol"
    }),
    z_max() {
      var rs = this.$store.state.image.image_num;
      return rs;
    },
    z_min() {
      return 1;
    }
  },

  data: () => ({
    z_value: 1,
  }),

  created() {
    this.unwatch = this.$store.watch(
      (state, getters) => getters["files/position/getchangedz"],
      newValue => {
        this.z_value = newValue + 1;
      }
    );
  },
  beforeDestroy() {},
  methods: {
    ...mapActions("files/position", {
      changeSelectsByZ: "changeSelectsByZ"
    }),
    
    myScroll: function() {
      this.z_value++;
    },
    on3DView: function() {
      console.log("3D View");
    }
  }
};
</script>

<style scoped>
.range-field {
  width: 48px;
  border: 2px solid #1976d2;
  border-radius: 4px;
  padding-left: 2px;
}

.range-field.disabled {
  border-color: #9e9e9e;
}

.no-underline >>> .v-input__slot::before {
  border-style: none !important;
}
</style>
