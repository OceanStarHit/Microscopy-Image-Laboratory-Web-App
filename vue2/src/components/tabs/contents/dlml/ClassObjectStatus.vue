<template>
  <small-card title="Class & Object Status">
    <custom-button
      icon="square-rounded-outline"
      label="Area"
      @click="onArea"
    />
    <custom-button
      icon="palette-outline"
      label="Color"
      @click="onColor"
    />
    <custom-button
      icon="palette-swatch-outline"
      label="Int"
      @click="onInt"
    />
    <custom-button
      icon="cog"
      label="Set"
      @click="onSet"
    />
  </small-card>
</template>

<script lang="ts">
import Component from 'vue-class-component';
import Vue from 'vue';

import SmallCard from '@/components/custom/SmallCard.vue';
import CustomButton from '@/components/custom/CustomButton.vue';

@Component({
  components: {
    SmallCard,
    CustomButton
  }
})
export default class ClassObjectStatus extends Vue {

  onArea(): void {
    console.log('onArea')
  }

  onColor(): void {
    console.log('onColor')
  }

  onInt(): void {
    console.log('onInt')
  }

  onSet(): void {
    console.log('onSet')
  }
}
</script>
