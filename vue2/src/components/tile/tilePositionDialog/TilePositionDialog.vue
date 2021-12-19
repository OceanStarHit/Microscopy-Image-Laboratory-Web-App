<template>
  <div class="d-none">
    <v-dialog v-model="isShowDialog" persistent>
      <v-card>
        <!-- <v-card-title class="text-h5">
          Position
        </v-card-title> -->

        <v-tabs
          v-model="selectedTab"
          fixed-tabs
          @change="onTabChange"
        >
          <v-tab href="#tabs-images" class="primary--text">
            Images
          </v-tab>
          <v-tab
            href="#tabs-tiling"
            class="primary--text"
            :disabled="tiles.length === 0"
          >
            Tiling
          </v-tab>
          <v-tab
            href="#tabs-metadata"
            class="primary--text"
            :disabled="tiles.length === 0"
          >
            Metadata
          </v-tab>
          <v-tab
            href="#tabs-name-type"
            class="primary--text"
            :disabled="tiles.length === 0"
          >
            Names &amp; Files
          </v-tab>
        </v-tabs>

        <v-tabs-items v-model="selectedTab" class="v-tab-item">
          <!-- ------------- Images Tab -------------- -->

          <v-tab-item value="tabs-images">
            <tile-position-file-drag-area />
          </v-tab-item>
          <!--          <v-tab-item value="tabs-tiling" class="v-tab-item" eager>-->
          <!--          <v-tab-item value="tabs-tiling" class="v-tab-item">-->
          <!--            <Tiling-->
          <!--              @set-progress-max="setProgressMax"-->
          <!--              @set-progress-current="setProgressCurrent"-->
          <!--            />-->
          <!--          </v-tab-item>-->
          <!--          <v-tab-item value="tabs-metadata" class="v-tab-item">-->
          <!--            <v-sheet-->
          <!--              class="drop pa-5"-->
          <!--              height="600"-->
          <!--              :class="getClasses"-->
          <!--              @dragover.prevent="dragOver"-->
          <!--              @dragleave.prevent="dragLeave"-->
          <!--              @drop.prevent="drop($event)"-->
          <!--            >-->
          <!--              <div-->
          <!--                v-if="!files.length"-->
          <!--                class="d-flex align-center justify-center fill-height"-->
          <!--              >-->
          <!--                <p class="text-h4 grey&#45;&#45;text text&#45;&#45;lighten-2">-->
          <!--                  {{ backgroundText }}-->
          <!--                </p>-->
          <!--              </div>-->
          <!--              <v-card v-else>-->
          <!--                <v-card-title class="v-card-title">-->
          <!--                  <v-spacer />-->
          <!--                  <v-text-field-->
          <!--                    v-model="searchMetadata"-->
          <!--                    append-icon="mdi-magnify"-->
          <!--                    label="Search"-->
          <!--                    single-line-->
          <!--                    hide-details-->
          <!--                  />-->
          <!--                </v-card-title>-->
          <!--                <v-data-table-->
          <!--                  v-model="selectedMetaContents"-->
          <!--                  class="meta-file-table"-->
          <!--                  :headers="metaHeaders"-->
          <!--                  :items="getMetaContents"-->
          <!--                  :search="searchMetadata"-->
          <!--                  :single-select="false"-->
          <!--                  item-key="no"-->
          <!--                  @click:row="selectContent"-->
          <!--                />-->
          <!--              </v-card>-->
          <!--            </v-sheet>-->
          <!--          </v-tab-item>-->
          <!--          <v-tab-item value="tabs-name-type" class="v-tab-item">-->
          <!--            <v-sheet-->
          <!--              class="drop pa-5 v-sheet"-->
          <!--              height="600"-->
          <!--              :class="getClasses"-->
          <!--              @dragover.prevent="dragOver"-->
          <!--              @dragleave.prevent="dragLeave"-->
          <!--              @drop.prevent="drop($event)"-->
          <!--            >-->
          <!--              &lt;!&ndash; @mouseup="selectExampleString" &ndash;&gt;-->
          <!--              <div-->
          <!--                v-if="files.length == 0"-->
          <!--                class="d-flex align-center justify-center fill-height"-->
          <!--              >-->
          <!--                <p class="text-h4 grey&#45;&#45;text text&#45;&#45;lighten-2">-->
          <!--                  {{ backgroundText }}-->
          <!--                </p>-->
          <!--              </div>-->
          <!--              <div v-else>-->
          <!--                <v-row class="justify-center mx-5">-->
          <!--                  <div-->
          <!--                    class="d-flex align-center justify-center"-->
          <!--                    style="width: calc(100% - 70px);"-->
          <!--                  >-->
          <!--                    <v-row class="align-center justify-center">-->
          <!--                      <p class="mb-0 mr-8">-->
          <!--                        Example-->
          <!--                      </p>-->
          <!--                      <div-->
          <!--                        ref="exampleBox"-->
          <!--                        class="d-flex example-string"-->
          <!--                        @mouseup="selectExampleString"-->
          <!--                        v-html="exampleFileName"-->
          <!--                      />-->
          <!--                    </v-row>-->
          <!--                  </div>-->
          <!--                  <v-select-->
          <!--                    v-model="selectedFileName"-->
          <!--                    :items="fileNames"-->
          <!--                    class="filenames-list"-->
          <!--                    flat-->
          <!--                  />-->
          <!--                </v-row>-->
          <!--                <v-row class="align-center justify-center name-type-input">-->
          <!--                  <div-->
          <!--                    v-for="(pattern, idx) in namePatterns"-->
          <!--                    :key="idx"-->
          <!--                    class="pattern-section"-->
          <!--                  >-->
          <!--                    <v-btn-->
          <!--                      class="pattern-item-button"-->
          <!--                      :color="pattern.color"-->
          <!--                      small-->
          <!--                      dark-->
          <!--                      @click="clickNamePattern(idx)"-->
          <!--                    >-->
          <!--                      {{ pattern.label }}-->
          <!--                    </v-btn>-->
          <!--                    <v-text-field-->
          <!--                      v-model="namePatterns[idx].text"-->
          <!--                      class="pattern-item-button"-->
          <!--                      solo-->
          <!--                    />-->
          <!--                  </div>-->
          <!--                </v-row>-->
          <!--              </div>-->
          <!--              <v-card v-if="files.length > 0">-->
          <!--                <v-card-title class="v-card-title">-->
          <!--                  <v-btn-->
          <!--                    class="common"-->
          <!--                    :disabled="!canUpdate"-->
          <!--                    depressed-->
          <!--                    color="primary"-->
          <!--                    @click="updateNameType"-->
          <!--                  >-->
          <!--                    Update-->
          <!--                  </v-btn>-->
          <!--                  <v-spacer class="type-spacer" />-->
          <!--                  <v-btn-->
          <!--                    class="common"-->
          <!--                    :disabled="!canClear"-->
          <!--                    depressed-->
          <!--                    color="primary"-->
          <!--                    @click="clearNameType"-->
          <!--                  >-->
          <!--                    Clear-->
          <!--                  </v-btn>-->
          <!--                  <v-spacer />-->
          <!--                  <v-text-field-->
          <!--                    v-model="searchNameType"-->
          <!--                    append-icon="mdi-magnify"-->
          <!--                    label="Search"-->
          <!--                    single-line-->
          <!--                    hide-details-->
          <!--                  />-->
          <!--                </v-card-title>-->
          <!--                <v-data-table-->
          <!--                  class="name-type-table"-->
          <!--                  :headers="nameTypeTableHeaders"-->
          <!--                  :items="nameTypeTableContents"-->
          <!--                  :search="searchNameType"-->
          <!--                  :single-select="false"-->
          <!--                  item-key="no"-->
          <!--                  height="300"-->
          <!--                  fixed-header-->
          <!--                  @click:row="selectContent"-->
          <!--                />-->
          <!--              </v-card>-->
          <!--            </v-sheet>-->
          <!--          </v-tab-item>-->
        </v-tabs-items>

        <v-card-actions>
          <v-progress-linear
            :style="{
              visibility: progressBarPercentage < 100 ? 'visible' : 'hidden'
            }"
            color="light-blue"
            height="10"
            width="300"
            :value="progressBarPercentage"
            striped
            class="progress-bar"
          />

          <v-spacer />
          <v-btn
            color="green darken-1"
            :disabled="!this.tiles.length"
            text
            @click="onSelect"
          >
            OK
          </v-btn>

          <v-btn
            color="green darken-1"
            text
            @click="onClose"
          >
            CANCEL
          </v-btn>
        </v-card-actions>
      </v-card>
      <!-- </simple-dialog> -->
    </v-dialog>
  </div>
