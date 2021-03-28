<template>
  <v-card class="pa-1" flat>
    <h5
      :style="{
        'font-weight': child ? 'normal' : 'bold',
      }"
    >
      {{ title }}
    </h5>
    <v-card-actions>
      <v-row class="mt-1" justify="space-around">
        <slot></slot>
      </v-row>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  name: "SmallCard",

  props: ["title", "child"],

  data: () => ({}),
};
</script>
