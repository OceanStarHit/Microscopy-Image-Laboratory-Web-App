import { apiClient } from '@/services/base'
import { AxiosResponse } from 'axios'
import { User } from '@/store/auth.module'

export interface LoginModel {
  email: string
  password: string
  otp: string | number
}

export interface RegisterModel {
  fullName: string
  email: string
  password: string
}

export interface LoggedInModel {
  user: User
  accessToken: string
  tokenType: string
}

export interface RegisteredModel {
  user: User
  accessToken: string
  tokenType: string
  otpSecret: string
  otpUri: string
  otpUriQr: string
}

class AuthService {
  // private static instance: AuthService;
  // //Assign "new AuthApiService()" here to avoid lazy initialisation
  //
  // constructor() {
  //   if (AuthService.instance) {
  //     return AuthService.instance;
  //   }
  //
  //   AuthService.instance = this;
  // }

  login(data: LoginModel): Promise<AxiosResponse<LoggedInModel>> {
    const formData = new FormData()
    formData.append('username', data.email) // email is username
    formData.append('password', data.password)
    formData.append('otp', String(data.otp))
    return apiClient.post('auth/login', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    })
  }

  register(data: RegisterModel): Promise<AxiosResponse<RegisteredModel>> {
    return apiClient.post('auth/register', data)
  }
}

export default new AuthService()
