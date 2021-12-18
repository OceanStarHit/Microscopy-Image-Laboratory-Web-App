<template>
  <small-card title="Objective">
    <v-row class="mx-3 my-0" justify="space-around">
      <!--      <ObjectiveButton-->
      <!--        v-for="objective in objectives"-->
      <!--        :key="objective.id"-->
      <!--        :label="objective.m + 'X'"-->
      <!--        :active="tileSelection.lensObjectiveM === objective.m"-->
      <!--        :disabled="!allLensObjectives.includes(objective.m)"-->
      <!--        @click="onSelect(objective)"-->
      <!--      />-->
    </v-row>
  </small-card>
</template>

<script lang="ts">
import Component from 'vue-class-component';
import Vue from 'vue';

import SmallCard from '../../../custom/SmallCard.vue';
import ObjectiveButton from '../../../custom/ObjectiveButton.vue';
import {lensObjectives} from '@/utils/constants';
import {LensObjectiveModel, TileModel, TileSelection} from '@/store/tiles.module';

const ObjectiveProps = Vue.extend()
@Component({
  components: {
    SmallCard,
    ObjectiveButton
  },
})
export default class Objective extends ObjectiveProps {

  objectives = lensObjectives;

  get tileSelection(): TileSelection {
    return this.$store.state.tiles.selection;
  }

  get tilesAtSelection(): TileModel[] {
    return this.$store.getters['tiles/getTilesAtSelection'];
  }

  get allLensObjectives(): number[] {
    return this.$store.getters['tiles/getAllLensObjectives'];
  }

  onSelect(lensObjective: LensObjectiveModel) {
    const selection: Partial<TileSelection> = { lensObjectiveM: lensObjective.m };
    this.$store.commit('tiles/addSelection', selection)
  }
}
</script>
