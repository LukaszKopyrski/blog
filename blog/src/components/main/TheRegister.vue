<template>
  <article id="register">
    <form id="register__form" @submit.prevent="register">
      <h2 id="form__title">Register</h2>
      <span id="form__error">{{ validationError }}</span>
      <span id="form__info">This is a local demo project. Please do not enter real personal data. Demo accounts credentials can be found in the README.md file</span>
      <label for="form__name" class="form__label">User name:</label>
      <input type="text" id="form__name" v-model="username" />

      <label for="form__answer" class="form__label">Answer used to reset your password (name of your first pet)</label>
      <input type="text" id="form__answer" v-model="answer" />

      <label for="form__email" class="form__label">Email:</label>
      <input type="text" id="form__email" v-model="email" />

      <label for="form__password" class="form__label">Password:</label>
      <input type="password" id="form__password" v-model="password" />

      <input type="submit" value="Create account" id="form__btn" />
    </form>
  </article>
</template>

<script setup>
import {ref} from "vue";
import {useRouter} from "vue-router";
import api from "@/api";

const router = useRouter();

const email = ref("");
const username = ref("");
const answer = ref("");
const password = ref("");
let validationError = ref("");



const register=async()=>{
  const registrationData = {
        username: username.value,
        email: email.value,
        answer: answer.value,
        password: password.value,
      };
      validationError.value = "";
      try {
        await api.post("/api/register/", registrationData);
        alert('Account successfully created');
        router.push('/');
      } catch (error) {
        const responseData = error?.response?.data;
        if (responseData?.username) {
            validationError.value = responseData.username[0];
          } else if (responseData?.email) {
            validationError.value = responseData.email[0];
          } else if(responseData?.answer){
            validationError.value = responseData.answer[0];
          }else if (responseData?.password) {
            validationError.value = responseData.password[0];
          } else {
            validationError.value = 'Error creating account. Please check the data below';
          }
      }
}
</script>

<style scoped>
#register__form {
  width: 100%;
  height: 100vh;
  display: flex;
  align-items: center;
  flex-direction: column;
  row-gap: 10px;
}

#form__name, #form__answer, #form__email, #form__password {
  width: 100%;
  padding: 10px;
  margin: 10px 0;
  border-radius: 8px;
  border: 1px solid #ccc;
  font-size: 1rem;
}

#form__error,#form__info {
  color: rgb(255, 145, 0);
  font-weight: 900;
  text-align: center;
}

#form__title {
  color: #e7e6e6;
}

.form__label {
  color: #e7e6e6;
  font-weight: 900;
  min-width: 270px;
  text-align: center;
}

#form__btn {
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
</style>
