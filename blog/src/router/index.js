import { createRouter, createWebHashHistory } from 'vue-router'
import TheAllPosts from "@/components/main/TheAllPosts"
import TheLoginView from "@/views/main/TheLoginView"
import TheRegisterView from "@/views/main/TheRegisterView"
import TheAccountView from "@/views/main/TheAccountView"
import TheResetPasswordView from "@/views/main/TheResetPasswordView"
const routes = [
  {
    path: '/',
    name: 'PostList',
    component:TheAllPosts
  },
  {
    path:'/login',
    name:"Login",
    component:TheLoginView
  },
  {
    path:'/register',
    name:'Register',
    component:TheRegisterView
  },
  {
    path:'/account',
    name:'Account',
    component:TheAccountView
  },
  {
    path:'/reset',
    name:'Reset',
    component:TheResetPasswordView
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
