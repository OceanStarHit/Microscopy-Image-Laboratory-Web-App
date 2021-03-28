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
      prepend-icon="mdi-swap-vertical"
      v-model="z_value"
      :min="z_min"
      :max="z_max == 1 ? 2 : z_max"
      :readonly="z_max == 1"
      @end="onChangeZ"
      dense
      hide-details
    ></v-slider>
    <v-row class="pa-0 ml-10 mr-2 my-0" justify="space-between">
      <input
        class="range-field"
        type="number"
        :value="z_range.min"
        disabled
        @input="onChangeZmin"
      />
      <input
        class="range-field"
        type="number"
        :value="z_range.max"
        disabled
        @input="onChangeZmax"
      />
    </v-row>
  </v-card>
</template>

<script>
export default {
  name: "ZPosition",

  components: {},

  data: () => ({
    z_value: 1,
    z_min: 1,
    z_max: 1,
    z_range: {
      min: 1,
      max: 1,
    },
  }),

  created() {
    this.unwatch1 = this.$store.watch(
      (state, getters) => getters["image/sizeZ"],
      (newValue) => {
        console.log(newValue);
        // this.z_min = 1;
        // this.z_max = newValue;

        // this.z_range.min = 1;
        // this.z_range.max = this.z_max;
      }
    );
    this.unwatch2 = this.$store.watch(
      (state, getters) => getters["image/imageParams"],
      (newValue) => {
        console.log(newValue);
        // this.z_value = newValue.Z;
      }
    );

    this.currentPageDataWatch = this.$store.watch(
      (state, getters) => getters["image/currentPageInfo"],
      (info) => {
        if (info.pageData.length == 1) {
          this.z_max = info.pageData[0].metadata.coreMetadata.sizeZ;
          this.z_range.max = this.z_max;
          this.z_value = info.pageData[0].metadata.imageInfo.pixels.sizeZ;
        } else {
          let zMax = 0;
          info.pageData.forEach((data, idx) => {
            const types = data.filename.match(
              /^(\w+)[_\s](\w+_\w+)_(\w\d{2})_(\d)_(\w)(\d{2})(\w\d{2})(\w\d)\.(\w+)$/
            );
            if (types) {
              if (zMax < types[4]) {
                zMax = types[4];
              }
              if (idx == info.pageData.dataIndex) {
                this.z_value = types[4];
              }
            }
          });

          this.z_max = zMax + 1;
          this.z_range.max = this.z_max;
        }
      }
    );
  },

  beforeDestroy() {
    this.unwatch1();
    this.unwatch2();
    this.currentPageDataWatch();
  },

  methods: {
    onChangeZ: function (z) {
      if (z !== this.$store.state.image.parameters.Z)
        this.$store.dispatch("image/changeParameterByZ", z);
    },
    onChangeZmin: function (event) {
      const z_min = event.target.value;

      if (!(z_min < 1 || z_min > this.z_range.max)) {
        this.z_range.min = z_min;

        if (this.z_value < z_min) {
          this.z_value = z_min;
          this.onChangeZ(this.z_value);
        }
      }

      this.$forceUpdate();
    },
    onChangeZmax: function (event) {
      const z_max = event.target.value;

      if (!(z_max > this.z_max || z_max < this.z_range.min)) {
        this.z_range.max = z_max;

        if (this.z_value > z_max) {
          this.z_value = z_max;
          this.onChangeZ(this.z_value);
        }
      }

      this.$forceUpdate();
    },
    on3DView: function () {
      console.log("3D View");
    },
  },
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
</style>