</template>

<script lang="ts">
import Component from 'vue-class-component';
import Vue from 'vue';

import * as utils from '@/utils/utils-func';

// import { getFileName } from '@/utils/utils-func';


// import utilFuncs = require('@/utils/utils-func');
//
// import {
//   getFileName,
//   checkFileType,
//   enumerateDirectory,
//   isOverlapped,
//   loadImage
// } from '@/utils/utils-func';

// import * as api from '../../api/tiles';

import OpenCloudDialog from '../OpenCloudDialog.vue';
import {TileModel} from '@/store/tiles.module';
import {tileNamePatternsConst} from '@/components/tile/tilePositionDialog/tile.constants';
import TilePositionFileDragArea from '@/components/tile/tilePositionDialog/tabs/TilePositionFileDragArea.vue';

// import SimpleDialog from "../../../custom/SimpleDialog";

// const positionModule = createNamespacedHelpers('files/position');
// import Tiling from './Tiling.vue';

// let createNewPage = true;

const TilePositionDialogProps = Vue.extend({
  props: {
    value: {
      type: Boolean,
      default: false
    }
  }
})

@Component({
  components: {
    TilePositionFileDragArea,
    // Tiling,
    OpenCloudDialog
  },
})
export default class TilePositionDialog extends TilePositionDialogProps {

