<template>
  <small-card title="Merge/Split">
    <custom-button image="c-sep" label="Split" @click="select1" />
    <custom-button image="c-merge" label="Merge" @click="select2" />
    <custom-button image="c-drop" label="Drop" @click="select3" />
    <custom-button icon="cog" label="Set" @click="select4" />
  </small-card>
</template>

<script>
import SmallCard from "../../../custom/SmallCard";
import CustomButton from "../../../custom/CustomButton";

export default {
  name: "MergeSplit",

  components: {
    SmallCard,
    CustomButton,
  },

  data: () => ({}),

  methods: {
    select1: function () {
      console.log("Select-1");
    },
    select2: function () {
      console.log("Select-2");
    },
    select3: function () {
      console.log("Select-3");
    },
    select4: function () {
      console.log("Select-4");
    },
  },
};
</script>
