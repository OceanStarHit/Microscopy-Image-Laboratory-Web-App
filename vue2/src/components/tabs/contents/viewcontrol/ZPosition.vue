<template>
  <v-card class="pa-1" flat>
    <div
      style="display: flex; justify-content: space-between; align-items: center"
    >
      <h5>Z Position</h5>
      <div>
        <v-spacer />
        <v-btn
          class="pa-1"
          height="20"
          color="primary"
          small
          @click="on3dView"
        >
          3-D View
        </v-btn>
      </div>
    </div>
    <v-slider
      v-model="selectedZValue"
      prepend-icon="mdi-swap-vertical"
      :min="zMinIndex"
      :max="zMaxIndex"
      :readonly="zMaxIndex === 0"
      dense
      hide-details
    />
    <!--    @end="onChangeZValueChange"-->
    <!--    />-->
    <!-- <v-row class="pa-0 ml-10 mr-2 my-0" justify="space-between">
      <input
        class="range-field"
        type="number"
        :value="z_min"
        disabled
        @input="onChangeZmin"
      />
      <input
        class="range-field"
        type="number"
        :value="z_max"
        disabled
        @input="onChangeZmax"
      />
    </v-row> -->
  </v-card>
</template>

<script lang="ts">
import Component from 'vue-class-component';
import Vue from 'vue';
import {TileModel} from '@/store/tiles.module';

@Component({})
export default class ZPosition extends Vue {

  get selectedZValue(): number {
    return this.$store.state.tiles.selection.zIndex;
  }

  set selectedZValue(zValue: number) {
    this.$store.commit('tiles/addSelection', {zIndex: zValue})
  }

  get tilesAtRowAndColumnSelection(): TileModel[] {
    return this.$store.getters['tiles/getTilesAtRowAndColumnSelection'];
  }

  get zMaxIndex(): number {
    return this.$store.getters['tiles/getMaxZIndex'];
  }

  get zMinIndex(): number {
    return this.$store.getters['tiles/getMinZIndex'];
  }

  // onChangeZMin() {
  //   this.$forceUpdate();
  // }
  //
  // onChangeZMax() {
  //   this.$forceUpdate();
  // }

  // onChangeZValueChange(zValue: number) {
  //   this.$store.commit('t')
  // }

  on3dView() {
    console.log('3d view');
  }
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
