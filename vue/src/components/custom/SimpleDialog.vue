<template>
  <v-card>
    <v-card-title>{{ title }}</v-card-title>
    <v-divider></v-divider>
    <slot></slot>
    <v-divider></v-divider>
    <v-card-actions class="pa-6">
      <v-spacer></v-spacer>
      <v-btn v-if="!singleButton" color="primary darken-1" @click="closed">
        {{ cancelTitle }}
      </v-btn>
      <v-btn color="success darken-1" @click="selected">
        {{ okTitle }}
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  name: "SimpleDialog",

  data: () => ({}),

  props: {
    title: {
      type: String,
      default: ""
    },
    singleButton: {
      type: Boolean,
      default: true
    },
    cancelTitle: {
      type: String,
      default: "Cancel"
    },
    okTitle: {
      type: String,
      default: "OK"
    }
  },

  methods: {
    closed: function() {
      this.$emit("close");
    },
    selected: function() {
      this.$emit("select");
    }
  }
};
</script>
<style scoped>
.v-btn {
  width: 80px;
}
</style>
