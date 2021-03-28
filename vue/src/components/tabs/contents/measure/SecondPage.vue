<template>
  <v-container class="pa-0">
    <Vessel />
    <v-divider></v-divider>
    <Objective />
    <v-divider></v-divider>
    <Channel />
    <v-divider></v-divider>
    <ImageAdjust />
    <v-divider></v-divider>
    <ZPosition />
    <v-divider></v-divider>
    <Timeline />
  </v-container>
</template>

<script>
import Vessel from "../viewcontrol/Vessel";
import Objective from "../viewcontrol/Objective";
import Channel from "../viewcontrol/Channel";
import ImageAdjust from "../viewcontrol/ImageAdjust";
import ZPosition from "../viewcontrol/ZPosition";
import Timeline from "../viewcontrol/Timeline";

export default {
  name: "SecondPage",

  components: {
    Vessel,
    Objective,
    Channel,
    ImageAdjust,
    ZPosition,
    Timeline,
  },

  data: () => ({}),

  computed: {},
};
</script>
