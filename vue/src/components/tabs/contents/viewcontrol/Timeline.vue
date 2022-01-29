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
        @end="changeSelectsByTimeline(timeList[t_value])"
      ></v-slider>
    </v-row>
    <v-row
      class="pa-0 ml-10 mr-2 my-0" justify="space-between"
    >
      <input
        class="range-field"
        type="number"
        :value="t_min"
        disabled
        @input="onChangeTmin"
      />
      <input
        class="range-field"
        type="number"
        :value="t_max"
        disabled
        @input="onChangeTmax"
      />
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
      t_value: 0, // 滑轮绑定的时间点
      timeList: [],
      timer: null, // 播放暂停使用
      continuePointIdx: 0, // 继续播放时间点下标
    }
  },

  created() {
    // this.changeParameterByT(this.t_min);

  },

  mounted() {

  },
  beforeDestroy() {
    // this.unwatch1();
    // this.unwatch2();
    // this.currentPageDataWatch();
  },

  computed: {
    ...mapGetters("files/position", { // 获取图片状态
      filesAtRowCol: "getFilesRowCol"
    }),
    ...mapState(['files']), // 获取图片状态

    t_max() {
      var length = 1;
      var rs = [];
      // if (this.timeList.length != 0) { // 如果存在图片
        for (let idx in this.filesAtRowCol) {
          let f = this.filesAtRowCol[idx];
          if (f.metaData) {
            rs.push(f.metaData.timeline);
          }
        }
        // var length = rs.length-1;
        // console.log('timeline value:',this.t_value);
        // console.log("timeline lenth:",String(length));
      // }
      return length;
    },
    t_min() {
      return 1;
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
      this.t_value = 0;
      this.continuePointIdx = 0;
      if (this.timeList != undefined && this.timeList.length>0){
        this.changeSelectsByTimeline(this.timeList[0]);
      }
      console.log("Refresh");
    },
    onSetting: function() {
      console.log("Setting");
    },
    getTimeList: function() { // 获得时间轴
      const filesInfo = this.files.position.files;
      // 得到时间轴列表
      var timeList = filesInfo.map(element=>{
        return element.metaData.timeline;
      });
      timeList.sort(); // 将时间轴排序，从小到大
      this.timeList = timeList;
      console.log('timeList', timeList);
      return timeList;
    },

    onPlay: async function() {
      let self = this;
      var timeList = this.getTimeList();
      // 开始播放
      var nowTimePointIdx = this.continuePointIdx;
      var timeIdx = timeList.length-1; // 计算时间轴最大下标值
      console.log('timeIdx',timeIdx);
      this.timer = setInterval(function () {
        if (nowTimePointIdx < timeIdx){

          nowTimePointIdx ++;
          self.t_value ++;
          self.continuePointIdx = nowTimePointIdx; // 记录继续进度
          self.changeSelectsByTimeline(timeList[nowTimePointIdx]);
        }else{
          clearInterval(self.timer); // 播放完成之后停止循环
        }

      },500);


      // // 半秒切换一次图片达到播放效果
      //   for ( var i = 0,l = timeList.length; i < l; i++ ){
      //     (function(i) {
      //         setTimeout(function() {
      //             console.log('test',i);
      //             self.t_value = i;
      //             self.changeSelectsByTimeline(timeList[i]);
      //         }, (i + 1) * 500);
      //     })(i)
      //   }
      console.log(this.files.position.files);
      console.log("Play");
    },


    onStop: function() {
      clearInterval(this.timer);
      console.log("Stop");
    },
    onRewind: function() { // 向前一张
      if (this.continuePointIdx>0){
          this.continuePointIdx --; // 当前时间点索引减一
      }
      this.changeSelectsByTimeline(this.timeList[this.continuePointIdx]);
      if (this.t_value > 0){
        this.t_value --;
      }
      console.log("Rewind");
    },
    onFForward: function() { // 向后一张
      var length = this.timeList.length-1;
      console.log("length",length);
      if (this.continuePointIdx < length){
        this.continuePointIdx ++; // 当前时间点索引加一
      }
      console.log("this.continuePointIdx",this.continuePointIdx)
      this.changeSelectsByTimeline(this.timeList[this.continuePointIdx]);
      if (this.t_value < length){
        this.t_value ++;
      }
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
