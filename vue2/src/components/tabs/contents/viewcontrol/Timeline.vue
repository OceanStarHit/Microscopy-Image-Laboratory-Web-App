<template>
  <v-card class="pa-1" flat>
    <div
      style="display: flex; justify-content: space-between; align-items: center"
    >
      <h5>Timeline</h5>
      <!--      <div>-->
      <!--        <v-spacer />-->
      <!--        <v-btn-->
      <!--          color="primary"-->
      <!--          width="30"-->
      <!--          height="30"-->
      <!--          icon-->
      <!--          dense-->
      <!--          @click="onRefresh"-->
      <!--        >-->
      <!--          <v-icon>mdi-refresh</v-icon>-->
      <!--        </v-btn>-->
      <!--        <v-btn-->
      <!--          color="primary"-->
      <!--          width="30"-->
      <!--          height="30"-->
      <!--          icon-->
      <!--          dense-->
      <!--          @click="onSetting"-->
      <!--        >-->
      <!--          <v-icon>mdi-cog</v-icon>-->
      <!--        </v-btn>-->
      <!--      </div>-->
      <!--    </div>-->
      <!--    <v-row class="pa-0 ma-0" justify="space-between">-->
      <!--      <v-btn-->
      <!--        color="primary"-->
      <!--        width="30"-->
      <!--        height="30"-->
      <!--        icon-->
      <!--        dense-->
      <!--        @click="onPlay"-->
      <!--      >-->
      <!--        <v-icon>mdi-play</v-icon>-->
      <!--      </v-btn>-->
      <!--      <v-btn-->
      <!--        color="primary"-->
      <!--        style="margin-left: -6px"-->
      <!--        width="30"-->
      <!--        height="30"-->
      <!--        icon-->
      <!--        dense-->
      <!--        @click="onStop"-->
      <!--      >-->
      <!--        <v-icon>mdi-stop</v-icon>-->
      <!--      </v-btn>-->
      <!--      <v-btn-->
      <!--        color="primary"-->
      <!--        style="margin-left: -6px"-->
      <!--        width="30"-->
      <!--        height="30"-->
      <!--        icon-->
      <!--        dense-->
      <!--        @click="onRewind"-->
      <!--      >-->
      <!--        <v-icon>mdi-rewind</v-icon>-->
      <!--      </v-btn>-->
      <!--      <v-btn-->
      <!--        color="primary"-->
      <!--        style="margin-left: -6px"-->
      <!--        width="30"-->
      <!--        height="30"-->
      <!--        icon-->
      <!--        dense-->
      <!--        @click="onFForward"-->
      <!--      >-->
      <!--        <v-icon>mdi-fast-forward</v-icon>-->
      <!--      </v-btn>-->
      <!--      <v-slider-->
      <!--        v-model="selectedZValue"-->
      <!--        class="ml-2"-->
      <!--        :min="timeMinIndex"-->
      <!--        :max="timeMaxIndex"-->
      <!--        :readonly="timeMaxIndex < 1"-->
      <!--        dense-->
      <!--        hide-details-->
      <!--      />-->
      <!--      &lt;!&ndash;      @end="changeSelectsByTimeline(timeList[t_value])"&ndash;&gt;-->
      <!--      &lt;!&ndash;      ></v-slider>&ndash;&gt;-->
      <!--    </v-row>-->
      <!--    <v-row-->
      <!--      class="pa-0 mr-2 my-0"-->
      <!--      style="margin-left: 120px"-->
      <!--      justify="space-between"-->
      <!--    >-->
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
      <!--    </v-row>-->
    </div>
  </v-card>
</template>

<script lang="ts">
import Component from 'vue-class-component';
import Vue from 'vue';
import {TileModel} from '@/store/tiles.module';

@Component({})
export default class Timeline extends Vue {

  timeList: number[] = [];
  timer = 0;
  continuePointIndex = 0;

  /* GET | SET */
  get selectedZValue(): number {
    return this.$store.state.tiles.selection.zIndex;
  }

  set selectedZValue(timeIndex: number) {
    this.$store.commit('tiles/addSelection', {timeIndex: timeIndex})
  }

  get tilesAtRowAndColumnSelection(): TileModel[] {
    return this.$store.getters['tiles/getTilesAtRowAndColumnSelection'];
  }

  get timeMaxIndex(): number {
    return this.$store.getters['tiles/getMaxTimeIndex'];
  }

  get timeMinIndex(): number {
    return this.$store.getters['tiles/getMinTimeIndex'];
  }


  onRefresh() {
    this.selectedZValue = 0;
    this.continuePointIndex = 0;
    if (this.timeList.length > 0){
      this.selectedZValue = this.timeList[0];
    }
    console.log('Refresh');
  }

