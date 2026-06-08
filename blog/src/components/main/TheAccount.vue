<template>
  <section class="main__account">
    <article class="account__user">
      <h2 class="user__header">Hello {{ account.username }} </h2>
      <ul class="user__data">
        <li class="data">email: {{ account.email }} <button @click="toggleVisibility('email')" v-if="!account.is_demo">Edit</button></li>
        <div v-if="emailEdit" class="data__edit email-edit">
          <input type="text" class="edit__input" v-model="email">
          <button class="edit__btn" @click="updateData('email', email)">Edit</button>
        </div>
        
        <li class="data">user name: {{ account.username }} <button @click="toggleVisibility('username')" v-if="!account.is_demo">Edit</button></li>
        <div v-if="usernameEdit" class="data__edit username-edit">
          <input type="text" class="edit__input" v-model="username">
          <button class="edit__btn" @click="updateData('username', username)">Edit</button>
        </div>
        
        <li class="data">admin: {{ account.is_staff }} </li>
        <li class="data">Account since: {{ account.date_joined }}</li>
      </ul>
      <div class="user__control" v-if="!account.is_demo">
        <router-link to="/reset" class="control__reset">Reset password</router-link>
        <button class="control__delete" @click="deleteAccount">Delete account</button>
      </div>
    </article>
  </section>
</template>

<script setup>
import {onMounted, ref} from "vue";
import {useRouter} from "vue-router";
import api from "@/api";
import { useAuthStore} from "@/store/auth.store";

const router = useRouter();
const auth = useAuthStore();

const account = ref({});
const email = ref("");
const username = ref("");

const emailEdit = ref(false);
const usernameEdit = ref(false);


const toggleVisibility = (which) =>{
  if(which === "email") emailEdit.value = !emailEdit.value
  if(which === "username") usernameEdit.value = !usernameEdit.value;
}

const getData=async()=>{
  const data = await api.get("/api/myaccount/").then(r => r.data);
  account.value = data;
  email.value = data.email;
  username.value = data.username;
}

const deleteAccount=async()=>{
  try {
    await api.delete("/api/myaccount/");
    alert("Account deleted");
    auth.clearAuth();
    router.push("/");
  } catch (error) {
    console.error("error deleting account:",error);
    alert("Error deleting account");
  }
}

const updateData=async(field,value)=>{
  try {
    await api.patch("/api/myaccount/",{[field]:value})
    account.value = {...account.value, [field]:value}
    alert(`Updated ${field}`);
  } catch (error) {
    console.error(`Error updating ${field}:`,error);
    alert(`Error updating ${field}`);
  }
}

onMounted(async()=>{
  try {
    await getData();
  } catch (error) {
    console.error("Error fetching data:",error);
    router.push("/login");    
  }
})

</script>

<style scoped>
.main__account {
  color: #dddedf;
}
.user__data {
  list-style-type: none;
}

.user__control {
  display: flex;
  flex-direction: column;
}


.control__reset {
  margin-top: 20px;
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
}
.control__delete {
  margin-top: 20px;
  min-width: 270px;
  text-decoration: none;
  font-weight: 700;
  font-size: 1.6rem;
  padding: 5px;
  color: #fff;
  background-color: #e71b1b;
  border-radius: 8px;
  border: 0;
  text-align: center;
}
</style>
