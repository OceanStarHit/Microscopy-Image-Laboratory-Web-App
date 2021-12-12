<template>
  <div class="login-container">
    <v-container
      ref="registerForm"
      :model="registerForm"
      class="inner-container"
      auto-complete="on"
      label-position="left"
    >
      <!-- 设置语言 -->

      <div class="title-container">
        <h3 class="title">{{ 'Register New User' }}</h3>
      </div>

      <v-col prop="name">
        <label>Full Name</label>
        <input
          v-model="registerForm.fullName"
          name="fullName"
          type="text"
          auto-complete="on"
          class="txt"
        />
      </v-col>

      <v-col prop="email">
        <label>Email</label>
        <input
          v-model="registerForm.email"
          name="email"
          type="text"
          auto-complete="on"
          class="txt"
        />
      </v-col>

      <v-col prop="password">
        <label>Password</label>
        <input
          v-model="registerForm.password"
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
          v-model="registerForm.passwordRepeat"
          class="txt"
          type="password"
          name="password_repeat"
          auto-complete="on"
          show-password
        />
      </v-col>

      <v-col>
        <label></label>
        <button
          :loading="loading"
          type="primary"
          size="large"
          style="
            width: 100%;
            height: 50px;
            margin-bottom: 30px;
            background: lightblue;
            border-radius: 2px;
          "
          @click="handleRegistration"
        >
          {{ 'Create Account' }}
        </button>
        <a style="float: right" @click="showLoginPage">Switch to login</a>
      </v-col>
    </v-container>
  </div>
</template>

<script lang="ts">
  import { Options, Vue } from 'vue-class-component'
  import { AuthPageEnum } from '@/store/auth.module'
  import { RegisterModel } from '@/services/authService'

  @Options({})
  export default class RegisterPage extends Vue {
    // registerFormRules = {
    //   email: [
    //     {
    //       required: true,
    //       trigger: 'blur',
    //       message: 'Email',
    //     },
    //   ],
    //   password: [
    //     {
    //       required: true,
    //       trigger: 'blur',
    //       message: 'Password',
    //     },
    //   ],
    // }

    get registerForm() {
      return {
        fullName: '',
        email: '',
        password: '',
        passwordRepeat: '',
      }
    }

    handleRegistration(): void {
      if (
        this.registerForm.password === '' ||
        this.registerForm.password !== this.registerForm.passwordRepeat
      ) {
        return
      }
      /* exclude password_repeat from registrationData */
      // eslint-disable-next-line @typescript-eslint/no-unused-vars
      const { passwordRepeat, ...registrationData } = this.registerForm

      const data: RegisterModel = { ...registrationData } // for type checking RegisterModel
      this.$store.dispatch('auth/register', data)
    }

    showLoginPage(): void {
      this.$store.dispatch('auth/changeAuthPage', AuthPageEnum.loginPage)
    }
  }
</script>

<style lang="scss" scoped>
  .login-container {
    background-color: #283443;
    min-height: 100vh;
    position: relative;

    .inner-container {
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
