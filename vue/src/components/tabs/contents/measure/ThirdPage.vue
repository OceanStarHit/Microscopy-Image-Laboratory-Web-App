<template>
  <v-container class="pa-0">
    <small-card title="Measure Contents">
      <custom-button
        icon="book-open-page-variant"
        label="Measure Item"
        @click="onClick1"
      />
      <custom-button icon="play-circle" label="Sort Area" @click="onClick2" />
      <custom-button icon="cog" label="Set" @click="onClick3" />
    </small-card>
    <v-divider class="my-2"></v-divider>
    <small-card title="Save Method">
      <custom-button icon="content-save" label="Save" @click="onClick4" />
      <custom-button
        icon="content-save-edit"
        label="Save As"
        @click="onClick5"
      />
    </small-card>
    <v-divider class="my-2"></v-divider>
    <small-card title="Go">
      <custom-button icon="play-circle-outline" label="Go" @click="onClick6" />
      <custom-button
        icon="stop-circle-outline"
        label="Stop"
        @click="onClick7"
      />
      <custom-button
        icon="content-save-outline"
        label="Save"
        @click="onClick8"
      />
      <custom-button
        icon="close-circle-outline"
        label="Cancel"
        @click="onClick9"
      />
    </small-card>
  </v-container>
</template>

<script>
import SmallCard from "../../../custom/SmallCard";
import CustomButton from "../../../custom/CustomButton";

export default {
  name: "ThirdPage",

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
    onClick8: function () {
      console.log("Click8");
    },
    onClick9: function () {
      console.log("Click9");
    },
  },
};
</script>
