<template>
  <small-card title="Channels">
    <v-row class="mx-3 my-0" justify="space-around">
      <div v-for="c in channels" :key="c.id" class="channel-box text-center">
        <v-checkbox
          v-model="selected"
          style="margin-top: -12px"
          dense
          hide-details
          :class="c.color + '--text'"
          :value="c.label"
          :color="c.color"
          :disabled="!channelOptions.includes(c.label)"
          @change="onChange"
        ></v-checkbox>
        <div
          class="caption font-weight-medium"
          :class="c.color + '--text'"
          style="margin-top: -5px"
        >
          {{ c.label }}
        </div>
      </div>
    </v-row>
  </small-card>
</template>

<script>
import { mapGetters, mapState } from "vuex";

import SmallCard from "../../../custom/SmallCard";
import { createNamespacedHelpers } from "vuex";
const positionModule = createNamespacedHelpers("files/position");

export default {
  name: "Channnels",

  components: { SmallCard },

  created: function() {
    this.unwatchFiles = this.$store.watch(
      (state, getters) => getters["files/position/getFiles"],
      files => {
        this.selected = this.channelOptions;
      }
    );
  },
  beforeDestroy: function() {
    this.unwatchFiles();
  },
  data: () => ({
    selected: [],
    channels: [
      { id: 0, label: "S", color: "black", disabled: false },
      { id: 1, label: "B", color: "blue", disabled: false },
      { id: 2, label: "G", color: "green", disabled: false },
      { id: 3, label: "R", color: "red", disabled: false },
      { id: 4, label: "C", color: "cyan", disabled: false },
      { id: 5, label: "Y", color: "amber", disabled: false },
      { id: 6, label: "M", color: "pink", disabled: false }
    ]
  }),

  computed: {
    ...positionModule.mapGetters({
      files: "getFiles",
      channelOptions: "getChannelOptions"
    })
  },

  methods: {
    ...positionModule.mapActions({
      changeSelectsByChannels: "changeSelectsByChannels"
    }),
    onChange: function() {
      this.changeSelectsByChannels(this.selected);
    }
  }
};
</script>

<style scoped>
.channel-box >>> .v-input--selection-controls__input {
  margin-right: 0px;
}
i > .v-input--selection-controls__input.v-icon {
  border-top-color: red !important;
}
</style>
