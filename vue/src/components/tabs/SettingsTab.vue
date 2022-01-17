<template>
  <tab-item title="Settings">
    <small-card title="Objective">
      <v-divider></v-divider>
    <Objective />
    </small-card>
  <v-divider class="my-2"></v-divider>
    <small-card title="Channnels">
      <v-divider></v-divider>
    <Channnels />
    </small-card>
  </tab-item>

</template>

<script>
import TabItem from "../custom/TabItem";
import Objective from "./contents/Settings/ObjectiveSettings.vue";
import Channnels from "./contents/Settings/ChannelSettings.vue"

export default {
  name: "SettingsTab",

  components: {
    TabItem,
    Objective,
    Channnels
  },

  data: () => ({})
};
</script>
