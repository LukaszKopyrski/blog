<template>
  <nav id="nav">
    <div id="nav__list">
      <router-link to="/" class="list__element">Posts</router-link>
      <router-link v-if="!auth.isLoggedIn" to="/login" class="list__element">Login</router-link>
      <router-link v-if="!auth.isLoggedIn" to="/register" class="list__element">Register</router-link>
      <router-link v-if="auth.isLoggedIn" to="/account" class="list__element">{{ auth.username }}</router-link>
      <router-link v-if="auth.isLoggedIn" to="/" class="list__element" @click="handleLogout">Logout</router-link>
    </div>

    <TheBurger id="burger" @click="toggleMobileMenu"></TheBurger>
    <TheMobileNav id="menu"></TheMobileNav>
  </nav>
</template>

<script setup>
import { onMounted, onBeforeUnmount } from 'vue';
import {useRouter} from "vue-router";
import { useAuthStore } from '@/store/auth.store';

import TheBurger from './TheBurger.vue';
import TheMobileNav from './TheMobileNav.vue';

const router = useRouter();
const auth = useAuthStore();


const handleLogout = async()=>{
  await auth.logout();
  router.push("/")
}
const showBurger=()=>{
  const navList = document.querySelector("#nav__list");
  const burger = document.querySelector("#burger");
  const menu = document.querySelector("#menu");

  if(window.innerWidth>1200){
    navList.style.display = "flex";
    burger.style.display = "none";
    menu.style.display = "none";
  }else{
    navList.style.display = "none";
    burger.style.display = "block";
  }
}

const toggleMobileMenu=()=>{
  const menu = document.querySelector("#menu");
  menu.style.display = menu.style.display ==="flex"?"none":"flex";
}

onMounted(()=>{
  showBurger();
  window.addEventListener("resize",showBurger);
});

onBeforeUnmount(()=>{
  window.removeEventListener("resize", showBurger);
})
</script>

<style scoped>
#nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

#nav__list {
  display: flex;
  gap: 10px;
  margin-right: 20px;

}

.list__element {
  text-decoration: none;
  font-weight: 700;
  padding: 5px;
  color: #2c3e50;
  background-color: #d4d3d3;
  border-radius: 8px;
}

#menu {
  display: none;
}

#burger {
  display: block;
}

#close {
  font-weight: 900;
  font-size: 50px;
  display: none;
  justify-content: end;
}
</style>
