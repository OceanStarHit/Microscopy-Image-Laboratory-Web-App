<template>
  <div
    class="scroll-slider"
    :class="[`slider-${direction}`]"
    id="scroll-slider"
    ref="slider"
  >
    <div
      class="scroll-slider-bar"
      :class="[`slider-bar-${direction}`]"
      :style="{
        top: topValue ? `${topValue}%` : '',
        left: leftValue ? `${leftValue}%` : '',
        width: direction === 'row' ? barLength + '%' : '',
        height: direction === 'col' ? barLength + '%' : ''
      }"
      ref="bar"
    ></div>
  </div>
</template>

<script>
export default {
  name: "ScrollBar",
  props: {
    direction: {
      type: String,
      default: "row"
    },
    total: {
      type: Number,
      default: 100
    },
    value: {
      type: Number,
      required: true
    },
    top: {
      type: Number,
      default: 0
    },
    left: {
      type: Number,
      default: 0
    }
  },
  model: {
    prop: "value",
    event: "change"
  },
  computed: {
    topValue() {
      return (Math.abs(this.top) / this.total) * 100;
    },
    leftValue() {
      return (Math.abs(this.left) / this.total) * 100;
    },
    barLength() {
      return (this.value / this.total) * 100;
    }
  },
  watch: {
    barLength() {
      console.log("Bar Length = ", this.barLength);
    },
    value(newValue) {
      this.setValue(newValue);
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.initInstance();
    });
  },
  beforeDestroy() {},
  methods: {
    setValue(value) {
      this.direction === "row" ? (this.left = value) : (this.top = value);
    },
    destroyEvent() {
      if (this.bar) {
        this.bar.removeEventListener("mousedown");
        this.bar.removeEventListener("mousemove");
        this.bar.removeEventListener("mouseleave");
        this.bar.removeEventListener("mouseup");
      }
    },
    initInstance() {
      const { bar, slider } = this.$refs;
      this.bar = bar;
      this.slider = slider;
      // 监听bar的点击及拖动事件
      document.addEventListener("mousedown", this.onMouseDown);
      document.addEventListener("mousemove", this.onMouseScroll);
      document.addEventListener("mouseleave", this.onMouseLeave);
      document.addEventListener("mouseup", this.onMouseUp);
      // The starting offset
      this.offset =
        this.direction === "row" ? this.bar.offsetLeft : this.bar.offsetTop;
    },
    onMouseDown(e) {
      if (e.target !== this.bar) return;
      this.isMoving = true;
      const event = e || window.event;
      // Starting position x when the direction is row, other y
      this.start =
        this.direction === "row"
          ? event.clientX - this.bar.offsetLeft
          : event.clientY - this.bar.offsetTop;
    },
    onMouseScroll: function(event) {
      if (!this.isMoving) return;
      // if (this.throttleTime && Date.now() - this.throttleTime < 3) return;
      this.throttleTime = Date.now();
      const e = event || window.event;
      let offset =
        this.direction === "row"
          ? e.clientX - this.start
          : e.clientY - this.start;
      const gap =
        this.direction === "row"
          ? this.slider.offsetWidth - this.bar.offsetWidth
          : this.slider.offsetHeight - this.bar.offsetHeight;
      if (offset < 0) {
        offset = 0;
      }
      if (offset > gap) {
        offset = gap;
      }
      const changeRate =
        this.direction === "row"
          ? offset / this.slider.offsetWidth
          : offset / this.slider.offsetHeight;
      this.$emit("change", changeRate * this.total);
    },
    onMouseUp(e) {
      if (!this.isMoving) return;
      this.isMoving = false;
      this.start = undefined;
    },
    onMouseLeave(e) {
      if (!this.isMoving) return;
      this.isMoving = false;
    }
  },
  data() {
    return {
      bar: undefined,
      slider: undefined,
      sliderWidth: undefined,
      sliderHeight: undefined,
      isMoving: false,
      // top: undefined,
      // left: undefined,
      offset: 0,
      start: 0,
      throttleTime: undefined
    };
  }
};
</script>

<style scoped>
.scroll-slider {
  position: relative;
  background: #eee;
  border-radius: 6px;
}
.slider-row {
  width: 100%;
  height: 10px;
}
.slider-col {
  width: 10px;
  height: 100%;
}
.scroll-slider-bar {
  position: absolute;
  border-radius: 6px;
  background-color: #666;
}
.slider-bar-row {
  left: 0;
  height: 100%;
  width: 30px;
}
.slider-bar-col {
  top: 0;
  height: 30px;
  width: 100%;
}
</style>
