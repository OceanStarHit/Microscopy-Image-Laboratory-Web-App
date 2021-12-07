<template>
  <div class="login-container">
    <v-container
      ref="registerForm"
      :model="registerForm"
      :rules="registerFormRules"
      class="inner-container"
      auto-complete="on"
      label-position="left"
      :validate-on-rule-change="false"
    >
      <!-- 设置语言 -->

      <div class="title-container">
        <h3 class="title">{{ "Register New User" }}</h3>
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
          v-model="registerForm.password_repeat"
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
          @click="handleRegistration"
          style="width: 100%; height: 50px; margin-bottom: 30px; background: lightblue; border-radius: 2px;"
        >
          {{ "Create Account" }}
        </button>
        <a style="float:right;" @click="showLoginPage">Switch to login</a>
      </v-col>
    </v-container>
  </div>
</template>

<script>
// import { mapGetters, mapActions } from 'vuex'
import * as API from "../../api/auth";

export default {
  name: "RegistrationPage",
  components: {},
  data() {
    return {
      registerForm: {
        fullName: "",
        email: "",
        password: "",
        password_repeat: ""
      },
      registerFormRules: {
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
        ]
      },
      loading: false
    };
  },
  computed: {},
  methods: {
    async handleRegistration() {
      if (
        this.registerForm.password === "" ||
        this.registerForm.password !== this.registerForm.password_repeat
      ) {
        this.$message({
          content: "Passwords do not match!",
          type: "warn"
        }).show();
        return;
      }
      /* exclude password_repeat from registrationData */
      const { password_repeat, ...registrationData } = this.registerForm;

      this.$store.dispatch("auth/registerUser", registrationData);
    },
    showLoginPage() {
      this.$store.dispatch("auth/setAuthPage", "loginPage");
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
