<template>
  <div class="login-container">
    <v-container
      ref="loginForm"
      :model="loginForm"
      :rules="loginRules"
      class="inner-container"
      auto-complete="on"
      label-position="left"
      :validate-on-rule-change="false"
    >
      <div class="title-container">
        <h3 class="title">{{ "Login" }}</h3>
      </div>

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

      <v-col prop="totp">
        <label>Totp</label>
        <input
          v-model="loginForm.otp"
          class="txt"
          type="text"
          name="otp"
          auto-complete="false"
        />
      </v-col>

      <v-col>
        <button
          :loading="loading"
          type="primary"
          size="large"
          style="width: 100%; height: 50px; margin-bottom: 3px; background: lightblue; border-radius: 2px;"
          @click="handleLogin"
        >
          {{ "Login" }}
        </button>
        <a style="float:right;" @click="showRegistration">Switch to register</a>
      </v-col>
    </v-container>
  </div>
</template>

<script>
export default {
  name: "LoginPage",
  components: {},
  data() {
    return {
      loginForm: { email: "", password: "", otp: "" },
      loginRules: {
        email: [
          {
            required: true,
            trigger: "blur",
            message: "Email"
          }
        ],
        password: [
          {
            required: true,
            trigger: "blur",
            message: "Password"
          }
        ],
        otp: [
          {
            required: true,
            trigger: "blur",
            message: "otp"
          }
        ]
      },
      loading: false
    };
  },
  computed: {},
  methods: {
    async handleLogin() {
      this.loading = true;
      await this.$store.dispatch("auth/logIn", this.loginForm);
    },
    showRegistration: function() {
      this.$store.dispatch("auth/setAuthPage", "registrationPage");
    }
  }
};
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
