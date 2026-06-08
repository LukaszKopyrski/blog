<template>
  <article class="posts__post" v-if="localpost">
    <div class="post__header">
      <h2 class="header__title">{{ localpost.title }}</h2>
      <span class="header__theme">{{ localpost.topic }}</span>
    </div>
    <div class="post__main">
      <div class="main__info">
        <span class="info__author">{{ localpost.username }}</span>
        <span class="info__date">{{ localpost.date }}</span>
      </div>
      <p class="main__content">{{ localpost.content }}</p>
    </div>
    <div class="post__input">
      <div class="input__score">
        <button class="btn score__plus" @click="addScore" v-if="!checkScore() && auth.isLoggedIn">+ </button>
        {{ localpost.score }}
        <button class="btn score__minus" @click="deleteScore" v-if="checkScore() && auth.isLoggedIn">- </button>
      </div>  
      <input type="button" class="input__btn" :value="toggleComment" @click="controlComments">
      <div class="input__comment">
        <input type="text" class="comment__field">
        <input type="button" class="comment__add" value="Add comment">
      </div>
      <div class="post__control">
        <button id="control__edit" v-if="localpost.is_author && auth.isLoggedIn" @click="editPost">Edit</button>
        <button id="control__delete" v-if="(localpost.is_staff || localpost.is_author) && auth.isLoggedIn" @click="deletePost">Delete</button>
      </div>
    </div>
    <TheAllComments v-if="showComments" :postid="localpost.id" class="post__comment"/>
  </article>
</template>

<script setup>
import {ref, onMounted, watch} from "vue";
import api from "@/api";
import TheAllComments from "./TheAllComments.vue";
import { useAuthStore } from "@/store/auth.store";
import { usePostStore } from "@/store/post.store";
import { useCommentStore } from "@/store/comment.store";
import { useReplyStore } from "@/store/reply.store";

const props = defineProps({
    postId:{
        type:Number,
        required:true,
    },
});

const auth = useAuthStore();
const postStore = usePostStore();
const commentStore = useCommentStore();
const replyStore = useReplyStore();

const localpost = ref(null);
const showComments = ref(false);
const toggleComment = ref("Comments");


const getPost=async()=>{
  try {
    const response = await api.get(`/api/post/${props.postId}`);
    localpost.value = response.data;
  } catch (error) {
    console.error("Error fetching post:",error);
  }
}

const checkScore=()=>{
  return localpost.value?.scores?.some(score=>score.username===auth.username);
}

const addScore=async()=>{
  try {
    await api.post(`/api/addpostscore/${localpost.value.id}/`);
    await getPost();
  } catch (error) {
    console.error("Error adding score:",error);
  }
}

const deleteScore=async()=>{
  try {
    await api.delete(`/api/deletepostscore/${localpost.value.id}/${auth.username}/`);
    await getPost();
  } catch (error) {
    console.error("Error deleting score:", error);
  }
}

const deletePost=async()=>{
  try {
    await api.delete(`/api/post/${localpost.value.id}/`);
    postStore.setTriggered(true);
  } catch (error) {
    console.error("Error deleting post:",error);
  }
}

const controlComments=()=>{
  showComments.value = !showComments.value;
  toggleComment.value = showComments.value ? "Hide":"Comments";
}

const editPost=()=>{
  postStore.openEdit(localpost.value);
}

watch(
  ()=>postStore.isTriggered,
  async (newVal)=>{
    if(newVal){
      await getPost();
    }
  }
);

watch(
  ()=>commentStore.isDeletingComment,
  async (newVal)=>{
    if(newVal){
      await getPost();
    }
  }
);

watch(
  ()=>replyStore.isDeletingReply,
  async (newVal)=>{
    if(newVal){
      await getPost();
    }
  }
);

onMounted(()=>{
  getPost();
});
</script>

<style scoped>
.posts__post{
    margin-bottom: 30px;
    margin: 5px;
    background-color: #dddedf;
    width: 90vw;
    padding: 5px;
    border-radius: 8px;
}
.post__header{
    grid-column: 1/-1;
    display: flex;
    justify-content: space-between;
    align-items: baseline;
}
.post__main{
    padding-top: 16px;
    padding-left: 5px;
    grid-column: 1/-1;
}
.main__info{
    grid-column: 1/-1;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
}
.post__input{
    display: grid;
    grid-template-columns: repeat(4,1fr);
    display: flex;
    justify-content: space-between;
    width: 100%;
}
.comment__field{
    border-radius: 8px;
    grid-row: 2/3;
}
.post__btn{
    grid-column: 1/-1;
    display: flex;
    justify-content: center;
    margin-top: 30px;
}
.input__comment{
  display: none;
}
.input__btn,.comment__add,#control__edit,#control__delete{
    text-decoration: none;
    font-weight: 900;
    padding: 5px;
    background-color: #2c3e50;
    color: #d4d3d3;
    border-radius: 8px;
    border: 0;
    margin-left: 5px;
}
.btn{
    width: 30px;
    height: 30px;
    border-radius: 15px;
    border: none;
}
.report__btn{
    text-decoration: none;
    font-weight: 600;
    padding: 5px;
    color: #ffffff;
    background-color: #da4646;
    border-radius: 8px;
}
</style>
