<template>
  <div style="display:none;">
    <input
      type="file"
      id="uploadFolder"
      @change="requestUploadFolder"
      webkitdirectory
      multiple
    />
    <v-dialog v-model="visibleDialog" max-width="980">
      <simple-dialog
        title="Folder"
        :singleButton="false"
        okTitle="Select"
        @select="onSelect"
        @close="onCancel"
      >
        <v-sheet class="drop pa-5" height="400">
          <v-btn class="d-block text-none" color="primary" text>
            <v-icon class="mr-3">
              mdi-folder
            </v-icon>
            Use f for closed folders
          </v-btn>
          <v-btn
            class="d-block text-none"
            color="primary"
            text
            @click="openFolder"
          >
            <v-icon class="mr-3">
              mdi-folder-open
            </v-icon>
            Use F for opened folders
          </v-btn>
          <div
            class="d-flex align-center justify-center"
            style="height: 200px;"
          >
            <p
              class="text-h4 grey--text text--lighten-2"
              :style="files.length ? { color: 'black !important' } : {}"
            >
              {{
                files.length
                  ? files.length + " files are imported"
                  : "Please Open Folder"
              }}
            </p>
          </div>
        </v-sheet>
      </simple-dialog>
    </v-dialog>
  </div>
</template>

<script>
// import { mapGetters } from "vuex";

import SimpleDialog from "../../../custom/SimpleDialog";

export default {
  name: "OpenFolderDialog",

  components: { SimpleDialog },

  data: () => ({
    imageSource: null,
    files: []
  }),

  props: {
    value: {
      type: Boolean,
      default: false
    }
  },

  created() {
    this.newResWatch = this.$store.watch(
      (state, getters) => getters["image/newRes"],
      res => {
        const filteredData = [];
        for (var key in res) {
          const idx = parseInt(key.split("_")[1]);
          if (
            key.startsWith("folder_") &&
            res[key] &&
            idx < this.files.length
          ) {
            filteredData.push({
              filename: this.files[idx].name,
              metadata: res[key]
            });
          }
        }

        if (filteredData.length > 0) {
          this.$store.dispatch("image/addData", filteredData);
        }

        this.newFile = null;
        this.imageData = null;
      }
    );
  },

  beforeDestroy() {
    this.newResWatch();
  },

  computed: {
    visibleDialog: {
      get() {
        return this.value;
      },
      set(val) {
        this.$emit("input", val);
      }
    }
  },

  methods: {
    openFolder() {
      this.$el.querySelector("#uploadFolder").click();
    },

    requestUploadFolder() {
      const fileInput = this.$el.querySelector("#uploadFolder");
      if (fileInput.files && fileInput.files.length > 0) {
        this.files = fileInput.files;
      }
    },

    onSelect() {
      this.visibleDialog = false;

      if (!this.files) {
        return "";
      }

      let formData = new FormData();
      const name = this.getNameType();
      if (name) {
        this.files.forEach((file, idx) => {
          const type = file.name.match(
            /^(\w+)[_\s](\w+_\w+)_(\w\d{2})_(\d)_(\w)(\d{2})(\w\d{2})(\w\d)\.(\w+)$/
          );
          if (type && type[1] == name) {
            formData.append("folder_" + idx, file);
          }
        });
      } else {
        formData.append("folder_0", this.files[0]);
      }

      this.$store.dispatch("image/setNewFiles", formData);
    },

    onCancel() {
      this.files = null;
      this.visibleDialog = false;
    },

    getNameType() {
      if (!this.files) {
        return "";
      }

      let num = {};
      const cnt = this.files.length;
      for (let idx = 0; idx < cnt; idx++) {
        const type = this.files[idx].name.match(
          /^(\w+)[_\s](\w+_\w+)_(\w\d{2})_(\d)_(\w)(\d{2})(\w\d{2})(\w\d)\.(\w+)$/
        );
        if (type) {
          const name = type[1];
          if (num[name]) {
            num[name] += 1;
          } else {
            num[name] = 1;
          }
        }
      }

      let maxN = 1;
      let maxKey = "";
      for (var key in num) {
        if (maxN < num[key]) {
          maxN = num[key];
          maxKey = key;
        }
      }

      return maxKey;
    }
  }
};
</script>

<style scoped>
#uploadFolder {
  display: none;
}
</style>
