<template>
  <small-card title="Method Select">
    <custom-button
      icon="plus-box"
      label="New"
      @click="onNew"
    />
    <custom-button
      icon="play-box"
      label="Call"
      @click="onCall"
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
    CustomButton,
  },
})
export default class MethodSelect extends Vue {

  onNew(): void {
    console.log('New');
  }

  onCall(): void {
    console.log('Call');
  }
}
</script>
