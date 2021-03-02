<template>
  <v-card>
    <v-card-title>{{ title }}</v-card-title>
    <v-divider></v-divider>
    <slot></slot>
    <v-divider></v-divider>
    <v-card-actions class="pa-6">
      <v-spacer></v-spacer>
      <v-btn v-if="updateButton" color="info darken-1" @click="updated">
        {{ updateTitle }}
      </v-btn>
      <v-btn v-if="deleteButton" color="warning darken-1" @click="deleted">
        {{ deleteTitle }}
      </v-btn>
      <v-btn color="success darken-2" @click="selected">
        {{ okTitle }}
      </v-btn>
      <v-btn v-if="!singleButton" color="primary darken-2" @click="closed">
        {{ cancelTitle }}
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
    updateButton: {
      type: Boolean,
      default: false
    },
    deleteButton: {
      type: Boolean,
      default: false
    },
    cancelTitle: {
      type: String,
      default: "Cancel"
    },
    okTitle: {
      type: String,
      default: "OK"
    },
    updateTitle: {
      type: String,
      default: "Update"
    },
    deleteTitle: {
      type: String,
      default: "Delete"
    }
  },

  methods: {
    closed: function() {
      this.$emit("close");
    },
    selected: function() {
      this.$emit("select");
    },
    updated: function() {
      this.$emit("close");
    },
    deleted: function() {
      this.$emit("close");
    }
  }
};
</script>
<style scoped>
.v-btn {
  width: 90px;
}
</style>
