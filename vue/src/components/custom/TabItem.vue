<template>
  <v-container class="px-0 py-1">
    <v-card outlined>
      <div class="px-3 py-2 blue lighten-5">
        <span class="subtitle-1 font-weight-medium primary--text">{{
          title
        }}</span>
        <div class="button-group">
          <v-btn
            v-if="buttons"
            color="primary"
            height="0"
            icon
            @click="onRefresh"
          >
            <v-icon>mdi-refresh</v-icon>
          </v-btn>
          <v-btn v-if="buttons" color="primary" height="0" icon @click="onHelp">
            <v-icon>mdi-help-circle-outline</v-icon>
          </v-btn>
        </div>
      </div>

      <slot></slot>
    </v-card>
  </v-container>
</template>

<script>
export default {
  name: "TabItem",

  props: ["title", "buttons"],

  data: () => ({}),

  methods: {
    onRefresh: function () {
      this.$emit("refresh");
    },
    onHelp: function () {
      this.$emit("help");
    },
  },
};
</script>

<style scoped>
.button-group {
  float: right;
}
</style>
