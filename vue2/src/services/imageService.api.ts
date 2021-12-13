import { apiClient } from '@/services/base.api';
import { AxiosResponse } from 'axios';

// export interface LoginModel {
//   email: string;
//   password: string;
//   otp: string | number;
// }


class ImageServiceApi {


  // login(data: LoginModel): Promise<AxiosResponse<LoggedInModel>> {
  //   const formData = new FormData();
  //   formData.append('username', data.email); // email is username
  //   formData.append('password', data.password);
  //   formData.append('otp', String(data.otp));
  //   return apiClient.post('auth/login', formData, {
  //     headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
  //   });
  // }

}
/** Use 'new' here to create an instance, this instance is then what is exported
 *  This essentially makes the Service work as a Singleton when imported, since you are importing the instance */
export default new ImageServiceApi();
