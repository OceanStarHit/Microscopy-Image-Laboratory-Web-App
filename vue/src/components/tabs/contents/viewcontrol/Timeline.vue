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

  data(){
    return {
      t_value: 1,
      timeList: []
    }
  },

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
    ...mapState(['files']), // 获取图片状态

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
      if (this.timeList != undefined && this.timeList.length>0){
        this.changeSelectsByTimeline(this.timeList[0]);
      }
      console.log("Refresh");
    },
    onSetting: function() {
      console.log("Setting");
    },
     onPlay: async function() {
      let self = this;
      const filesInfo = this.files.position.files;
      // 得到时间轴列表
      var timeList = filesInfo.map(element=>{
        return element.metaData.timeline;
      });
      timeList.sort(); // 将时间轴排序，从小到大
      this.timeList = timeList;
      console.log('时间轴列表',timeList);
      // 半秒切换一次图片达到播放效果
        for ( var i = 0,l = timeList.length; i < l; i++ ){
          (function(i) {
              setTimeout(function() {
                  console.log('test',i);
                  self.changeSelectsByTimeline(i);
              }, (i + 1) * 500);
          })(i)
        }
      console.log(this.files.position.files);
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
