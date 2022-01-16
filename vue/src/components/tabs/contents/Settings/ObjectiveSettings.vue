<template>
  <small-card title="Objective">
    <v-row class="mx-3 my-0" justify="space-around">
      <ObjectiveButton
        v-for="o in objectives"
        :key="o.id"
        :label="o.m + 'X'"
        :active="selects.objectLense == o.m"
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
import { createNamespacedHelpers } from "vuex";
const positionModule = createNamespacedHelpers("files/position");

export default {
  name: "Objective",

  components: {
    SmallCard,
    ObjectiveButton
  },

  computed: {
    ...mapState({
      selects: state => state.files.position.selects
    }),
    ...positionModule.mapGetters({
      filesAtRowCol: "getFilesAtRowCol"
    }),

    allOptions: function() {
      let os = this.filesAtRowCol.map(file => file.metaData.objectLense);
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
    ...mapActions("files/position", {
      changeSelectsByObjectLense: "changeSelectsByObjectLense"
    }),
    onSelect: function(x) {
      this.changeSelectsByObjectLense(x.m);
    }
  }
};
</script>