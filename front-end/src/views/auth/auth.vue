<template>
  <div class="auth-container">
    <v-app v-if="authPage === 'loginPage'">
      <LoginPage />
    </v-app>
    <v-app v-else-if="authPage === 'registrationPage'">
      <RegisterPage />
    </v-app>
    <v-app v-else-if="authPage === 'otpQRPage'">
      <RegisterOTPQRPage />
    </v-app>
  </div>
</template>

<script lang="ts">
  import { Options, Vue } from 'vue-class-component'
  import LoginPage from './login.vue'
  import { AuthPageEnum } from '@/store/auth.module'
  import RegisterPage from '@/views/auth/register.vue'
  import RegisterOTPQRPage from '@/views/auth/register_otp_qr.vue'

  @Options({
    components: {
      LoginPage,
      RegisterPage,
      RegisterOTPQRPage,
    },
  })
  export default class AuthPage extends Vue {
    get authPage(): AuthPageEnum | null {
      return this.$store.state.auth.authPage
    }
  }
</script>

<style lang="scss" scoped>
  .auth-container {
    background-color: #283443;
    min-height: 100vh;
    position: relative;
  }
</style>
