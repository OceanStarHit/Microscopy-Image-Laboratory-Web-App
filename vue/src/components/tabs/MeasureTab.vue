<template>
  <tab-item title="Measure">
    <div class="pa-3 text-center">
      <v-pagination v-model="page" :length="3"></v-pagination>
    </div>
    <v-divider class="mb-2"></v-divider>
    <first-page v-if="page == 1" />
    <second-page v-if="page == 2" />
    <third-page v-if="page == 3" />
  </tab-item>
</template>

<script>
import TabItem from "../custom/TabItem.vue";
import FirstPage from "./contents/measure/FirstPage";
import SecondPage from "./contents/measure/SecondPage";
import ThirdPage from "./contents/measure/ThirdPage";

export default {
  name: "MeasureTab",

  components: {
    TabItem,
    FirstPage,
    SecondPage,
    ThirdPage,
  },

  data: () => ({
    page: 1,
  }),
};
</script>
