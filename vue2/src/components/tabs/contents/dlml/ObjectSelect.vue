<template>
  <v-card class="pa-1" flat>
    <h5>Object Select</h5>
    <small-card title="Object Brightness" :child="true">
      <custom-button
        icon="lightbulb-outline"
        label="Light"
        @click="onLight"
      />
      <custom-button
        icon="lightbulb"
        label="Black"
        @click="onBlack"
      />
    </small-card>
    <small-card title="Select Target" :child="true">
      <custom-button
        icon="gesture-tap"
        label="Object"
        @click="onObject"
      />
      <custom-button
        icon="layers-triple"
        label="Area"
        @click="onArea"
      />
      <custom-button
        icon="gesture-tap-button"
        label="Back"
        @click="onBack"
      />
      <custom-button
        icon="cog"
        label="Set"
        @click="onSet"
      />
    </small-card>
  </v-card>
</template>

<script lang="ts">
import Component from 'vue-class-component';
import Vue from 'vue';

import SmallCard from '@/components/custom/SmallCard.vue';
import CustomButton from '@/components/custom/CustomButton.vue';

@Component({
  components: {
    SmallCard,
    CustomButton,
  },
})
export default class ObjectSelect extends Vue {

  onLight(): void {
    console.log('Light');
  }

  onBlack(): void {
    console.log('Black');
  }

  onObject(): void {
    console.log('Object');
  }

  onArea(): void {
    console.log('Area');
  }

  onBack(): void {
    console.log('Back');
  }

  onSet(): void {
    console.log('Set');
  }
}
</script>
