<template>
  <small-card title="Channels">
    <v-row class="mx-3 my-0" justify="space-around">
      <div class="channel-box text-center" v-for="c in channels" :key="c.id">
        <v-checkbox
          v-model="selected"
          style="margin-top: -12px"
          dense
          hide-details
          :class="c.color + '--text'"
          :value="c.label"
          :color="c.color"
          :disabled="c.disabled"
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
import { mapGetters } from "vuex";

import SmallCard from "../../../custom/SmallCard";

export default {
  name: "Channel",

  components: { SmallCard },

  data: () => ({
    selected: [],
    channels: [
      { id: 0, label: "S", color: "black", disabled: false },
      { id: 1, label: "B", color: "blue", disabled: false },
      { id: 2, label: "G", color: "green", disabled: false },
      { id: 3, label: "R", color: "red", disabled: false },
      { id: 4, label: "C", color: "cyan", disabled: false },
      { id: 5, label: "Y", color: "amber", disabled: false },
      { id: 6, label: "M", color: "pink", disabled: false },
    ],
  }),

  created() {
    this.currentPageDataWatch = this.$store.watch(
      (state, getters) => getters["image/currentPageInfo"],
      (info) => {
        if (info.pageData.length == 1) {
          const channel = info.pageData[0].metadata.imageInfo.pixels.sizeC;
          this.setChannels(channel);
        } else {
          const idx = info.dataIndex;
          const types = info.pageData[idx].filename.match(
            /^(\w+)[_\s](\w+_\w+)_(\w\d{2})_(\d)_(\w)(\d{2})(\w\d{2})(\w\d)\.(\w+)$/
          );
          if (types) {
            this.setChannels(types[3]);
          }
        }
      }
    );
  },

  computed: {
    ...mapGetters("image", {
      chInfo: "channelInfo",
    }),
  },

  methods: {
    onChange: function () {
      if (this.currentChannel !== this.$store.state.image.parameters.C)
        this.$store.dispatch("image/changeParameterByC", this.currentChannel);
    },

    setChannels(n) {
      switch (n) {
        case 1:
          this.selected = ["S"];
          break;
        case 2:
          this.selected = ["S", "B"];
          break;
        default:
          this.selected = ["B", "G", "R"];
      }
    },
  },
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
