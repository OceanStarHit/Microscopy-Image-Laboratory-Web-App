<template>
  <small-card title="Object Class">
    <custom-button
      icon="creation"
      label="Auto"
      @click="onAuto"
    />
    <custom-button
      icon="hand-pointing-up"
      label="Add"
      @click="onAdd"
    />
    <custom-button
      icon="trash-can-outline"
      label="Erase"
      @click="onErase"
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
export default class ObjectClass extends Vue {

  onAuto(): void {
    console.log('Auto');
  }

  onAdd(): void {
    console.log('Add');
  }

  onErase(): void {
    console.log('Erase');
  }
}
</script>
