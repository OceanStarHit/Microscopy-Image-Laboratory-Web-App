<template>
  <v-expansion-panel class="rounded-0">
    <v-expansion-panel-header
      class="subtitle-2 font-weight-medium black--text"
    >
      {{ titleProp }}
    </v-expansion-panel-header>
    <v-expansion-panel-content>
      <slot />
    </v-expansion-panel-content>
  </v-expansion-panel>
</template>

<script lang="ts">
import Component from 'vue-class-component';
import Vue from 'vue';

const ExpansionPanelProps = Vue.extend({
  props: {
    title: String,
  }
})

@Component({})
export default class ExpansionPanel extends ExpansionPanelProps {

  get titleProp(): string {
    return this.title;
  }
}
</script>