  isDragging= false;
  selectedTab= null;

  /* GET | SET */

  // todo should isShowDialog be in the view store instead of a prop?
  get isShowDialog(): boolean {
    return this.value;
  }

  set isShowDialog(isShow: boolean) {
    this.$emit('input', isShow); // todo we are emitting because we are using v-model {value} as prop?
  }

  get tiles(): TileModel[] {
    return this.$store.state.tiles.tiles;
  }

  get selectedDefaultTile(): TileModel {
    return this.$store.state.tilePositionDialogView.selectedDefaultTile;
  }

  get calculatedClass() {
    return { isDragging: this.isDragging };
  }

  get backgroundText(): string {
    return this.$store.state.tilePositionDialogView.backgroundText;
  }

  get progressBarPercentage(): number {
    return this.$store.state.tilePositionDialogView.progressBarPercentage;
  }

  set progressBarPercentage(value: number) {
    this.$store.state.tilePositionDialogView.progressBarPercentage = value;
  }

  get filePatternHTMLString(): string {
    /**
     * Create a html string to show how to extract metadata from the filename
     *
     */
    // todo currently uses 'tileNamePatternsConst' which is fake data
    // todo clean this up and move it to a file name component
    // todo test this to make sure it actually works
    const fileNameOnly = utils.getFileName(this.selectedDefaultTile.fileName);
    let html = '',
        start = 0,
        str = '';

    const patterns = tileNamePatternsConst
        .filter(n => n.start > -1)
        .map(n => Object.assign({}, n));
    for (let i = 0; i < patterns.length; i++) {
      for (let j = i + 1; j < patterns.length; j++) {
        if (patterns[i].start > patterns[j].start) {
          const temp = patterns[i];
          patterns[i] = patterns[j];
          patterns[j] = temp;
        }
      }

      if (patterns[i].start > 0) {
        str = fileNameOnly.substring(start, patterns[i].start);
        html += `<pre>${str}</pre>`;
      }
      str = fileNameOnly.substring(patterns[i].start, patterns[i].end);
      html += `<pre class="${patterns[i].color}--text">${str}</pre>`;

      start = patterns[i].end;
    }

    str = fileNameOnly.substring(start, fileNameOnly.length);
    html += `<pre>${str}</pre>`;

    return html;
  }



  /* METHODS */

  onSelect() {
    // Click select button
    this.isShowDialog = false;
  }

  onClose() {
    // Click close button
    this.isShowDialog = false;
  }

