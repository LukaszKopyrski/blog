import {defineStore} from "pinia";
import { authService } from "../api/auth.service";

export const useAuthStore = defineStore('auth',{
    state:()=>({
        user:null,
        ready:false,
    }),
    getters:{
        isLoggedIn: (s)=>!!s.user,
        username:(s) => s.user?.username || "",
    },
    actions:{
        async init(){
            try{
                this.user = await authService.myaccount();
            }catch{
                this.user = null;
            }finally{
                this.ready = true;
            }
        },
        async login(payload){
            await authService.login(payload);
            this.user = await authService.myaccount();
        },
        async logout(){
            try {await authService.logout();}
            finally {this.user = null}
        },
        async clearAuth(){
            this.isLoggedIn = false;
            this.username = null;
            this.user = null;
        }
    },
});