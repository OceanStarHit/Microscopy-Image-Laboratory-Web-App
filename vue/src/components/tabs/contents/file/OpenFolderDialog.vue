<template>
  <v-dialog v-model="visibleDialog" max-width="980">
    <simple-dialog
      title="Folder"
      :singleButton="false"
      okTitle="Select"
      @select="visibleDialog = false"
      @close="visibleDialog = false"
    >
      <v-sheet
        class="drop pa-5"
        height="400"
        :class="getClasses"
        @dragover.prevent="dragOver"
        @dragleave.prevent="dragLeave"
        @drop.prevent="drop($event)"
      >
        <v-btn class="d-block text-none" color="primary" text>
          <v-icon class="mr-3">
            mdi-folder
          </v-icon>
          Use f for closed folders
        </v-btn>
        <v-btn class="d-block text-none" color="primary" text>
          <v-icon class="mr-3">
            mdi-folder-open
          </v-icon>
          Use F for opened folders
        </v-btn>
        <div class="d-flex align-center justify-center" style="height: 200px;">
          <p class="text-h4 grey--text text--lighten-2">
            Drop your folder.
          </p>
        </div>
      </v-sheet>
    </simple-dialog>
  </v-dialog>
</template>

<script>
// import { mapGetters } from "vuex";

import SimpleDialog from "../../../custom/SimpleDialog";

export default {
  name: "OpenFolderDialog",

  components: { SimpleDialog },

  data: () => ({
    isDragging: false,
    imageSource: null
  }),

  props: {
    value: {
      type: Boolean,
      default: false
    }
  },

  computed: {
    visibleDialog: {
      get() {
        return this.value;
      },
      set(val) {
        this.$emit("input", val);
      }
    },
    getClasses() {
      return { isDragging: this.isDragging };
    }
  },

  methods: {
    dragOver() {
      this.isDragging = true;
    },
    dragLeave() {
      this.isDragging = false;
    },
    drop(e) {
      let files = e.dataTransfer.files;
      this.imageSource = files[0];

      alert(this.imageSource.name);

      this.isDragging = false;
    }
  }
};
</script>

<style scoped>
.isDragging {
  background-color: #e3f2fd;
  border-color: #fff;
}
</style>
