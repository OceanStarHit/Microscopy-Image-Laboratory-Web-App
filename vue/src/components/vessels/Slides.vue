<template>
  <v-row
    v-if="count < 3"
    class="flex-column justify-space-around px-3 my-1"
    :width="rect.width"
    :style="{
      height: rect.height + 'px',
    }"
  >
    <div
      class="d-flex justify-center"
      v-for="i in count"
      :key="i"
      :ripple="interaction"
      @click="clicked(i)"
    >
      <v-sheet
        class="slide-box-left"
        :width="slide.width / 4"
        :height="slide.height"
      ></v-sheet>
      <v-sheet
        class="slide-box-right"
        :class="
          check
            ? activeSlides.indexOf(i) > -1
              ? selectedSlide === i
                ? 'selected'
                : 'active'
              : ''
            : selectedSlide === i
            ? 'selected'
            : ''
        "
        :width="(slide.width / 4) * 3"
        :height="slide.height"
      >
        <div v-if="showNumber" class="body-1 primary--text">
          {{ i }}
        </div>
      </v-sheet>
    </div>
  </v-row>
  <v-row v-else class="justify-space-around px-3 my-1" :width="rect.width">
    <div v-for="i in count" :key="i" :ripple="interaction" @click="clicked(i)">
      <v-sheet
        class="slide-box-top"
        :width="slide.width"
        :height="slide.height / 4"
      ></v-sheet>
      <v-sheet
        class="slide-box-bottom"
        :class="
          check
            ? activeSlides.indexOf(i) > -1
              ? selectedSlide === i
                ? 'selected'
                : 'active'
              : ''
            : selectedSlide === i
            ? 'selected'
            : ''
        "
        :width="slide.width"
        :height="(slide.height / 4) * 3"
      >
        <div v-if="showNumber" class="body-1 primary--text">
          {{ i }}
        </div>
      </v-sheet>
    </div>
  </v-row>
</template>

<script>
import { mapState } from "vuex";

const H_RATIO = 0.6;
const V_RATIO = 0.5;
const MAX_HEIGHT = 1000;

export default {
  name: "Slide",

  components: {},

  props: {
    count: {
      type: Number,
      default: 1,
    },
    width: {
      type: Number,
      default: 0,
    },
    showNumber: {
      type: Boolean,
      default: false,
    },
    actives: {
      type: Array,
      default: () => [],
    },
    selected: {
      type: Number,
      default: -1,
    },
    check: {
      type: Boolean,
      default: true,
    },
    interaction: {
      type: Boolean,
      default: true,
    },
  },

  data: function () {
    return {
      rect: {
        width: 0,
        height: 0,
      },
      slide: {
        width: 0,
        height: 0,
      },
      selectedSlide: this.selected,
      activeSlides: this.actives,
    };
  },

  watch: {
    count: {
      handler() {
        this.resize();
        this.selectedSlide = -1;
        this.setActivate();
      },
      deep: true,
      immediate: true,
    },
    width: {
      handler() {
        this.resize();
      },
      deep: true,
      immediate: true,
    },
    "$store.state.vessel.currentVesselId": {
      handler() {
        this.setActivate();
      },
      deep: true,
      immediate: true,
    },
  },

  computed: {
    ...mapState({
      allIndice: (state) => state.image.allIndice,
      curPageIdx: (state) => state.image.curPageIdx,
    }),
  },

  methods: {
    resize: function () {
      if (this.count < 3) {
        if (this.width * H_RATIO > MAX_HEIGHT) {
          this.rect.height = MAX_HEIGHT;
          this.rect.width = this.height / H_RATIO;
        } else {
          this.rect.width = this.width - 40;
          this.rect.height = this.width * H_RATIO;
        }

        this.slide.width = this.rect.width;

        const MAX_HEIGHT = this.rect.height / 3;

        const one_height =
          (this.rect.height - (this.count - 1) * 20) / this.count;
        if (one_height > MAX_HEIGHT) {
          this.slide.height = MAX_HEIGHT;
        } else {
          this.slide.height = one_height;
        }
      } else {
        if (this.width * V_RATIO > MAX_HEIGHT) {
          this.rect.height = MAX_HEIGHT;
          this.rect.width = this.height / V_RATIO;
        } else {
          this.rect.width = this.width;
          this.rect.height = this.width * V_RATIO;
        }

        this.slide.height = this.rect.height;

        const MAX_WIDTH = this.slide.height / 3;

        const one_width =
          (this.rect.width - (this.count - 1) * 20) / this.count;
        if (one_width > MAX_WIDTH) {
          this.slide.width = MAX_WIDTH;
        } else {
          this.slide.width = one_width;
        }
      }
    },

    clicked: function (slideNo) {
      if (!this.interaction) return;

      if (this.check) {
        const pos = this.activeSlides.indexOf(slideNo);
        if (pos > -1) {
          this.selectedSlide = slideNo;
          // this.$emit("click", slideNo);

          const data = this.$store.getters["image/currentPageInfo"];
          if (
            !data ||
            data.pageData == undefined ||
            data.dataIndex == undefined ||
            data.pageData.length < slideNo
          ) {
            return;
          }

          if (this.allIndice[this.curPageIdx] != slideNo) {
            this.$store.dispatch("image/changeCurrentData", slideNo);
          }
        }
      } else {
        this.selectedSlide = slideNo;
        this.$emit("click", slideNo);
      }
    },

    setActivate() {
      this.activeSlides = [];

      const data = this.$store.getters["image/currentPageInfo"];
      if (!data || data.pageData == undefined || data.dataIndex == undefined) {
        return;
      }

      const cnt = data.pageData.length;
      for (let idx = 1; idx <= cnt; idx++) {
        this.activeSlides.push(idx);

        if (idx == data.dataIndex + 1) {
          this.selectedSlide = idx;
        }
      }
    },
  },
};
</script>

<style scoped>
.slide-box-left {
  border: 2px solid black !important;
  border-right-width: 1px !important;
}
.slide-box-right {
  border: 2px solid black !important;
  border-left-width: 1px !important;
  display: flex;
  align-items: center;
  justify-content: center;
}
.slide-box-top {
  border: 2px solid black !important;
  border-bottom-width: 1px !important;
}
.slide-box-bottom {
  border: 2px solid black !important;
  border-top-width: 1px !important;
  display: flex;
  align-items: center;
  justify-content: center;
}
.slide-box-right.active,
.slide-box-bottom.active {
  background-color: cyan !important;
}
.slide-box-right.selected,
.slide-box-bottom.selected {
  background-color: magenta !important;
}
</style>
