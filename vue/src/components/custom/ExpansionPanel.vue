<template>
  <v-expansion-panel class="rounded-0">
    <v-expansion-panel-header
      class="subtitle-2 font-weight-medium black--text"
      >{{ title }}</v-expansion-panel-header
    >
    <v-expansion-panel-content>
      <slot></slot>
    </v-expansion-panel-content>
  </v-expansion-panel>
</template>

<script>
export default {
  name: "ExpansionPanel",

  props: ["title"],

  data: () => ({}),
};
</script>
