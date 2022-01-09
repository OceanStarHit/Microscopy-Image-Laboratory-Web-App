<template>
  <div class="auth-container">
    <h1>{{ authPage }}</h1>
    <v-app v-if="authPage === 'loginPage'">
      <LoginPage />
    </v-app>
    <v-app v-else-if="authPage === 'registrationPage'">
      <RegistrationPage />
    </v-app>
    <v-app v-else-if="authPage === 'otpQRPage'">
      <RegisterOTP_QR_Page />
    </v-app>
  </div>
</template>

<script>
import { mapGetters, mapActions, mapState } from "vuex";
import LoginPage from "@/components/auth/login";
import RegistrationPage from "@/components/auth/register";
import RegisterOTP_QR_Page from "@/components/auth/register_otp_qr";

export default {
  name: "AuthPage",
  components: {
    LoginPage,
    RegistrationPage,
    RegisterOTP_QR_Page
  },
  computed: {
    ...mapState({
      authPage: state => state.auth.authPage
    })
  },
  methods: {}
};
</script>

<style lang="scss" scoped>
.auth-container {
  background-color: #283443;
  min-height: 100vh;
  position: relative;
}
</style>
