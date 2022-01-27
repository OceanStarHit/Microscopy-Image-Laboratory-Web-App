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
      :min="z_min"
      :max="z_max"
      dense
      hide-details
      @end="changeSelectsByZ"
    ></v-slider>
    <v-row class="pa-0 ml-10 mr-2 my-0" justify="space-between">
      <input
        class="range-field"
        type="number"
        :value="z_min"
        disabled
        @input="onChangeZmin"
      />
      <input
        class="range-field"
        type="number"
        :value="z_max"
        disabled
        @input="onChangeZmax"
      />
    </v-row>
  </v-card>
</template>

<script>
import { mapState, mapGetters, mapActions } from "vuex";

export default {
  name: "ZPosition",

  components: {},

  computed: {
    ...mapGetters("files/position", {
      filesAtRowCol: "getFilesRowCol",
      filesCount:"getFilesUpdatedCount"
    }),
    z_max() {
      var rs = [0];
      if (this.filesAtRowCol) {
        for (let idx in this.filesAtRowCol) {
          let f = this.filesAtRowCol[idx];
          if (f.metaData) {
            rs.push(f.metaData.z);
          }
        }
        rs = Math.max(...rs);
      }
      console.log("max"+rs);
      return rs;
    },
    z_min() {
      var rs = [0];
      if (this.filesAtRowCol) {
        for (let idx in this.filesAtRowCol) {
          let f = this.filesAtRowCol[idx];
          if (f.metaData) {
            rs.push(f.metaData.z);
          }
        }
        if (rs.length == 0) rs.push(0);
        rs = Math.min(...rs);
      }
      console.log("z_min"+rs);
      return rs;
    }
  },

  data: () => ({
    z_value: 1
  }),

  created() {},
  beforeDestroy() {},

  methods: {
    ...mapActions("files/position", {
      changeSelectsByZ: "changeSelectsByZ"
    }),
    onChangeZmin: function(event) {
      this.$forceUpdate();
    },
    onChangeZmax: function(event) {
      this.$forceUpdate();
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
</style>
