<template>
  <div class="auth-container">
    {{ authPage }}
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
import RegisterPage from '@/views/auth/register.vue'
import RegisterOTPQRPage from '@/views/auth/register_otp_qr.vue'
import Vue from 'vue';
import Component from 'vue-class-component';
import LoginPage from '@/views/auth/login.vue';

@Component({
  components: {
    LoginPage,
    RegisterPage,
    RegisterOTPQRPage,
  }
})
class AuthPage extends Vue {
  get authPage(): string | null {
    return this.$store.state.auth.authPage;
  }
}

export default AuthPage;
</script>

<style lang="scss" scoped>
.auth-container {
  background-color: #283443;
  min-height: 100vh;
  position: relative;
}
</style>
