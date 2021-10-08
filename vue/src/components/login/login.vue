<template>
  <div class="login-container">
    <v-container
      ref="loginForm"
      :model="loginForm"
      :rules="loginRules"
      class="login-form"
      auto-complete="on"
      label-position="left"
      :validate-on-rule-change="false"
    >
      <!-- 设置语言 -->

      <div class="title-container">
        <h3 class="title">{{ 'Login' }}</h3>
      </div>

      <v-col prop="account">
        <label>Email</label>
        <input
          v-model="loginForm.account"
          name="account"
          type="text"
          auto-complete="on"
          class="txt"
        />
      </v-col>

      <v-col prop="password">
        <label>Password</label>
        <input
          v-model="loginForm.password"
          class="txt"
          type="password"
          name="password"
          auto-complete="on"
          show-password          
        />
      </v-col>

    <v-col >
      <button
        :loading="loading"
        type="primary"
        size="large"
        style="width: 100%; height: 50px; margin-bottom: 30; background: lightblue; border-radius: 2px;"
        @click="handleLogin"
      >
        {{ 'Login' }}
      </button>
      <a style="float:right;" @click="regi">Switch to register</a>
      </v-col>
    </v-container>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import * as API from "../../api/auth";

export default {
  name: 'LoginPage',
  layout: 'login',
  components: {
  },
  data() {
    return {
      loginForm: { account: '', password: '' },
      loginRules: {
        account: [
          {
            required: true,
            trigger: 'blur',
            message: 'Email'
          }
        ],
        password: [
          {
            required: true,
            trigger: 'blur',
            message: 'Password'
          }
        ]
      },
      loading: false
    }
  },
  computed: {
    
  },
  methods: {
    async handleLogin() {
      try {
        this.loading = true
        API.login(this.loginForm).then(response => {
            console.log(response);
            console.log(this.$message);
            if (response.code == "LOGIN_SUCCESS") {
              sessionStorage.setItem('logind',true);
              this.$store.dispatch("auth/setLogind", {
                'logind':true,
                'token':''
              });                   
              this.$message({content:"Login succeed!",type:"success"}).show();              
              location.reload();         
            } else {
              this.$store.dispatch("auth/setLogind", {
                'logind':false,
                'token':''
              });              
              this.$message({content:"Email or password not correct!",type:"err"}).show();
            }            

        }).catch(error => {
            console.error(error);
            this.$store.dispatch("auth/setLogind", {
              'logind':false,
              'token':''
            });
        });        
      } catch (error) {
        console.log(error)
      }
      this.loading = false
    },
    regi: function() {
      this.$store.dispatch("auth/setShowRegist", {
        'showRegist':true
      });
    }
  }
}
</script>

<style lang="scss" scoped>
.login-container {
  background-color: #283443;
  min-height: 100vh;
  position: relative;

  .login-form {
    box-sizing: border-box;
    width: 500px;
    height: 400px;
    border-radius: 5px;
    padding: 60px;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background-color: #fff;
    .title-container {
      padding-bottom: 20px;
      .title {
        text-align: center;
      }
    }
    .set-language {
      position: absolute;
      top: 10px;
      right: 10px;
    }
    .txt {
        width: 100%;
        height: 38px;
        padding: 9px 10px;
        line-height: 38px;
        box-sizing: border-box;
        background: transparent;
        background-color: rgb(232, 240, 254);
        appearance: none;
        -webkit-appearance: none;
    }
    .txt:focus {
      outline: none;
    }
  }
}
</style>
