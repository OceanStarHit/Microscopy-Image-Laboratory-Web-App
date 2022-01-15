<template>
  <tab-item title="Settings">
    <small-card title="Objective">
      <v-divider></v-divider>
    <Objective />
    </small-card>
  </tab-item>
</template>

<script>
import TabItem from "../custom/TabItem";
import Objective from "./contents/viewcontrol/Objective";

export default {
  name: "SettingsTab",

  components: { 
    TabItem,
    Objective 
  },

  data: () => ({})
};
</script>
