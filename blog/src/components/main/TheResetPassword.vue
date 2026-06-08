<template>
    <article id="reset">
      <form id="reset__form" @submit.prevent="resetPassword">
        <h2 id="form__title">Reset password</h2>
        <span id="form__error">{{ validationError }}</span>
  
        <label for="form__email" class="form__label">Email:</label>
        <input type="text" id="form__email" v-model="email" />
  
        <label for="form__answer" class="form__label">Answer used to reset your password (name of your first pet)</label>
        <input type="text" id="form__answer" v-model="answer" />
  
        <label for="form__password" class="form__label">Password:</label>
        <input type="password" id="form__password" v-model="password" />
  
        <input type="submit" value="Reset password" id="form__btn" />
      </form>
    </article>
</template>
  
<script setup>
import {ref} from "vue";
import {useRouter} from "vue-router";
import api from "@/api";
import { useAuthStore } from "@/store/auth.store";

const router = useRouter();

const auth = useAuthStore()

const email = ref("");
const answer = ref("");
const password = ref("");
const validationError = ref("");



const resetPassword=async()=>{
  validationError.value = "";

  if(!email.value || !answer.value || !password.value){
    validationError.value = "All fields are required";
    return
  }

  const resetData = {
    email:email.value,
    answer:answer.value,
    new_password:password.value,
  };

  try {
    await api.patch("/api/resetpassword/",resetData);
    email.value ="";
    answer.value ="";
    password.value ="";

    await auth.logout();
    alert("Password updated");
    router.push("/login");
  } catch (error) {
    validationError.value = "Password change failed. Verify your data";
  }
}
</script>
  
<style scoped>
#reset {
    display: flex;
    flex-direction: column;
    align-items: center;
    color: white;
}

#reset__form {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    max-width: 400px;
    padding: 20px;
    border-radius: 8px;
}

#form__email, #form__answer, #form__password {
    width: 100%;
    padding: 10px;
    margin: 10px 0;
    border-radius: 8px;
    border: 1px solid #ccc;
    font-size: 1rem;
}
.form__label{
  font-weight: 700;
}
#form__btn,#login__reset  {
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
    cursor:pointer;
}

#form__error {
  color: red;
  font-weight: bold;
}
</style>