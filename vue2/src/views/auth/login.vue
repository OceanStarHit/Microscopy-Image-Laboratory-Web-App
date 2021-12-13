<template>
  <div class="login-container">
    <v-container
      ref="loginForm"
      :model="loginForm"
      class="inner-container"
      auto-complete="on"
      label-position="left"
    >
      <div class="title-container">
        <h3 class="title">
          {{ 'Login' }}
        </h3>
      </div>

      <v-col prop="email">
        <label>Email</label>
        <input
          v-model="loginForm.email"
          name="email"
          type="text"
          auto-complete="on"
          class="txt"
        >
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
        >
      </v-col>

      <v-col prop="totp">
        <label>Totp</label>
        <input
          v-model="loginForm.otp"
          class="txt"
          type="text"
          name="otp"
          auto-complete="false"
        >
      </v-col>

      <v-col>
        <button
          type="primary"
          size="large"
          style="
                width: 100%;
                height: 50px;
                margin-bottom: 3px;
                background: lightblue;
                border-radius: 2px;
              "
          @click="handleLogin"
        >
          {{ 'Login' }}
        </button>
        <a
          style="float: right"
          @click="showRegistration"
        >Switch to register</a>  
      </v-col>
    </v-container>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import Component from 'vue-class-component';
import {LoggedInModel, LoginModel} from '@/services/authService.api';
import {AxiosResponse} from 'axios';
import router from '@/router';

@Component({})
class LoginPage extends Vue {
  get loginForm() {
    return {
      email: '',
      password: '',
      otp: ''
    };
  }
  handleLogin() {
    const loginData: LoginModel = { ...this.loginForm };
    this.$store.dispatch('auth/logIn', loginData)
      .then((response: AxiosResponse<LoggedInModel>) => {
        if (response.data) {
          router.push('/'); /* successful login so route to main */
        }
      })
      // .catch(() => router.push('/auth'))
  }

  showRegistration() {
    this.$store.dispatch('auth/changeAuthPage', 'registrationPage');
  }
}
export default LoginPage;
</script>

<style lang="scss" scoped>
.login-container {
  background-color: #283443;
  min-height: 100vh;
  position: relative;

  .inner-container {
    box-sizing: border-box;
    width: 500px;
    height: 500px;
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
