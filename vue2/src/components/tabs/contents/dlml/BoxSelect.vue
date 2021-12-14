<template>
  <small-card title="Box Select">
    <custom-button icon="near-me" @click="select1" />
    <custom-button icon="pencil" @click="select2" />
    <custom-button icon="checkbox-blank-circle-outline" @click="select3" />
    <custom-button icon="dots-vertical" @click="select4" />
    <custom-button icon="vector-rectangle" @click="select5" />
    <custom-button icon="square-edit-outline" @click="select6" />
    <custom-button icon="trash-can-outline" @click="select7" />
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
export default class BoxSelect extends Vue {

  select1(): void {
    console.log('select-1')
  }

  select2(): void {
    console.log('select-2')
  }

  select3(): void {
    console.log('select-3')
  }

  select4(): void {
    console.log('select-4')
  }

  select5(): void {
    console.log('select-5')
  }

  select6(): void {
    console.log('select-6')
  }

  select7(): void {
    console.log('select-7')
  }
}
</script>
