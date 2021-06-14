<template>
  <tab-item title="File/Edit" :buttons="true" @refresh="refresh" @help="help">
    <!-- Open Section -->
    <small-card title="Open">
      <custom-button
        icon="cloud-download-outline"
        label="Cloud"
        @click="cloudDialog = true"
      />
      <open-cloud-dialog v-model="cloudDialog" />

      <custom-button
        icon="email-newsletter"
        label="File"
        @click="fileDialog = true"
      />
      <open-file-dialog v-model="fileDialog" />

      <custom-button
        icon="folder-open-outline"
        label="Folder"
        @click="folderDialog = true"
      />
      <open-folder-dialog v-model="folderDialog" />

      <custom-button
        icon="dots-grid"
        label="Position"
        @click="positionDialog = true"
      />
      <open-position-dialog v-model="positionDialog" />
    </small-card>
    <v-divider class="my-2"></v-divider>

    <!-- Save/Load Section -->
    <small-card title="Save / Load">
      <custom-button icon="content-save-outline" label="Save" @click="onSave" />
      <custom-button
        icon="content-save-edit-outline"
        label="SaveAs"
        @click="onSaveAs"
      />
      <custom-button icon="upload" label="Export" @click="onExport" />
      <custom-button icon="download" label="Load" @click="onLoad" />
    </small-card>
    <v-divider class="my-2"></v-divider>

    <!-- Edit Section -->
    <small-card title="Edit">
      <custom-button icon="content-cut" label="Cut" @click="onCut" />
      <custom-button icon="content-copy" label="Copy" @click="onCopy" />
      <custom-button icon="content-paste" label="Paste" @click="onPaste" />
      <custom-button icon="file-outline" label="New" @click="onNew" />
    </small-card>
    <v-divider class="my-2"></v-divider>

    <!-- Comment Section -->
    <small-card title="Comment">
      <custom-button icon="near-me" @click="onSelect1" />
      <custom-button icon="pencil" @click="onSelect2" />
      <custom-button icon="checkbox-blank-circle-outline" @click="onSelect3" />
      <custom-button icon="dots-vertical" @click="onSelect4" />
      <custom-button icon="vector-rectangle" @click="onSelect5" />
      <custom-button icon="square-edit-outline" @click="onSelect6" />
      <custom-button icon="trash-can-outline" @click="onSelect7" />
    </small-card>
    <v-divider class="my-2"></v-divider>

    <!-- Change Dimension Section -->
    <small-card title="Change Dimension">
      <custom-button
        icon="sort-clock-descending-outline"
        label="Z->T"
        @click="onSelect8"
      />
      <custom-button
        icon="sort-clock-ascending"
        label="T->Z"
        @click="onSelect9"
      />
      <custom-button icon="cog" label="Set" @click="onSelect10" />
    </small-card>
  </tab-item>
</template>

<script>
import TabItem from "../custom/TabItem.vue";
import SmallCard from "../custom/SmallCard";
import CustomButton from "../custom/CustomButton";

import OpenCloudDialog from "./contents/file/OpenCloudDialog";
import OpenFileDialog from "./contents/file/OpenFileDialog";
import OpenFolderDialog from "./contents/file/OpenFolderDialog";
import OpenPositionDialog from "./contents/file/OpenPositionDialog";

export default {
  name: "FileTab",

  components: {
    TabItem,
    SmallCard,
    CustomButton,
    OpenCloudDialog,
    OpenFileDialog,
    OpenFolderDialog,
    OpenPositionDialog,
  },

  data: () => ({
    cloudDialog: false,
    fileDialog: false,
    folderDialog: false,
    positionDialog: false,
  }),

  methods: {
    refresh: function () {
      console.log("Refresh");
    },
    help: function () {
      console.log("Help");
    },
    onPosition: function () {
      console.log("Position");
    },
    onSave: function () {
      console.log("Save");
    },
    onSaveAs: function () {
      console.log("SaveAs");
    },
    onExport: function () {
      console.log("Export");
    },
    onLoad: function () {
      console.log("Load");
    },
    onCut: function () {
      console.log("Cut");
    },
    onCopy: function () {
      console.log("Copy");
    },
    onPaste: function () {
      console.log("Paste");
    },
    onNew: function () {
      console.log("New");
    },
    onSelect1: function () {
      console.log("Select-1");
    },
    onSelect2: function () {
      console.log("Select-2");
    },
    onSelect3: function () {
      console.log("Select-3");
    },
    onSelect4: function () {
      console.log("Select-4");
    },
    onSelect5: function () {
      console.log("Select-5");
    },
    onSelect6: function () {
      console.log("Select-6");
    },
    onSelect7: function () {
      console.log("Select-7");
    },
    onSelect8: function () {
      console.log("Select-8");
    },
    onSelect9: function () {
      console.log("Select-9");
    },
    onSelect10: function () {
      console.log("Select-10");
    },
  },
};
</script>
