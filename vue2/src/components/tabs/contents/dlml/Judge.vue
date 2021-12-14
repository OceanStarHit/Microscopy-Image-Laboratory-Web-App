<template>
  <small-card title="Judge">
    <custom-button
      icon="play-circle-outline"
      label="Go"
      @click="onGo"
    />
    <custom-button
      icon="thumb-up-outline"
      label="Good"
      @click="onGood"
    />
    <custom-button
      icon="thumb-down-outline"
      label="No"
      @click="onNo"
    />
    <custom-button
      icon="keyboard-return"
      label="Return"
      @click="onReturn"
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
export default class Judge extends Vue {

  onGo(): void {
    console.log('go');
  }

  onGood(): void {
    console.log('good');
  }

  onNo(): void {
    console.log('no');
  }

  onReturn(): void {
    console.log('return');
  }

}
</script>
