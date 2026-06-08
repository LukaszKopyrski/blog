<template>
  <article id="login">
    <form id="login__form" @submit.prevent="submitLogin">
      <h2>Login</h2>
      <div v-if="error" class="error-message">{{ error }}</div>
      <input type="text" id="form__email" placeholder="Email" v-model="email" required>
      <input type="password" id="form__password" placeholder="Password" v-model="password" required>
      <button id="form__btn" type="submit">Login</button>
    </form>
    <router-link id="login__reset" to="/reset">Reset password</router-link>
  </article>
</template>

<script setup>
import {ref} from "vue"
import {useRouter} from "vue-router"
import { useAuthStore} from "@/store/auth.store";

const router = useRouter();
const auth = useAuthStore();

const email = ref("");
const password = ref("");
const error = ref("");


const submitLogin = async()=>{
  error.value = "";
  try {
    await auth.login({email:email.value, password:password.value});
    router.push("/");
  } catch (error) {
    const message = error?.response?.data?.error||error?.response?.data?.detail||"error";
    error.value = message;
  }
}
</script>

<style scoped>
#login {
  display: flex;
  flex-direction: column;
  align-items: center;
  color: white;
  height: 100vh;
}

#login__form {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  max-width: 400px;
  padding: 20px;
  border-radius: 8px;
}

#form__email, #form__password {
  width: 100%;
  padding: 10px;
  margin: 10px 0;
  border-radius: 8px;
  border: 1px solid #ccc;
  font-size: 1rem;
}

#form__btn, #login__reset {
  min-width: 270px;
  text-decoration: none;
  font-weight: 700;
  font-size: 1.6rem;
  padding: 5px;
  color: #fff;
  background-color: #008080;
  border-radius: 8px;
  border: 0;
  text-align: center;
  cursor: pointer;
}

.error-message {
  color: red;
  font-weight: bold;
}
</style>
