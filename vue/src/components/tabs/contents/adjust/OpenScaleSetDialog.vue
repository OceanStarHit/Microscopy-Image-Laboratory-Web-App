<template>
  <v-dialog v-model="visibleDialog" max-width="675px">
    <simple-dialog
      title="Scale"
      :single-button="false"
      ok-title="Select"
      @select="visibleCloud"
      @close="visibleDialog = false"
    >
    <div>
        <v-container        
        class=""
      >
        <v-row          
        >
          <v-col :cols="5">
            <v-card
              style="border: 1px solid white;"
              class="pa-2"
              outlined
              tile
            >
              <p>Manual Input</p>
              <label for="updownmanualinput" style="display:inline-block;">Pixel</label>
              <vue-numeric-input :value="4" controls-type="updown" id="updownmanualinput" style="display:inline-block;width:65px;margin-left:40px;height:38px;"></vue-numeric-input>
              <br>
              <br>
              <vue-numeric-input :value="4" controls-type="updown" id="updownmanualinput" style="display:inline-block;width:65px;height:38px;"></vue-numeric-input>
              <v-combobox style="width:103px;display:inline-block;margin-left:40px;"
                v-model="manualunitselect"
                :items="items"               
                height="40px" 
                outlined
                dense
              ></v-combobox>
              
            </v-card>
          </v-col>
          <v-col :cols="2">
            <v-card style="border: 1px solid white;"
              class="pa-2"
              outlined
              tile
            >
              
            </v-card>
          </v-col>
          <v-col :cols="5">
            <v-card
              style="border: 1px solid white;"
              class="pa-2"
              outlined
              tile
            >
              <p>Display Input</p>              
              <vue-numeric-input :value="4" controls-type="updown" id="updownmanualinput" style="display:inline-block;width:65px;height:38px;"></vue-numeric-input>
              <v-combobox style="width:103px;display:inline-block;margin-left:40px;"
                v-model="manualunitselect"
                :items="items"               
                height="40px" 
                outlined
                dense
              ></v-combobox>
              <br>              
              <v-btn style="margin-left: 107px;"
                depressed
                color="primary"
              >
                Display
              </v-btn>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </div>
    </simple-dialog>
  </v-dialog>
</template>
<script>
import SimpleDialog from "../../../custom/SimpleDialog";
import VueNumericInput from 'vue-numeric-input'
export default {
  name: "OpenScaleSetDialog",

  components: { 
    SimpleDialog,
    VueNumericInput
   },

  props: {
    value: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    visibleDialog: {
      get() {
        console.log(this.value);
        return this.value;
      },
      set(val) {
        this.$emit("input", val);
        
      }
    }
    
  },
  data () {
      return {
        manualunitselect: ['μm'],
        items: [
          'km',
          'hm',
          'dam',
          'm',
          'dm',
          'cm',
          'mm',
          'μm',
          'nm',
          'pm',
          'fm',
          'am',
          'zm',
          'ym'
        ],
      }
    },
  methods: {
    onClick: function() {},
    visibleCloud() {
      console.log("show cloud window");
    },
    selectData(item) {
      console.log(item);
    },
    selectedData(items) {
      console.login(items);
    },
    uploadFile() {
      console.log("asdfasd");
    }
  }
};
</script>

<style scoped></style>
