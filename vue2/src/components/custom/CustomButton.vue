<template>
  <v-btn
    class="px-0"
    min-width="24"
    :height="labelProp ? 38 : 28"
    text
    color="teal"
    @click="onClick"
  >
    <div class="ma-0">
      <div v-if="imageNameProp" class="pa-1">
        <v-img
          style="margin: 0 auto"
          width="12"
          height="12"
          :src="imageUrl"
        />
      </div>
      <v-icon
        v-if="icon"
        class="ma-0"
        :dense="true"
      >
        mdi-{{ iconProp }}
      </v-icon>
      <div class="label-text caption">
        {{ labelProp }}
      </div>
    </div>
  </v-btn>
</template>

<script lang="ts">
import Component from 'vue-class-component';
import Vue from 'vue';

const CustomButtonProps = Vue.extend({
  props: {
    icon: String,
    imageName: String,
    label: String,
  }
})

@Component({})
export default class CustomButton extends CustomButtonProps {

  onClick(): void {
    this.$emit('click');
  }

  get imageUrl(): string {
    return '@/assets/images/' + this.imageName + '.png';
  }

  /* prop getters */

  get iconProp(): string {
    return this.icon;
  }

  get imageNameProp(): string {
    return this.imageName;
  }

  get labelProp(): string {
    return this.label;
  }
}
</script>

<style scoped>
.label-text {
  text-transform: capitalize !important;
  line-height: 0.75rem;
}
</style>
