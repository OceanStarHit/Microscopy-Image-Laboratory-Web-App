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
        :readonly="t_max == 1"
        dense
        hide-details
        @end="changeParameterByT"
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
    this.changeParameterByT(this.t_min);
  },

  beforeDestroy() {
    // this.unwatch1();
    // this.unwatch2();
    // this.currentPageDataWatch();
  },

  computed: {
    ...mapGetters("image", {
      selectedImagesAtRowCol: "selectedImagesAtRowCol"
    }),

    t_max() {
      var rs = 0
      if(this.selectedImagesAtRowCol) {
        let zs = this.selectedImagesAtRowCol.map(img => img.extParams.timeline);
        console.log(zs);
        if(zs.length == 0) {
          return 0;
        }
        
        rs = Math.max(...zs);
      }
      return rs;
    },
    t_min() {
      var rs = 0;
      if(this.selectedImagesAtRowCol) {
        let zs = this.selectedImagesAtRowCol.map(img => img.extParams.timeline);
        if(zs.length == 0) {
          return 0;
        }
        
        rs = Math.min(...zs);
      }
      return rs;
    }
  },

  methods: {
    ...mapActions("image", {
      changeParameterByT: "changeParameterByT"
    }),
    // onChangeT: function(t) {
    //   if (t !== this.$store.state.image.parameters.T)
    //     this.$store.dispatch("image/changeParameterByT", t);
    // },
    onChangeTmin: function(event) {
      // const t_min = event.target.value;

      // if (!(t_min < 1 || t_min > this.t_range.max)) {
      //   this.t_range.min = t_min;

      //   if (this.t_value < t_min) {
      //     this.t_value = t_min;
      //     this.onChangeT(this.t_value);
      //   }
      // }

      this.$forceUpdate();
    },
    onChangeTmax: function(event) {
      // const t_max = event.target.value;

      // if (!(t_max > this.t_max || t_max < this.t_range.min)) {
      //   this.t_range.max = t_max;

      //   if (this.t_value > t_max) {
      //     this.t_value = t_max;
      //     this.onChangeT(this.t_value);
      //   }
      // }

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
