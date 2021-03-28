<template>
  <v-app>
    <v-app-bar app dark>
      <v-toolbar dark flat>
        <v-app-bar-nav-icon></v-app-bar-nav-icon>

        <v-toolbar-title class="title font-weight-bold">
          <v-img
            width="116"
            height="48"
            contain
            src="./assets/images/logo75.png"
          />
        </v-toolbar-title>

        <v-spacer></v-spacer>

        <v-btn icon>
          <v-icon>mdi-cog-outline</v-icon>
        </v-btn>

        <v-btn icon>
          <v-avatar color="primary" size="32">
            <span class="white--text">JM</span>
          </v-avatar>
        </v-btn>
      </v-toolbar>
    </v-app-bar>

    <v-main>
      <MainFrame />
    </v-main>
  </v-app>
</template>

<script>
import MainFrame from "./components/MainFrame";

export default {
  name: "App",

  components: {
    MainFrame,
  },

  data: () => ({
    //
  }),
};
</script>
