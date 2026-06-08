<template>
   <nav>
    <router-link to="/" class="list__element">Posts</router-link>
      <router-link v-if="!auth.isLoggedIn" to="/login" class="list__element">Login</router-link>
      <router-link v-if="!auth.isLoggedIn" to="/register" class="list__element">Register</router-link>
      <router-link v-if="auth.isLoggedIn" to="/account" class="list__element">{{ auth.username }}</router-link>
      <router-link v-if="auth.isLoggedIn" to="/" class="list__element" @click="handleLogout">Logout</router-link>
   </nav>
</template>


<script setup>
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/store/auth.store';

const router = useRouter();
const auth = useAuthStore();



const handleLogout=async()=>{
  try {
    await auth.logout();
    router.push("/");
  } catch (error) {
    console.error("Error ",error)
  }
}
</script>

<style scoped>
nav{
 font-size: 1.2rem;
 display: flex;
 flex-direction: column;
 z-index: 1;
 gap: 10px;

}
.list__element{
    text-decoration: none;
    font-weight: 700;
    padding: 5px;
    color: #2c3e50;
    background-color: #d4d3d3;
    border-radius: 8px;


}
</style>

