<template>
  <!--  <div class="d-none">-->
  <div>
    <v-btn
      class="cloud-btn mt-15 ml-5 ma-2"
      depressed
      color="primary"
      @click="isShowCloudDialog = true"
    >
      Cloud
    </v-btn>
    <open-cloud-dialog v-model="isShowCloudDialog" />

    <v-sheet
      class="drop pa-5 overflow-y-auto"
      height="600"
      :class="calculatedClass"
      @dragover.prevent="onDragOver"
      @dragleave.prevent="onDragLeave"
      @drop.prevent="onDrop($event)"
    >
      <div
        v-if="!tiles.length"
        class="d-flex align-center justify-center fill-height"
      >
        <p class="text-h4 grey--text text--lighten-2">
          {{ backgroundText }}
        </p>
      </div>
      <v-row v-else class="align-center">
        <v-col
          v-for="(tile, idx) in tiles"
          :key="idx"
          cols="2"
          class="px-4"
        >
          <img
            v-if="tile.thumbnailData"
            :id="'images_' + idx"
            :src="tile.thumbnailData"
            class="mx-auto"
            width="120"
          >
          <p class="ma-2 text-center text-caption">
            {{ tile.name }}
          </p>
        </v-col>
      </v-row>
    </v-sheet>
  </div>
</template>

<script lang="ts">
import Component from 'vue-class-component';
import Vue from 'vue';

import OpenCloudDialog from '../../OpenCloudDialog.vue';
import {TileModel} from '@/store/tiles.module';

@Component({
  components: {
    OpenCloudDialog
  },
})
export default class TilePositionFileDragArea extends Vue {

  isShowCloudDialog= false;
  isDragging= false;

  /* GET | SET */

  get tiles(): TileModel[] {
    return this.$store.state.tiles.tiles;
  }

  get calculatedClass() {
    return { isDragging: this.isDragging };
  }

  get backgroundText(): string {
    return this.$store.state.tile.view.backgroundText;
  }

  get progressBarPercentage(): number {
    return this.$store.state.tile.view.progressBarPercentage;
  }

  set progressBarPercentage(value: number) {
    this.$store.state.tile.view.progressBarPercentage = value;
  }

  /* METHODS */

  onDragOver() {
    this.isDragging = true;
  }

  onDragLeave() {
    this.isDragging = false;
  }

  onDrop(event: DragEvent) {
    /**
     * Handle file drop event
     *
     * Add files to store, which in turn will upload them to the api and add them to the local store.
     */

    this.isDragging = false;
    this.$store.commit('tiles/view/setIsLoading', true);
    event.preventDefault();
    //
    // this.allFiles = [];
    // this.clearFiles();
    const files: FileList = event.dataTransfer.files;
    const foo = event.dataTransfer.items;

    console.log(event);

    //
    // this.progressBarValue = 0;
    // this.progressBarMaxValue = 0;
    //
    // for (let i = 0; i < items.length; i++) {
    //   const item = items[i].webkitGetAsEntry();
    //   if (item) {
    //     const thiz = this;
    //     this.traverseFileTree(item, '', function() {
    //       thiz.progressBarValue++;
    //
    //       if (thiz.progressBarValue === thiz.progressBarMaxValue) {
    //         // console.log(
    //         //   thiz.progressBarValue + " / " + thiz.progressBarMaxValue
    //         // );
    //         // console.log(thiz.allFiles);
    //         api.uploadImageTiles(thiz.allFiles);
    //       }
    //     });
    //   }
    // }
    // this.resetConfig();
  }

  traverseFileTree(item: any, path: string, doneCB: any) {
    /* TODO redo this or just delete this mess */
    // const self = this;
    // path = path || '';
    // if (item.isFile) {
    //   item.file(function(file) {
    //     // console.log(file);
    //     if (checkFileType(file.name)) {
    //       self.progressBarMaxValue++;
    //
    //       self.allFiles.push(file);
    //       self.addFile({
    //         file: file,
    //         doneCB: doneCB
    //       });
    //     }
    //   });
    //   self.isLoading = false;
    // } else if (item.isDirectory) {
    //   //   enumerateDirectory(item).then(entries => {
    //   //     entries = entries.sort(function(a, b) {
    //   //       return a.name.localeCompare(b.name, undefined, {
    //   //         numeric: true,
    //   //         sensitivity: "base"
    //   //       });
    //   //     });
    //   //     for (let i = 0; i < entries.length; i++) {
    //   //       self.traverseFileTree(entries[i], path + item.name + "/");
    //   //     }
    //   //     self.loading = false;
    //   //   });
    // }
  }

  // Select example string in names&types tab
  selectFileNameString() {
  // selectExampleString() {
    /**
     *
     */

    //  todo this one seem quite smart so just rewrite it with types and general cleanup


    // todo move this along with the method to a file name component
    // let selectionRange = {
    //   text: '',
    //   startOffset: -1,
    //   endOffset: -1
    // }

    // if (typeof window.getSelection != 'undefined') {
    //   try {
    //     const sel = window.getSelection(),
    //         range = sel.getRangeAt(0);
    //     const selectionRect = range.getBoundingClientRect(),
    //         fullRect = this.$refs.exampleBox.getBoundingClientRect();
    //
    //     this.selectionRange.text = range.toString();
    //
    //     this.selectionRange.startOffset = Math.round(
    //         ((selectionRect.left - fullRect.left) / selectionRect.width) *
    //         range.toString().length
    //     );
    //     this.selectionRange.endOffset =
    //         this.selectionRange.startOffset + range.toString().length;
    //   } catch (error) {
    //     console.log(error);
    //   }
    // }
  }
}
</script>

<style scoped>
.pattern-section {
  width: 14.2%;
  padding: 5px;
}
.pattern-item-button {
  width: 100%;
  text-transform: none;
}
.pattern-item-button >>> input {
  width: 100%;
  text-align: center;
}
.pattern-item-button >>> label {
  width: 100%;
  text-align: center;
}
.pattern-item-button >>> .v-input__control {
  min-height: 30px !important;
}
.example-string >>> pre {
  font-size: 1.2em;
  font-weight: bold;
}
.name-type-input {
  margin-left: -5px;
  margin-right: -5px;
  margin-bottom: -30px;
}
.type-spacer {
  flex-grow: 0.1 !important;
}
.cloud-btn {
  width: 160px !important;
}
.common {
  width: 80px;
}
.filenames-list.v-select >>> .v-select__selections {
  display: none !important;
}
.filenames-list.v-select >>> .v-input__slot:before,
.filenames-list.v-select >>> .v-input__slot:after {
  border-style: none;
}
.meta-file-table >>> tr th:nth-child(2),
.meta-file-table >>> tr td:nth-child(2) {
  width: 295px !important;
}
.name-type-table >>> tr th:nth-child(2),
.name-type-table >>> tr td:nth-child(2) {
  width: 295px !important;
}
.progress-bar {
  width: 300pt;
}
</style>
