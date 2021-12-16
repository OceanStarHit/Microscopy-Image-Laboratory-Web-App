import store from '@/store'
import {Route} from 'vue-router';
import authService from '@/services/authService.api';

export default async (to: Route, from: Route, next: any) => {
    /** Guard made specifically for the Auth View with the purpose to redirect back to the main page if the user
     * is already logged in
     */

    return await authService.getCurrentUser()
        .then(() => {
            return next('/')  /* route to main if user is logged in */
        })
        .catch(() => {
            return next() /* allow route to auth if not logged in */
        })
}


