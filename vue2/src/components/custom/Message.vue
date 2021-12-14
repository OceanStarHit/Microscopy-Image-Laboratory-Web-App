<template>
  <transition name="fade" v-if="isShow">
    <div
      class="tip-box"
      :class="{
        success: type == 'success',
        warn: type == 'warn',
        err: type == 'err'
      }"
    >
      <div class="tip-box-content">
        {{ content }}
      </div>
    </div>
  </transition>
</template>

<script>
export default {
  name: "Tip",
  props: {
    content: {
      type: String,
      default: ""
    },
    type: {
      type: String,
      default: "default"
    },
    timer: {
      type: Number,
      default: 3000
    }
  },
  data() {
    return {
      isShow: false
    };
  },
  methods: {
    show() {
      this.isShow = true;
      setTimeout(this.hide, this.timer);
    },
    hide() {
      this.isShow = false;
      this.remove();
    }
  }
};
</script>

<style lang="scss" scoped>
.tip-box {
  position: fixed;
  left: 35%;
  top: 10px;
  font-size: 14px;
  width: 30%;
  padding: 20px 0;
  border-radius: 8px;
  letter-spacing: 1px;
  text-align: center;
  z-index: 9999;
  color: #fff;
  .tip-box-content {
    width: 90%;
    margin: 0 auto;
  }
}

.fade-center-active,
.fade-leave-active {
  transition: opacity 0.2s;
}
.fade-center,
.fade-leave-to {
  opacity: 0;
}

.success {
  background: #67c23a;
}
.warn {
  background: #e6a23c;
}
.err {
  background: #e24747;
}
.default {
  background: #909399;
}
</style>
