<template>
  <v-btn
    class="px-0"
    :class="isActiveProp ? 'grey lighten-2' : ''"
    min-width="24"
    min-height="52"
    text
    :disabled="isDisabledProp"
    color="teal"
    @click="onClick"
  >
    <div class="my-2">
      <v-img
        style="margin: 0 auto"
        width="32"
        height="32"
        src="../../assets/images/object.png"
      />
      <div class="caption" :class="isActiveProp ? 'font-weight-bold' : ''">
        {{ labelProp }}
      </div>
    </div>
  </v-btn>
</template>

<script lang="ts">
import Component from 'vue-class-component';
import Vue from 'vue';

const ObjectiveButtonProps = Vue.extend({
  props: {
    label: String,
    isActive: Boolean,
    isDisabled: Boolean,
  }
})

@Component({})
export default class ObjectiveButton extends ObjectiveButtonProps {

  onClick(): void {
    this.$emit('click');
  }

  /* prop getters */
  get labelProp(): string {
    return this.label;
  }

  get isActiveProp(): boolean {
    return this.isActive;
  }

  get isDisabledProp(): boolean {
    return this.isDisabled;
  }

}
</script>