  onTabChange(tabName: string): void {
    console.log(tabName);
    // if (tabIdx === 'tabs-tiling') {
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


// todo I dont know what this does, what does the filteredData and newRes data look like?!
//   this.newResWatch = this.$store.watch(
//     (state, getters) => getters['image/newRes'],
//     res => {
//       const filteredData = new Map();
//       const payload = {
//         files: filteredData,
//         appendToCurrentPage: false
//       };
//
//       payload.appendToCurrentPage = !createNewPage;
//       createNewPage = false;
//       for (const key in res) {
//         const idx = parseInt(key.split('_')[1]);
//         const fileName = this.allFiles[idx].name;
//         const p = getPosition(fileName);
//         if (
//           key.startsWith('position_') &&
//           res[key] &&
//           idx < this.allFiles.length
//         ) {
//           const extParams = {
//             row: p.row,
//             col: p.col,
//             z: p.z,
//             timeline: p.timeline,
//             objective: 4
//           };
//
//           const metadata = res[key];
//           if (metadata.imageInfo.objective) {
//             let X = 4;
//             const cm = metadata.imageInfo.objective.calibratedMagnification;
//             const nm = metadata.imageInfo.objective.nominalMagnification;
//
//             if (cm && nm) {
//               X = cm > nm ? cm : nm;
//             } else if (cm && !nm) {
//               X = cm;
//             } else if (!cm && nm) {
//               X = nm;
//             }
//             extParams.objective = X;
//           }
//
//           filteredData.set(idx, {
//             filename: fileName,
//             metadata: res[key],
//             extParams: extParams
//           });
//         }
//       }
//       if (filteredData.size > 0) {
//         this.$store.dispatch('image/addData', payload);
//       }
//       // this.newFile = null;
//       // this.imageData = null;
//     }
//   );
// },

  //
  //   resetConfig() {
  //     this.imageWidth = 0;
  //     this.imageHeight = 0;
  //     this.tiling.edit.activeFileItem = -1;
  //     this.tiling.edit.oldFileItem = -1;
  //   }
  //
  //
  //   ,
  //
  //
  //
  //   showImageData(idx) {
  //     if (-1 < idx && idx < this.imgData.length) {
  //       const imgData = this.imgData[idx];
  //       if (imgData) {
  //         this.$store.dispatch('image/setImageDataFromPosition', imgData);
  //       }
  //     }
  //   },
  //   showMetaData(idx) {
  //     if (-1 < idx && idx < this.metaData.length) {
  //       const metaData = this.metaData[idx];
  //       if (metaData) {
  //         this.$store.dispatch('image/setMetadataFromPosition', metaData);
  //       }
  //     }
  //   },
  //
  //   clickNamePattern(index) {
  //     const { text, startOffset, endOffset } = this.selectionRange;
  //     const selectedText = this.getSelectionText();
  //
  //     if (text !== '' && selectedText !== '') {
  //       if (text === selectedText) {
  //         if (startOffset > -1 && endOffset > -1) {
  //           const patterns = this.namePatterns.filter(n => n.start > -1);
  //           for (let i = 0; i < patterns.length; i++) {
  //             if (
  //               isOverlapped(
  //                 [patterns[i].start, patterns[i].end],
  //                 [startOffset, endOffset]
  //               )
  //             ) {
  //               break;
  //             }
  //             if (i === patterns.length) {
  //               this.namePatterns[index].text = text;
  //               this.namePatterns[index].start = startOffset;
  //               this.namePatterns[index].end = endOffset;
  //             }
  //           }
  //         }
  //       }
  //     }
  //   },
  //
  //   getSelectionText() {
  //     let text = '';
  //     if (window.getSelection) {
  //       text = window.getSelection().toString();
  //     } else if (document.selection && document.selection.type !== 'Control') {
  //       text = document.selection.createRange().text;
  //     }
  //     return text.replaceAll('\n', '');
  //   },
  //
  //   getMainName() {
  //     if (!this.allFiles) {
  //       return '';
  //     }
  //     const num = {};
  //     const cnt = this.allFiles.length;
  //     for (let idx = 0; idx < cnt; idx++) {
  //       if (this.allFiles[idx].name) {
  //         const name = getSeries(this.allFiles[idx].name);
  //
  //         if (num[name]) {
  //           num[name] += 1;
  //         } else {
  //           num[name] = 1;
  //         }
  //       }
  //     }
  //
  //     let maxN = 1;
  //     let maxKey = '';
  //     for (const key in num) {
  //       if (maxN < num[key]) {
  //         maxN = num[key];
  //         maxKey = key;
  //       }
  //     }
  //     return maxKey;
  //   },
  //   getSource(file) {
  //     if (
  //       file &&
  //       file.type &&
  //       file.type.startsWith('image/') &&
  //       !file.type.startsWith('image/tif') &&
  //       file.size < 2 * 1024 * 1024
  //     ) {
  //       const reader = new FileReader();
  //       reader.onload = function() {
  //         if (file.type.startsWith('image/tif')) {
  //           return require('../../../assets/images/no-preview.png');
  //         } else {
  //           return reader.result;
  //         }
  //       };
  //       reader.readAsDataURL(file);
  //     }
  //     return require('../../../assets/images/no-preview.png');
  //   },
  //   selectContent(content) {
  //     switch (this.selectedTab) {
  //       case 'tabs-images':
  //         {
  //           this.curImgIdx = content;
  //           const i = this.selectedImgIndices.indexOf(content);
  //           if (i > -1) {
  //             this.selectedImgIndices.splice(i, 1);
  //           } else {
  //             this.selectedImgIndices.push(content);
  //           }
  //         }
  //         break;
  //       case 'tabs-tiling':
  //         break;
  //       case 'tabs-metadata':
  //         this.curMetaIdx = content.no - 1;
  //         break;
  //       case 'tabs-name-type':
  //         this.curNameIdx = content.no - 1;
  //         break;
  //     }
  //   },
  //
  //   updateNamePattern(fileName) {
  //     for (let i = 0; i < this.namePatterns.length; i++) {
  //       let key = null;
  //       switch (i) {
  //         case 0:
  //           key = 'series';
  //           break;
  //         case 1:
  //           key = 'row';
  //           break;
  //         case 2:
  //           key = 'col';
  //           break;
  //         case 3:
  //           key = 'field';
  //           break;
  //         case 4:
  //           key = 'channel';
  //           break;
  //         case 5:
  //           key = 'z';
  //           break;
  //         case 6:
  //           key = 'time';
  //           break;
  //       }
  //       if (key) {
  //         this.setNamePattern({
  //           key: key,
  //           pos: [this.namePatterns[i].start, this.namePatterns[i].end]
  //         });
  //       }
  //     }
  //     if (fileName) {
  //       this.setNamePattern({
  //         key: 'totalLen',
  //         pos: fileName.length
  //       });
  //     }
  //   },
  //
  //   // update
  //   updateNameType() {
  //     const MAX_BATCH_SIZE = 10;
  //
  //     this.updateNamePattern(this.selectedFileName);
  //
  //     if (!this.allFiles) {
  //       console.log('allFiles error: ' + this.allFiles);
  //       return '';
  //     }
  //     const thiz = this;
  //     this.progressBarValue = 0;
  //     this.progressBarMaxValue = this.allFiles.length;
  //     for (const i in this.allFiles) {
  //       const p = getPosition(this.allFiles[i].name);
  //       this.addMetaData({
  //         index: i,
  //         metaData: {
  //           row: p.row,
  //           col: p.col,
  //           z: p.z,
  //           timeline: p.timeline,
  //           channel: p.channel,
  //           objectLense: 4 // The default object lense for name & type
  //         },
  //         doneCB: function() {
  //           thiz.progressBarValue++;
  //           console.log(
  //             thiz.progressBarValue + ' / ' + thiz.progressBarMaxValue
  //           );
  //         }
  //       });
  //     }
  //     if (this.allFiles.length > 0) {
  //       const defaultSelected = this.files[0];
  //       this.changeSelectsByRowCol({
  //         row: defaultSelected.metaData.row,
  //         col: defaultSelected.metaData.col
  //       });
  //       this.changeSelectsByObjectLense(defaultSelected.metaData.objectLense);
  //       this.changeSelectsByZ(defaultSelected.metaData.z);
  //       this.changeSelectsByTimeline(defaultSelected.metaData.timeline);
  //       this.changeSelectsByChannels(this.channelOptions);
  //     }
  //
  //     return;
  //
  //     // Remove bioformat.
  //     createNewPage = true;
  //     let formData = new FormData();
  //     const mainName = this.getMainName();
  //     let count = 0;
  //     if (mainName) {
  //       this.allFiles.forEach((file, idx) => {
  //         const name = getSeries(file.name);
  //
  //         if (mainName == name) {
  //           formData.append('position_' + idx, file);
  //           count++;
  //         }
  //
  //         if (count >= MAX_BATCH_SIZE) {
  //           this.$store.dispatch('image/setNewFiles', formData);
  //           formData = new FormData();
  //           count = 0;
  //         }
  //       });
  //     } else {
  //       formData.append('position_0', this.allFiles[0]);
  //       count++;
  //     }
  //
  //     if (count > 0) {
  //       this.$store.dispatch('image/setNewFiles', formData);
  //     }
  //   },
  //
  //   // clear
  //   clearNameType() {
  //     this.namePatterns.forEach(pattern => {
  //       pattern.start = -1;
  //       pattern.end = -1;
  //       pattern.text = '';
  //     });
  //   },
  //
  //   getNameType(filename) {
  //     return {
  //       series: this.getPatternValue(0, filename),
  //       row: this.getPatternValue(1, filename),
  //       column: this.getPatternValue(2, filename),
  //       field: this.getPatternValue(3, filename),
  //       viewMethod: this.getPatternValue(4, filename),
  //       zPosition: this.getPatternValue(5, filename),
  //       timepoint: this.getPatternValue(6, filename)
  //     };
  //   },
  //
  //   getPatternValue(index, filename) {
  //     const pattern = this.namePatterns[index];
  //     return pattern.start == -1
  //       ? ''
  //       : filename.substring(pattern.start, pattern.end);
  //   },
  //
  //   setProgressMax(maxValue) {
  //     console.log('in setProgressMax: ' + maxValue);
  //     this.progressBarMaxValue = maxValue;
  //   },
  //   setProgressCurrent(currValue) {
  //     this.progressBarValue = currValue;
  //   }
  // }
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
