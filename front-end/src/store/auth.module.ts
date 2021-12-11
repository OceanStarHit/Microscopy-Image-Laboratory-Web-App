// import { VuexModule, Module, Mutation, Action } from "vuex-module-decorators";
import { ActionContext, createStore, Store } from 'vuex'
import { InjectionKey } from 'vue'
import authService, {
  LoggedInModel,
  LoginModel,
  RegisteredModel,
  RegisterModel,
} from '@/services/authService'
import { AxiosResponse } from 'axios'

export enum AuthPage {
  loginPage = 'loginPage',
  registrationPage = 'registrationPage',
  otpQRPage = 'otpQRPage',
}

// store.ts

export interface User {
  id: string
  fullName: string
  email: string
  isAdmin: boolean
  isActive: boolean
  createdAtDate: Date
  lastLoginDate: Date
}

export interface OtpSecrets {
  secret: string
  uri: string
  uriQr: string
}

export interface AuthState {
  /** user
   * null if we failed to login or retrieve the user
   * undefined if we have not yet finished trying to retrieve it
   */

  user: User | null | undefined
  isLoggedIn: boolean
  token: string | null
  tokenType: string | null
  authPage: AuthPage | null
  otpSecrets: OtpSecrets | null
  errors: { [key: string]: string }[] // errors related to auth TODO
}

const initialState: AuthState = {
  user: undefined,
  isLoggedIn: sessionStorage.getItem('authToken') != null,
  token: sessionStorage.getItem('authToken'),
  tokenType: sessionStorage.getItem('authTokenType'),
  authPage: sessionStorage.getItem('authToken') ? null : AuthPage.loginPage,
  otpSecrets: null,
  errors: [],
}

// define injection key
export const key: InjectionKey<Store<AuthState>> = Symbol()

// @Module({namespaced: true})

export const authStore = createStore<AuthState>({
  state: {
    ...initialState,
  },
  actions: {
    logIn(
      context,
      data: LoginModel
    ): Promise<AxiosResponse<LoggedInModel> | void> {
      return authService
        .login(data)
        .then((response: AxiosResponse<LoggedInModel>) => {
          if (response.status === 200) {
            context.dispatch('loggedIn', {
              token: response.data.accessToken,
              tokenType: response.data.tokenType,
              user: response.data.user,
            })
            context.dispatch('setAuthPage', null)
            return response
          }
        })
        .catch((error: AxiosResponse) => {
          if (error.status === 401) {
            // context.dispatch("logOut");
          }
        })
    },

    register(
      context,
      data: RegisterModel
    ): Promise<AxiosResponse<RegisteredModel> | void> {
      return authService
        .register(data)
        .then((response) => {
          if (response.status === 201) {
            /* After successful registration user is logged in */
            context.dispatch('loggedIn', {
              token: response.data.accessToken,
              user: response.data.user,
            })
            /* set the otp secrets, should be deleted from state after showing QR code */
            context.commit('setAuthSecrets', {
              secret: response.data.otpSecret,
              uri: response.data.otpUri,
              qrSVG: response.data.otpUriQr,
            })
            /* then we show the QR code so that the user may save it */
            context.commit('setAuthPage', AuthPage.otpQRPage)
          }
        })
        .catch((error) => {
          /* Error with registration of user */
          context.dispatch('logOut')
          console.log(error)
          if (error.status === 401) {
            // context.dispatch("logOut");
          }
        })
    },
    logOut(context) {
      sessionStorage.removeItem('authToken')
      sessionStorage.removeItem('authTokenType')
      context.commit('setLoggedOut')
    },
  }, // END OF ACTIONS

  mutations: {
    loggedIn(state, data: LoggedInModel) {
      state.user = data.user
      state.token = data.accessToken
      state.tokenType = data.tokenType

      state.isLoggedIn = true
      state.authPage = null

      /* save token and token type in sessionStorage so it is not lost if we refresh */
      sessionStorage.setItem('authToken', data.accessToken)
      sessionStorage.setItem('authTokenType', data.tokenType)
    },

    registered(state, data: RegisteredModel) {
      state.user = data.user
      state.token = data.accessToken
      state.tokenType = data.tokenType

      state.otpSecrets = {
        secret: data.otpSecret,
        uri: data.otpUri,
        uriQr: data.otpUriQr,
      }

      state.isLoggedIn = true
      state.authPage = AuthPage.otpQRPage

      /* save token and token type in sessionStorage so it is not lost if we refresh */
      sessionStorage.setItem('authToken', data.accessToken)
      sessionStorage.setItem('authTokenType', data.tokenType)
    },

    loggedOut(state) {
      state.isLoggedIn = false
      state.token = null
      state.tokenType = null
      state.authPage = AuthPage.loginPage // go back to login page

      sessionStorage.removeItem('authToken')
      sessionStorage.removeItem('authTokenType')
    },

    deleteOTPSecrets(state) {
      state.otpSecrets = null
    },
  }, // end of mutations
})
