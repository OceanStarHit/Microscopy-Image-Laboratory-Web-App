<template>
  <small-card title="Object Class">
    <custom-button icon="creation" label="Auto" @click="onAuto" />
    <custom-button icon="hand-pointing-up" label="Add" @click="onAdd" />
    <custom-button icon="trash-can-outline" label="Erase" @click="onErase" />
  </small-card>
</template>

<script>
import SmallCard from "../../../custom/SmallCard";
import CustomButton from "../../../custom/CustomButton";

export default {
  name: "ObjectClass2",

  components: {
    SmallCard,
    CustomButton,
  },

  data: () => ({}),

  methods: {
    onAuto: () => {
      console.log("Auto");
    },
    onAdd: () => {
      console.log("Add");
    },
    onErase: () => {
      console.log("Erase");
    },
  },
};
</script>
