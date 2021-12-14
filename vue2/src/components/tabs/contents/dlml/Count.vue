<template>
  <small-card title="Count">
    <custom-button
      icon="calculator"
      label="Count"
      @click="onCount"
    />
    <custom-button
      icon="replay"
      label="Back"
      @click="onBack"
    />
    <custom-button
      icon="arrow-collapse-vertical"
      label="Split"
      @click="onSplit"
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
export default class Count extends Vue {

  onCount(): void {
    console.log('onCount')
  }

  onBack(): void {
    console.log('onBack')
  }

  onSplit(): void {
    console.log('onSplit')
  }
}
</script>
