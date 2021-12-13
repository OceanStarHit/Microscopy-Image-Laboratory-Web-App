<template>
  <div class="otp-qr-container">
    <v-container
      class="inner-container"
      label-position="left"
    >
      <div class="title-container">
        <h3 class="title">
          {{ '2 Factor Authorization QR Code' }}
        </h3>
        <p>
          Please use an Authorization application to save this QR code, you will use the
          authorization code given by your app to log in
        </p>
      </div>

      <v-col>
        <div
          class="d-flex justify-center"
          v-html="otpSecrets.qrSVG"
        />
      </v-col>

      <v-col>
        <p>Secret:</p>
        <p>{{ otpSecrets.secret }}</p>
      </v-col>

      <v-col>
        <label />
        <button
          type="primary"
          size="large"
          style="
            width: 100%;
            height: 50px;
            margin-bottom: 30px;
            background: lightblue;
            border-radius: 2px;
          "
          @click="handleContinue"
        >
          Continue
        </button>
      </v-col>
    </v-container>
  </div>
</template>

<script lang="ts">
  import Vue from 'vue';
  import Component from 'vue-class-component';
  import { OtpSecrets } from '@/store/auth.module'

  @Component({
    // layout: 'login',
  })
  export default class RegisterOTPQRPage extends Vue {
    get otpSecrets(): OtpSecrets | null {
      return this.$store.state.auth.otpSecrets
    }

    handleContinue(): void {
      this.$store.dispatch('auth/changeAuthPage', null)
      this.$store.commit('auth/deleteOTPSecrets')
    }
  }

</script>

<style lang="scss" scoped>
  .otp-qr-container {
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
        p {
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
