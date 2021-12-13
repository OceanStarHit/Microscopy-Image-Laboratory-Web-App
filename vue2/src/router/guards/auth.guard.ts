import store from '@/store'
import {Route} from 'vue-router';
import authService from '@/services/authService.api';

export default async (to: Route, from: Route, next: any) => {
    return await authService.getCurrentUser()
    .then((response) => {
        store.commit('auth/setUser', response.data);  /* update user with the current user */
        return next();  /* allow if user is logged in */
    })
    .catch(() => {
        /* not logged in
        *  logout and go to route to Auth view */
        store.dispatch('auth/logOut');
        return next('/auth')
    })
}


