<template>
  <v-app>
    <TopToolBar />
    <v-main>
      <v-container class="pa-0" fluid>
        <v-row no-gutters>
          <!-- Left Sidebar -->
          <LeftToolBar />

          <!-- Center  -->
          <v-col />
          <!--          -->
          <!--          -->
          <!--          <v-col-->
          <!--            class="grey lighten-3"-->
          <!--            cols="8"-->
          <!--            :style="{-->
          <!--              height: windowHeight + 'px'-->
          <!--            }"-->
          <!--            style="border-left: 1px dotted gray; border-right: 1px dotted gray"-->
          <!--          >-->
          <!--            <ImageViewer />-->
          <!--          </v-col>-->

          <!-- Right Sidebar -->
          <RightToolBar />
        </v-row>

        <!--        <loading-->
        <!--          :active.sync="loading_count_gt_zero"-->
        <!--          :can-cancel="false"-->
        <!--          :is-full-page="true"-->
        <!--          :opacity="0.8"-->
        <!--        >-->
        <!--          <v-container class="text-center loading-progress-bar">-->
        <!--            <v-progress-linear-->
        <!--              color="light-blue"-->
        <!--              height="15"-->
        <!--              :value="loading_bar_value"-->
        <!--              striped-->
        <!--            />-->
        <!--            <div class="title mt-4 teal&#45;&#45;text">-->
        <!--              In update ...-->
        <!--            </div>-->
        <!--          </v-container>-->
        <!--        </loading>-->

        <!--        <loading-->
        <!--          :active.sync="loading"-->
        <!--          :can-cancel="false"-->
        <!--          :is-full-page="true"-->
        <!--          :opacity="0.6"-->
        <!--        >-->
        <!--          <v-container class="text-center">-->
        <!--            <v-progress-circular-->
        <!--              :size="50"-->
        <!--              color="teal"-->
        <!--              indeterminate-->
        <!--            />-->
        <!--            <div class="title mt-4 teal&#45;&#45;text">-->
        <!--              Loading...-->
        <!--            </div>-->
        <!--          </v-container>-->
        <!--        </loading>-->
      </v-container>

      here
      <!--      <MainFrame />-->
    </v-main>
  </v-app>
</template>

<script lang="ts">
import Vue from 'vue';
import Component from 'vue-class-component';
import TopToolBar from '@/components/topToolBar.vue';
import LeftToolBar from '@/components/leftToolBar/leftToolBar.vue';
import RightToolBar from '@/components/rightToolBar/rightToolBar.vue';
import windowSizeService from '@/services/windowSizeService';

@Component({
  components: {
    TopToolBar,
    LeftToolBar,
    RightToolBar,
  },
})
export default class MainComponent extends Vue {
  /** importing windowService would be enough but making it a variable here just to clearly show that is being used.
   * It needs to be started and kept running throughout the lifetime of the app to allow it to update the window size state.*/
  __keep_me_running = windowSizeService;

}
</script>

<style scoped>

</style>
