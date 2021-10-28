<template>
  <v-dialog v-model="visibleDialog" max-width="980">
    <simple-dialog
      title="Cloud"
      :single-button="false"
      ok-title="View the cloud"
      @select="visibleDialog = false"
      @close="visibleDialog = false"
    >
      <div class="d-flex my-2 mx-10">
        <h2 class="mr-2 mt-4">Experiment name</h2>
        <v-text-field
          v-model="experimentName"
        ></v-text-field>
      </div>
      <div class ="my-2 mx-10">
        <h3 class="mr-2 mt-4">select date</h3>
        <v-treeview
          v-model="tree"
          :open="initiallyOpen"
          :items="items"
          activatable
          item-key="name"
          open-on-click
        >
          <template v-slot:prepend="{ item, open }">
            <v-icon v-if="!item.file">
              {{ open ? "mdi-folder-open" : "mdi-folder" }}
            </v-icon>
            <v-icon v-else>
              {{ files[item.file] }}
            </v-icon>
          </template>
        </v-treeview>
      </div>
      <div class="d-flex justify-end mx-5 my-2">
        <v-btn
          class="mr-2 text-capitalize"
          color="info lighten-1"
        >
          {{ newSelect }}
        </v-btn>
        <v-btn
          color="info darken-2"
        >
          {{ newUpload }}
        </v-btn>
      </div>
      <v-img
        width="300"
        height="300">
      </v-img>
    </simple-dialog>
  </v-dialog>
</template>

<script>
// import { mapGetters } from "vuex";

import SimpleDialog from "../../../custom/SimpleDialog";

export default {
  name: "OpenCloudDialog",

  components: { SimpleDialog },

  props: {
    value: {
      type: Boolean,
      default: false
    },

    newSelect: {
      type: String,
      default: "Select date"
    },

    newUpload: {
      type: String,
      default: "Upload"
    }
  },

  data: () => ({
    initiallyOpen: ["public"],
    files: {
      image: "mdi-file-image",
      other: "mdi-file-document-outline"
    },
    tree: [],
    items: [
      {
        name: "name holder 2020-01-22",
        children: [
          {
            name: "gradient-512x512x10.tif",
            file: "image"
          },
          {
            name: "MR-MONO2-8-16x-heart.dcm",
            file: "other"
          }
        ]
      },
      {
        name: "name holder 2019-05-17",
        children: [
          {
            name: "20041103 1049_01_REF-1049-03 - EvoTec_0_H5_0.png",
            file: "image"
          },
          {
            name: "SmallMontage0008.tif",
            file: "image"
          }
        ]
      },
      {
        name: "name holder 2018-04-11",
        children: [
          {
            name: "Convallaria_3C_1T_confocal.ims",
            file: "other"
          },
          {
            name:
              "170912-FISH-Hela cell FISH-DAPI-GFP-TxRed-4735-40X FL OIL.tif",
            file: "image"
          }
        ]
      }
    ],
    experimentName: ''
  }),

  computed: {
    visibleDialog: {
      get() {
        return this.value;
      },
      set(val) {
        this.$emit("input", val);
      }
    },
  },

  methods: {
    onClick: function() {
      //
    }
  }
};
</script>

<style scoped></style>