  onSetting() {
    console.log('Setting');
  }

  getTimeIndices() {
    return this.$store.state.tiles.tiles
        .filter((tile: TileModel) => 'timeIndex' in tile)
        .map((tile: TileModel) => tile.timeIndex)
        .sort()
  }

  async onPlay() {
    // eslint-disable-next-line @typescript-eslint/no-this-alias
    const self = this;
    const timeIndices = this.getTimeIndices();

    let currentTimeIndex = this.continuePointIndex;
    const timeIndex = timeIndices.length-1; // 计算时间轴最大下标值
    console.log('timeIndex', timeIndex);
    this.timer = setInterval(function () {
      if (currentTimeIndex < timeIndex){

        currentTimeIndex ++;
        self.selectedZValue ++;
        self.continuePointIndex = currentTimeIndex; // 记录继续进度
        self.selectedZValue = timeIndices[currentTimeIndex];
      }else{
        console.log('播放结束');
        clearInterval(self.timer); // 播放完成之后停止循环
      }

    },500);

    console.log('Play');
  }
  //
  // methods: {
  //   ...mapActions("files/position", {
  //     changeSelectsByTimeline: "changeSelectsByTimeline"
  //   }),
  //   onChangeTmin: function(event) {
  //     this.$forceUpdate();
  //   },
  //   onChangeTmax: function(event) {
  //     this.$forceUpdate();
  //   },
  //   onRefresh: function() {
  //     this.t_value = 0;
  //     this.continuePointIdx = 0;
  //     if (this.timeList != undefined && this.timeList.length>0){
  //       this.changeSelectsByTimeline(this.timeList[0]);
  //     }
  //     console.log("Refresh");
  //   },
  //   onSetting: function() {
  //     console.log("Setting");
  //   },
  //   getTimeList: function() { // 获得时间轴
  //     const filesInfo = this.files.position.files;
  //     // 得到时间轴列表
  //     var timeList = filesInfo.map(element=>{
  //       return element.metaData.timeline;
  //     });
  //     timeList.sort(); // 将时间轴排序，从小到大
  //     this.timeList = timeList;
  //     console.log('时间轴列表', timeList);
  //     return timeList;
  //   },
  //
  //   onPlay: async function() {
  //     let self = this;
  //     var timeList = this.getTimeList();
  //     // 开始播放
  //     var nowTimePointIdx = this.continuePointIdx;
  //     var timeIdx = timeList.length-1; // 计算时间轴最大下标值
  //     console.log('timeIdx',timeIdx);
  //     this.timer = setInterval(function () {
  //       if (nowTimePointIdx < timeIdx){
  //
  //         nowTimePointIdx ++;
  //         self.t_value ++;
  //         self.continuePointIdx = nowTimePointIdx; // 记录继续进度
  //         self.changeSelectsByTimeline(timeList[nowTimePointIdx]);
  //       }else{
  //         console.log("播放结束");
  //         clearInterval(self.timer); // 播放完成之后停止循环
  //       }
  //
  //     },500);
  //
  //
  //     // // 半秒切换一次图片达到播放效果
  //     //   for ( var i = 0,l = timeList.length; i < l; i++ ){
  //     //     (function(i) {
  //     //         setTimeout(function() {
  //     //             console.log('test',i);
  //     //             self.t_value = i;
  //     //             self.changeSelectsByTimeline(timeList[i]);
  //     //         }, (i + 1) * 500);
  //     //     })(i)
  //     //   }
  //     console.log(this.files.position.files);
  //     console.log("Play");
  //   },
  //
  //
  //   onStop: function() {
  //     clearInterval(this.timer);
  //     console.log("Stop");
  //   },
  //   onRewind: function() { // 向前一张
  //     if (this.continuePointIdx>0){
  //         this.continuePointIdx --; // 当前时间点索引减一
  //     }
  //     this.changeSelectsByTimeline(this.timeList[this.continuePointIdx]);
  //     if (this.t_value > 0){
  //       this.t_value --;
  //     }
  //     console.log("Rewind");
  //   },
  //   onFForward: function() { // 向后一张
  //     var length = this.timeList.length-1;
  //     console.log("length",length);
  //     if (this.continuePointIdx < length){
  //       this.continuePointIdx ++; // 当前时间点索引加一
  //     }
  //     console.log("this.continuePointIdx",this.continuePointIdx)
  //     this.changeSelectsByTimeline(this.timeList[this.continuePointIdx]);
  //     if (this.t_value < length){
  //       this.t_value ++;
  //     }
  //     console.log("FForward");
  //   }
  // }
}
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
