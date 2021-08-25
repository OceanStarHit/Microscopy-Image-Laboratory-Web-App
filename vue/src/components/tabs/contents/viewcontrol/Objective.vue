<template>
  <small-card title="Objective">
    <v-row class="mx-3 my-0" justify="space-around">
      <ObjectiveButton
        v-for="o in objectives"
        :key="o.id"
        :label="o.m + 'X'"
        :active="selectedObjective == o.m"
        :disabled="!allOptions.includes(o.m)"
        @click="onSelect(o)"
      />
    </v-row>
  </small-card>
</template>

<script>
import SmallCard from "../../../custom/SmallCard";
import ObjectiveButton from "../../../custom/ObjectiveButton";
import { mapState, mapGetters, mapActions } from "vuex";

export default {
  name: "Objective",

  components: {
    SmallCard,
    ObjectiveButton
  },

  computed: {
    ...mapState({
      selectedObjective: state => state.image.parameters.objective
    }),
    ...mapGetters("image", {
      selectedImagesAtRowCol: "selectedImagesAtRowCol"
    }),
    allOptions: function() {
      let os = this.selectedImagesAtRowCol.map(img => img.extParams.objective);
      os = [...new Set(os)];
      return os;
    }
  },

  data: () => ({
    objectives: [
      { id: 0, m: 4, active: true },
      { id: 1, m: 10, active: false },
      { id: 2, m: 20, active: false },
      { id: 3, m: 40, active: false },
      { id: 4, m: 100, active: false }
    ]
  }),

  methods: {
    ...mapActions("image", {
      changeParameterByObjective: "changeParameterByObjective"
    }),
    onSelect: function(x) {
      console.log(x.m);
      this.changeParameterByObjective(x.m);
      // let activeId = -1;
      // for (var o of objs) {
      //   if (o.active) activeId = o.id;
      // }

      // if (activeId === -1) {
      //   objs[id].active = true;
      // } else {
      //   if (activeId === id) {
      //     objs[id].active = !objs[id].active;
      //   } else {
      //     objs[activeId].active = false;
      //     objs[id].active = true;
      //   }
      // }
    }
  }
};
</script>
