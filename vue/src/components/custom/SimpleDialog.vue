<template>
  <v-card>
    <v-card-title>
      <h2>
        {{ title }}
      </h2>
    </v-card-title>
    <v-divider></v-divider>
    <slot></slot>
    <v-divider></v-divider>
    <v-card-actions class="pa-3">
      <v-spacer></v-spacer>
      <v-btn
        v-if="newButton"
        :disabled="newDisable"
        color="warning lighten-1"
        @click="newed"
      >
        {{ newTitle }}
      </v-btn>
      <v-btn
        v-if="updateButton"
        :disabled="updateDisable"
        color="info darken-1"
        @click="updated"
      >
        {{ updateTitle }}
      </v-btn>
      <v-btn
        v-if="removeButton"
        :disabled="removeDisable"
        color="warning darken-2"
        @click="removed"
      >
        {{ removeTitle }}
      </v-btn>
      <v-btn
        :disabled="selectDisable"
        color="success darken-2"
        @click="selected"
        class="mr-2 text-capitalize"
      >
        {{ okTitle }}
      </v-btn>
      <v-btn 
        v-if="!singleButton" 
        color="primary darken-2" 
        @click="closed"
        class="mr-2 text-capitalize"
      >
        {{ closeTitle }}
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  name: "SimpleDialog",

  props: {
    title: {
      type: String,
      default: ""
    },

    // new button
    newTitle: {
      type: String,
      default: "New"
    },
    newButton: {
      type: Boolean,
      default: false
    },
    newDisable: {
      type: Boolean,
      default: false
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

    // remove button
    removeTitle: {
      type: String,
      default: "remove"
    },
    removeButton: {
      type: Boolean,
      default: false
    },
    removeDisable: {
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

  data: () => ({}),

  methods: {
    newed: function() {
      this.$emit("new");
    },
    updated: function() {
      this.$emit("update");
    },
    removed: function() {
      this.$emit("remove");
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
/* .v-btn {
  width: 90px;
} */
</style>