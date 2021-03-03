<template>
  <v-card>
    <v-card-title>{{ title }}</v-card-title>
    <v-divider></v-divider>
    <slot></slot>
    <v-divider></v-divider>
    <v-card-actions class="pa-6">
      <v-spacer></v-spacer>
      <v-btn
        v-if="updateButton"
        :disabled="updateDisable"
        color="info darken-1"
        @click="updated"
      >
        {{ updateTitle }}
      </v-btn>
      <v-btn
        :disabled="deleteDisable"
        v-if="deleteButton"
        color="warning darken-1"
        @click="deleted"
      >
        {{ deleteTitle }}
      </v-btn>
      <v-btn
        :disabled="selectDisable"
        color="success darken-2"
        @click="selected"
      >
        {{ okTitle }}
      </v-btn>
      <v-btn v-if="!singleButton" color="primary darken-2" @click="closed">
        {{ closeTitle }}
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

    // update button
    updateTitle: {
      type: String,
      default: "Update"
    },
    updateButton: {
      type: Boolean,
      default: false
    },
    updateDisable: {
      type: Boolean,
      default: false
    },

    // delete button
    deleteTitle: {
      type: String,
      default: "Delete"
    },
    deleteButton: {
      type: Boolean,
      default: false
    },
    deleteDisable: {
      type: Boolean,
      default: false
    },

    // ok button
    okTitle: {
      type: String,
      default: "OK"
    },
    selectDisable: {
      type: Boolean,
      default: false
    },

    // close button
    closeTitle: {
      type: String,
      default: "Cancel"
    },
    singleButton: {
      type: Boolean,
      default: true
    }
  },

  methods: {
    updated: function() {
      this.$emit("update");
    },
    deleted: function() {
      this.$emit("delete");
    },
    selected: function() {
      this.$emit("select");
    },
    closed: function() {
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
