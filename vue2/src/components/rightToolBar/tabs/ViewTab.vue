<template>
  <tab-item title="View">
    <v-row justify="center">
      <v-container class="max-width pagination">
        <v-pagination
          v-model="currentPageIndex"
          class="my-4 pagination"
          total-visible="5"
          :length="allData.length"
          @input="onPageChange"
        />
      </v-container>
    </v-row>
    <v-divider />
    <Vessel />
    <v-divider />
    <Objective />
    <v-divider />
    <Channel />
    <v-divider />
    <ImageAdjust />
    <!--        &lt;!&ndash; <div v-if="seriesCount > 1">-->
    <!--    <v-divider />-->
    <!--    <ImageSeries />-->
    <!--        </div> &ndash;&gt;-->
    <!--    <div>-->
    <v-divider />
    <ZPosition />
    <!--    </div>-->
    <!--    <div>-->
    <v-divider />
    <Timeline />
    <!--    </div>-->
  </tab-item>
</template>

<script lang="ts">
import Component from 'vue-class-component';
import Vue from 'vue';

import TabItem from '../../custom/TabItem.vue';
import Vessel from '../../tabs/contents/viewcontrol/Vessel.vue';
import Objective from '../../tabs/contents/viewcontrol/Objective.vue';
import Channel from '../../tabs/contents/viewcontrol/Channel.vue';
import ImageAdjust from '../../tabs/contents/viewcontrol/ImageAdjust.vue';
// import ImageSeries from "./contents/viewcontrol/ImageSeries.vue";
import ZPosition from '../../tabs/contents/viewcontrol/ZPosition.vue';
import Timeline from '../../tabs/contents/viewcontrol/Timeline.vue';

@Component({
  components: {
    TabItem,
    Vessel,
    Objective,
    Channel,
    ImageAdjust,
    // ImageSeries,
    ZPosition,
    Timeline
  }
})
export default class ViewTab extends Vue {
  totalPageCount = 0;
  curPageIndex = 0;

  get currentPageIndex(): number {
    return this.$store.state.image.currentPageIndex;
  }

  set currentPageIndex(index: number) {
    this.$store.state.image.currentPageIndex = index;
  }

  get allData(): any {
    return this.$store.state.image.allData;
  }

  get sizeZ(): number {
    return this.$store.state.image.allData;
  }

  onPageChange(index: number) {
    this.$store.dispatch('image/changeCurrentPage', index);
  }


}
</script>

<style scoped>
.pagination {
  padding: 0px !important;
}
.pagination >>> button {
  width: 24px;
  height: 24px;
  min-width: 24px;
}
</style>
