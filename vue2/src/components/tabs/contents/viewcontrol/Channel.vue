<template>
  <small-card title="Channels">
    <v-row class="mx-3 my-0" justify="space-around">
      <!--      <div-->
      <!--        v-for="channel in channels"-->
      <!--        :key="channel.id"-->
      <!--        class="channel-box text-center"-->
      <!--      >-->
      <!--        <v-checkbox-->
      <!--          v-model="selected"-->
      <!--          style="margin-top: -12px"-->
      <!--          dense-->
      <!--          hide-details-->
      <!--          :class="channel.color + '&#45;&#45;text'"-->
      <!--          :value="channel.label"-->
      <!--          :color="channel.color"-->
      <!--          :disabled="!allChannelLabels.includes(channel.label)"-->
      <!--          @change="onChange(channel)"-->
      <!--        />-->
      <!--        <div-->
      <!--          class="caption font-weight-medium"-->
      <!--          :class="channel.color + '&#45;&#45;text'"-->
      <!--          style="margin-top: -5px"-->
      <!--        >-->
      <!--          {{ c.label }}-->
      <!--        </div>-->
      <!--      </div>-->
    </v-row>
  </small-card>
</template>

<script lang="ts">
import Component from 'vue-class-component';
import Vue from 'vue';

import SmallCard from '../../../custom/SmallCard.vue';
import {imageChannels} from '@/utils/constants';
import {TileModel, TileSelection} from '@/store/tiles.module';
import {ImageChannelModel} from '@/services/imageService.api';

@Component({
  components: {
    SmallCard,
  },
})
export default class Channel extends Vue {

  channels = imageChannels;

  private _selected: boolean[] = [];

  get selected(): boolean[] {
    return this._selected; // todo, legacy was faking it..this should be updated from the store as well
  }

  get tilesAtSelection(): TileModel[] {
    return this.$store.getters['tiles/getTilesAtSelection'];
  }

  get allChannelLabels(): number[] {
    return this.$store.getters['tiles/getAllChannels']
        .map((channel: ImageChannelModel) => channel.label)
  }

  onChange(channel: ImageChannelModel) {
    const selectedChannels: ImageChannelModel[] = this.$store.state.tiles.selection.channels;
    selectedChannels.push(channel);
    const selection: Partial<TileSelection> = { channels: selectedChannels };
    this.$store.commit('tiles/addSelection', selection)
  }
}
</script>

<style scoped>
.channel-box >>> .v-input--selection-controls__input {
  margin-right: 0px;
}
i > .v-input--selection-controls__input.v-icon {
  border-top-color: red !important;
}
</style>
