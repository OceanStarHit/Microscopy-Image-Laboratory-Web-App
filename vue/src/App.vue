<template>
  <div>
  <v-app v-if="showRegist">
    <v-main>
      <RegistPage />
    </v-main>
  </v-app>
  <v-app v-else-if="logind">    
    <v-app-bar app dark>
      <v-toolbar dark flat>
        <v-app-bar-nav-icon></v-app-bar-nav-icon>

        <v-toolbar-title class="title font-weight-bold">
          <v-img
            width="116"
            height="48"
            contain
            src="./assets/images/logo75.png"
          />
        </v-toolbar-title>

        <v-spacer></v-spacer>

        <v-btn icon>
          <v-icon>mdi-cog-outline</v-icon>
        </v-btn>

        <v-btn icon>
          <v-avatar color="primary" size="32">
            <span class="white--text" >JM</span>
          </v-avatar>
        </v-btn>

         <v-btn icon>
          <v-icon @click="handleLogout">mdi-export</v-icon>
        </v-btn>
      </v-toolbar>      
    </v-app-bar>

    <v-main>
      <MainFrame />
    </v-main>
  </v-app>
  <v-app v-else-if="!logind">
    <v-main>
      <LoginPage />
    </v-main>
  </v-app>
  
  </div>
</template>

<script>
import { mapState } from "vuex";
import LoginPage from "./components/login/login";
import RegistPage from "./components/login/regist";
import MainFrame from "./components/MainFrame";
import * as API from "./api/auth";

export default {
  name: "App",

  components: {
    LoginPage,
    RegistPage,
    MainFrame
  },

  data: () => ({
  }),

  computed: {    
    logind: () => {
      return sessionStorage.getItem('logind') == 'true'? true:false;
    },
    ...mapState({
      showRegist: state => state.auth.showRegist
    })
  },

  mounted() {
    console.log(this.logind);
  },

  methods: {
    handleLogout() {
        API.logout().then(response => {
            if (response.code == "LOGOUT_SUCCESS") {
              sessionStorage.setItem('logind',false);
              location.reload();
            } 
        }).catch(error => {
            console.error(error)            
        }); 
    }
  }
};
</script>
