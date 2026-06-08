<template>
  <div class="panel">
    <button type="button" class="panel__close" @click="$emit('close')">X</button>

    <form class="panel__form" @submit.prevent="sendPost">
      <h3>Title</h3>
      <input type="text" class="form__input" v-model="title">
      <h3>Topic</h3>
      <input type="text" class="form__input" v-model="topic">
      <h3>Content</h3>
      <textarea class="form__input" rows="6" v-model="content"></textarea>
      <br>
      <div v-if="validationError" class="error-message">{{ validationError }}</div>
      <div class="panel__btn">
        <button type="submit" class="btn__add">Add post</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import {ref} from "vue";
import api from "@/api";
import { usePostStore } from "@/store/post.store";

const emit = defineEmits(["close","created"]);

const title = ref("");
const topic = ref("");
const content = ref("");
const validationError = ref("");
const loading = ref(false);

const postStore = usePostStore();


const sendPost=async()=>{
  validationError.value="";
  loading.value=true;

  const postData={
    title:title.value,
    topic:topic.value,
    content:content.value
  };

  try {
    await api.post("/api/posts/",postData);

    title.value="";
    topic.value="";
    content.value="";

    postStore.setIsAddPost(true);

    emit("created");
    emit("close");
  } catch (error) {
    const responseData = error?.response?.data;
    if(responseData?.title){
      validationError.value = responseData.title[0];
    }else if(responseData?.topic){
      validationError.value = responseData.topic[0];
    }else if(responseData?.content){
      validationError.value = responseData.content[0];
    }else{
      validationError.value = "Error adding post";
    }
    console.error("Error:",error);
  }finally{
    loading.value=false;
  }
}
</script>

<style scoped>
.panel__close {
  width: 30px;
  height: 30px;
  border-radius: 15px;
  border: none;
  margin-right: 20px;
}
.panel {
  position: fixed;
  bottom: 50px;
  left: 0;
  background-color: #d4d3d3;
  width: 100%;
  padding: 3px;
  border-radius: 8px;
  display: flex;
  justify-content: center;
}
.panel__form{
 text-align: center;
}

.form__input {
  width: 90vw;
  border-radius: 6px;
  border: 0;
}
textarea {
  resize: none;
}
.panel__btn {
  width: 100%;
  display: flex;
  justify-content: center;
}
.btn__add {
  background-color: #2c3e50;
  border: none;
  padding: 10px;
  border-radius: 8px;
  color: #d4d3d3;
  font-weight: 900;
}
.error-message {
  color: black;
  font-weight: bold;
  text-align: center;
  margin-bottom: 10px;
}
</style>