<template>
  <v-card class="pa-1" flat>
    <div
      style="display: flex; justify-content: space-between; align-items: center"
    >
      <h5>Timeline</h5>
      <div>
        <v-spacer></v-spacer>
        <v-btn
          color="primary"
          width="30"
          height="30"
          icon
          dense
          @click="onRefresh"
        >
          <v-icon>mdi-refresh</v-icon>
        </v-btn>
        <v-btn
          color="primary"
          width="30"
          height="30"
          icon
          dense
          @click="onSetting"
        >
          <v-icon>mdi-cog</v-icon>
        </v-btn>
      </div>
    </div>
    <v-row class="pa-0 ma-0" justify="space-between">
      <v-btn color="primary" width="30" height="30" icon dense @click="onPlay">
        <v-icon>mdi-play</v-icon>
      </v-btn>
      <v-btn
        color="primary"
        style="margin-left: -6px"
        width="30"
        height="30"
        icon
        dense
        @click="onStop"
      >
        <v-icon>mdi-stop</v-icon>
      </v-btn>
      <v-btn
        color="primary"
        style="margin-left: -6px"
        width="30"
        height="30"
        icon
        dense
        @click="onRewind"
      >
        <v-icon>mdi-rewind</v-icon>
      </v-btn>
      <v-btn
        color="primary"
        style="margin-left: -6px"
        width="30"
        height="30"
        icon
        dense
        @click="onFForward"
      >
        <v-icon>mdi-fast-forward</v-icon>
      </v-btn>
      <v-slider
        v-model="t_value"
        class="ml-2"
        :min="t_min"
        :max="t_max"
        :readonly="t_max < 1"
        dense
        hide-details
        @end="changeSelectsByTimeline"
      ></v-slider>
    </v-row>
    <v-row
      class="pa-0 mr-2 my-0"
      style="margin-left: 120px"
      justify="space-between"
    >
      <!-- <input
        class="range-field"
        type="number"
        :value="t_range.min"
        disabled
        @input="onChangeTmin"
      />
      <input
        class="range-field"
        type="number"
        :value="t_range.max"
        disabled
        @input="onChangeTmax"
      /> -->
    </v-row>
  </v-card>
</template>

<script>
import { mapState, mapGetters, mapActions } from "vuex";

export default {
  name: "Timeline",

  components: {},

  data: () => ({
    t_value: 1
  }),

  created() {
    // this.changeParameterByT(this.t_min);
  },

  beforeDestroy() {
    // this.unwatch1();
    // this.unwatch2();
    // this.currentPageDataWatch();
  },

  computed: {
    ...mapGetters("files/position", {
      filesAtRowCol: "getFilesAtRowCol"
    }),

    t_max() {
      var rs = [0];
      if (this.filesAtRowCol) {
        for (let idx in this.filesAtRowCol) {
          let f = this.filesAtRowCol[idx];
          if (f.metaData) {
            rs.push(f.metaData.timeline);
          }
        }
        rs = Math.max(...rs);
      }
      return rs;
    },
    t_min() {
      var rs = [];
      if (this.filesAtRowCol) {
        for (let idx in this.filesAtRowCol) {
          let f = this.filesAtRowCol[idx];
          if (f.metaData) {
            rs.push(f.metaData.timeline);
          }
        }
        if (rs.length == 0) rs.push(0);
        rs = Math.min(...rs);
      }
      return rs;
    }
  },

  methods: {
    ...mapActions("files/position", {
      changeSelectsByTimeline: "changeSelectsByTimeline"
    }),
    onChangeTmin: function(event) {
      this.$forceUpdate();
    },
    onChangeTmax: function(event) {
      this.$forceUpdate();
    },
    onRefresh: function() {
      console.log("Refresh");
    },
    onSetting: function() {
      console.log("Setting");
    },
    onPlay: function() {
      console.log("Play");
    },
    onStop: function() {
      console.log("Stop");
    },
    onRewind: function() {
      console.log("Rewind");
    },
    onFForward: function() {
      console.log("FForward");
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
