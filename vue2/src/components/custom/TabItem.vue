<template>
  <v-container class="px-0 py-1">
    <v-card outlined>
      <div class="px-3 py-2 blue lighten-5">
        <span class="subtitle-1 font-weight-medium primary--text">
          {{ titleProp }}
        </span>
        <div class="button-group">
          <v-btn
            v-if="isButtonsProp"
            color="primary"
            height="0"
            icon
            @click="onRefresh"
          >
            <v-icon>mdi-refresh</v-icon>
          </v-btn>
          <v-btn
            v-if="isButtonsProp"
            color="primary"
            height="0"
            icon
            @click="onHelp"
          >
            <v-icon>mdi-help-circle-outline</v-icon>
          </v-btn>
        </div>
      </div>

      <slot />
    </v-card>
  </v-container>
</template>

<script lang="ts">
import Component from 'vue-class-component';
import Vue from 'vue';


const TabItemProps = Vue.extend({
  props: {
    title: String,
    isButtons: Boolean
  }
})

@Component({})
export default class TabItem extends TabItemProps {

  // props: ['title', 'buttons']

  onRefresh(): void {
    this.$emit('refresh');
  }

  onHelp(): void {
    this.$emit('help');
  }

  get titleProp(): string {
    return this.title;
  }

  get isButtonsProp(): boolean {
    return this.isButtons;
  }
}
</script>

<style scoped>
.button-group {
  float: right;
}
</style>
