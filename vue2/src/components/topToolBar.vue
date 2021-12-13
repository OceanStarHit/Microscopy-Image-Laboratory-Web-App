<template>
  <v-app-bar app dark>
    <v-toolbar dark flat>
      <v-app-bar-nav-icon />

      <v-toolbar-title class="title font-weight-bold">
        <v-img
          width="116"
          height="48"
          contain
          src="@/assets/images/logo75.png"
        />
      </v-toolbar-title>

      <v-spacer />

      <v-btn icon>
        <v-icon>mdi-cog-outline</v-icon>
      </v-btn>

      <v-btn icon>
        <v-avatar color="primary" size="32">
          <span class="white--text">JM</span>
        </v-avatar>
      </v-btn>

      <v-btn icon>
        <v-icon @click="handleLogout">
          mdi-export
        </v-icon>
      </v-btn>
    </v-toolbar>
  </v-app-bar>
</template>
<script lang="ts">
import Component from 'vue-class-component';
import Vue from 'vue';

@Component({})
export default class TopToolBarComponent extends Vue {
  handleLogout() {
    this.$store.dispatch('auth/logOut');
  }
}
</script>

<style scoped>

</style>
