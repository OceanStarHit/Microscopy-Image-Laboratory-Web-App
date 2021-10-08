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
        <h3 class="title">{{ 'Register' }}</h3>
      </div>

      <v-col prop="name">
        <label>Name</label>
        <input
          v-model="loginForm.name"
          name="name"
          type="text"
          auto-complete="on"
          class="txt"
        />
      </v-col>

      <v-col prop="email">
        <label>Email</label>
        <input
          v-model="loginForm.email"
          name="email"
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

      <v-col prop="password">
        <label>Confirm Password</label>
        <input
          v-model="loginForm.password1"
          class="txt"
          type="password"
          name="password1"
          auto-complete="on"
          show-password
        />
      </v-col>

    <v-col >
      <label></label>
      <button
        :loading="loading"
        type="primary"
        size="large"
        @click="handleRegist"
        style="width: 100%; height: 50px; margin-bottom: 30; background: lightblue; border-radius: 2px;"
      >
        {{ 'Create Account' }}
      </button>
      <a style="float:right;" @click="toLogin">Switch to login</a>
      </v-col>
    </v-container>
  </div>
</template>

<script>
// import { mapGetters, mapActions } from 'vuex'
import * as API from "../../api/auth";

export default {
  name: 'RegistPage',
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
            message: 'Account'
          }
        ]
      },
      loading: false
    }
  },
  computed: {
  },
  methods: {
    async handleRegist() {
        if (this.loginForm.password == '' || this.loginForm.password != this.loginForm.password1) {
            this.$message({content:"Passwords do not match!",type:"warn"}).show();
            return;
        }
        try {
            this.loading = true
            API.regist(this.loginForm).then(response => {
                console.log(response);
            }).catch(error => {
                console.error(error);
            });        
        } catch (error) {
            console.log(error)
        }
        this.loading = false
    },
    toLogin() {
      this.$store.dispatch("auth/setShowRegist", {
        'showRegist':false
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
    height: 600px;
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
