<template>
  <tab-item title="View">
    <Vessel />
    <v-divider />
    <Objective />
    <v-divider />
    <Channel />
    <div>
      <v-divider />
      <ZPosition />
    </div>
    <div>
      <v-divider />
      <Timeline />
    </div>
  </tab-item>
</template>

<script>
import { mapGetters, mapState } from 'vuex';

import TabItem from '../custom/TabItem';
import Vessel from '../tabs/contents/viewcontrol/Vessel';
import Objective from '../tabs/contents/viewcontrol/Objective';
import Channel from '../tabs/contents/viewcontrol/Channel';
// import ImageSeries from "./contents/viewcontrol/ImageSeries";
import ZPosition from '../tabs/contents/viewcontrol/ZPosition';
import Timeline from '../tabs/contents/viewcontrol/Timeline';

export default {
  name: 'OpenPositionViewTab',

  components: {
    TabItem,
    Vessel,
    Objective,
    Channel,
    ZPosition,
    Timeline
  },

  data: () => ({
    totalPageCnt: 0,
    curPageIdx: 0
  }),

  created() {
    this.curPageIdxWatch = this.$store.watch(
      (state, getters) => getters['image/currentPageIndex'],
      res => {
        this.curPageIdx = res;
      }
    );
  },

  beforeDestroy() {
    this.curPageIdxWatch();
  },

  computed: {
    ...mapGetters('image', {
      seriesCount: 'seriesCount',
      selectedImagesAtRowCol: 'selectedImagesAtRowCol'
    }),
    ...mapState({
      allData: state => state.image.allData
    }),
    sizeZ: function() {
      let zs = this.selectedImagesAtRowCol.map(img => img.extParams.z);
      zs = [...new Set(zs)];
      return zs.length;
    },
    sizeT: function() {
      let ts = this.selectedImagesAtRowCol.map(img => img.extParams.timeline);
      ts = [...new Set(ts)];
      return ts.length;
    }
  },
  methods: {
    handlePageChange(idx) {}
  }
};
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
