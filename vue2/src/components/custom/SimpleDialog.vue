<template>
  <v-card>
    <v-card-title>
      <h2>
        {{ titleProp }}
      </h2>
    </v-card-title>
    <v-divider />
    <slot />
    <v-divider />
    <v-card-actions class="pa-3">
      <v-spacer />

      <v-btn
        v-if="isNewButtonProp"
        :disabled="isNewButtonDisabledProp"
        color="warning lighten-1"
        @click="onNew"
      >
        {{ newTitleProp }}
      </v-btn>

      <v-btn
        v-if="isUpdateButtonProp"
        :disabled="isUpdateButtonDisabledProp"
        color="info darken-1"
        @click="onUpdate"
      >
        {{ updateTitleProp }}
      </v-btn>

      <v-btn
        v-if="isRemoveButtonProp"
        :disabled="isRemoveButtonDisabledProp"
        color="warning darken-2"
        @click="onRemove"
      >
        {{ removeTitleProp }}
      </v-btn>

      <v-btn
        :disabled="isSelectDisabledProp"
        color="success darken-2"
        @click="onSelect"
        class="mr-2 text-capitalize"
      >
        {{ okTitleProp }}
      </v-btn>
      <v-btn 
        v-if="!isSingleButtonProp"
        color="primary darken-2" 
        @click="onClose"
        class="mr-2 text-capitalize"
      >
        {{ closeTitleProp }}
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script lang="ts">
import Component from 'vue-class-component';
import Vue from 'vue';

const SimpleDialogProps = Vue.extend({
  props: {
    title: String,
    newTitle: String,
    updateTitle: String,
    removeTitle: String,
    okTitle: String,
    closeTitle: String,

    isNewButton: Boolean,
    isNewButtonDisabled: Boolean,
    isUpdateButton: Boolean,
    isUpdateButtonDisabled: Boolean,
    isRemoveButton: Boolean,
    isRemoveButtonDisabled: Boolean,

    isSingleButton: Boolean,

    isSelectDisabled: Boolean,
  }
})

@Component({})
export default class SimpleDialog extends SimpleDialogProps {

  onNew(): void {
    this.$emit('new');
  }

  onUpdate(): void {
    this.$emit('update');
  }

  onRemove(): void {
    this.$emit('remove');
  }

  onSelect(): void {
    this.$emit('select');
  }

  onClose(): void {
    this.$emit('close');
  }

  /* Prop getters */

  /* titles */
  get titleProp(): string {
    return this.title;
  }

  get newTitleProp(): string {
    return this.newTitle != undefined ? this.newTitle : 'New';
  }

  get updateTitleProp(): string {
    return this.updateTitle;
  }

  get removeTitleProp(): string {
    return this.removeTitle;
  }

  get okTitleProp(): string {
    return this.okTitle;
  }

  get closeTitleProp(): string {
    return this.closeTitle;
  }

  /* button booleans */
  get isNewButtonProp(): boolean {
    return this.isNewButton;
  }

  get isNewButtonDisabledProp(): boolean {
    return this.isNewButtonDisabled;
  }

  get isUpdateButtonProp(): boolean {
    return this.isUpdateButton;
  }

  get isUpdateButtonDisabledProp(): boolean {
    return this.isUpdateButtonDisabled;
  }

  get isRemoveButtonProp(): boolean {
    return this.isRemoveButton;
  }

  get isRemoveButtonDisabledProp(): boolean {
    return this.isRemoveButtonDisabled;
  }

  get isSingleButtonProp(): boolean {
    return this.isSingleButton;
  }

  get isSelectDisabledProp(): boolean {
    return this.isSelectDisabled;
  }


}
</script>
<style scoped>
/* .v-btn {
  width: 90px;
} */
</style>
