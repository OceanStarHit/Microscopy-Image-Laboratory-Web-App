<template>
  <v-container class="pa-0">
    <small-card title="Analysis Method">
      <custom-button
        icon="book-open-page-variant"
        label="Set Call"
        @click="onClick1"
      />
      <custom-button icon="play-circle" label="Go" @click="onClick2" />
    </small-card>
    <v-divider class="my-2"></v-divider>
    <small-card title="Learning Method">
      <custom-button icon="cube" label="DLCall" @click="onClick3" />
      <custom-button icon="layers" label="MLCall" @click="onClick4" />
      <custom-button icon="play-circle" label="Go" @click="onClick5" />
    </small-card>
    <v-divider class="my-2"></v-divider>
    <small-card title="Object Method">
      <custom-button icon="cube-outline" label="DLCall" @click="onClick6" />
      <custom-button icon="layers-outline" label="MLCall" @click="onClick7" />
    </small-card>
  </v-container>
</template>

<script>
import SmallCard from "../../../custom/SmallCard";
import CustomButton from "../../../custom/CustomButton";

export default {
  name: "FirstPage",

  components: {
    SmallCard,
    CustomButton,
  },

  data: () => ({}),

  methods: {
    onClick1: function () {
      console.log("Click1");
    },
    onClick2: function () {
      console.log("Click2");
    },
    onClick3: function () {
      console.log("Click3");
    },
    onClick4: function () {
      console.log("Click4");
    },
    onClick5: function () {
      console.log("Click5");
    },
    onClick6: function () {
      console.log("Click6");
    },
    onClick7: function () {
      console.log("Click7");
    },
  },
};
</script>
