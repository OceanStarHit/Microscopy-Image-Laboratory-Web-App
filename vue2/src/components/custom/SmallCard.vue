<template>
  <v-card class="pa-1" flat>
    <h5
      :style="{
        'font-weight': isChildProp ? 'normal' : 'bold'
      }"
    >
      {{ titleProp }}
    </h5>
    <v-card-actions>
      <v-row class="mt-1" justify="space-around">
        <slot />
      </v-row>
    </v-card-actions>
  </v-card>
</template>

<script lang="ts">
import Component from 'vue-class-component';
import Vue from 'vue';

const SmallCardProps = Vue.extend({
  props: {
    title: String,
    isChild: Boolean
  }
})

@Component({})
export default class SmallCard extends SmallCardProps {

  get titleProp(): string {
    return this.title;
  }

  get isChildProp(): boolean {
    return this.isChild;
  }
}
</script>
