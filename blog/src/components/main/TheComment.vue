<template>
    <article id="comments__comment">
        <div class="comment__info">
            <span class="info__author">{{ localComment.username }}</span>
            <span class="info__date">{{ localComment.date }}</span>
        </div>
        <div class="comment__main">
            <p class="main__content">{{ localComment.content }}</p>
        </div>
        <div class="comment__input">
            <span class="input__score">
                <button class="btn score__plus" @click="addScore" v-if="!checkScore() && auth.isLoggedIn">+</button>
                {{ localComment.score }}
                <button class="btn score__minus" @click="deleteScore" v-if="checkScore() && auth.isLoggedIn">-</button>
            </span>
            <div class="input__reply">
                <button class="reply__btn" @click="toggleReplies">{{ showRepliesText }}</button>
            </div>
            <div class="comment__control">
                <button id="control__edit" v-if="localComment.is_author && auth.isLoggedIn" @click="editComment">Edit</button>
                <button id="control__delete" v-if="(localComment.is_staff || localComment.is_author) && auth.isLoggedIn" @click="deleteComment">Delete</button>
            </div>
        </div>
        <TheAllReplies :commentid="localComment.id" class="comment__reply" v-show="showReplies"/>
    </article>
</template>
  
<script setup>
import {ref, computed, watch} from "vue";
import api from "@/api";
import TheAllReplies from "./TheAllReplies.vue";
import { useAuthStore } from "@/store/auth.store";
import { useCommentStore } from "@/store/comment.store";

const props = defineProps({
    comment:{
        type:Object,
        required:true,
    },
});
const emit = defineEmits(["edit-comment"]);
const auth = useAuthStore();
const commentStore = useCommentStore();

const showReplies = ref(false);
const localComment = ref({...props.comment});

watch(
    ()=>props.comment,
    (newComment) =>{
        localComment.value = {...newComment};
    },
    {deep:true}
);

const showRepliesText = computed(()=>{
    return showReplies.value ? "Hide":"Replies";
});

const toggleReplies =()=>{
    showReplies.value = !showReplies.value;
}

const editComment =()=>{
    commentStore.setEditComment(true,localComment.value.id);
    emit("edit-comment",localComment.value.id);
}

const getComment=async()=>{
    try {
        const response = await api.get(`/api/comment/${localComment.value.id}/`);
        localComment.value = response.data;
    } catch (error) {
        console.error("Error fetching comment:",error);
    }
}

const checkScore=()=>{
    return localComment.value?.scores?.some((score)=>score.username===auth.username);
}

const addScore=async()=>{
  try {
    await api.post(`/api/addcommentscore/${localComment.value.id}/`);
    await getComment();
  } catch (error) {
    console.error("Error adding score:",error);
  }
}

const deleteScore=async()=>{
    try {
        await api.delete(`/api/deletecommentscore/${localComment.value.id}/${auth.username}/`);
        await getComment();
    } catch (error) {
        console.error("Error deleting score:",error);
    }
}

const deleteComment=async()=>{
    try {
        await api.delete(`/api/comment/${localComment.value.id}/`);
        commentStore.setDeletingComment(true);
    } catch (error) {
        console.error("Error deleting comment:",error);
    }
}
</script>
  
<style scoped>
  #comments__comment {
    background-color: #c6c7c7;
    grid-column: 1/-1;
    margin: 5px 0;
  }
  .comment__info {
    display: flex;
    justify-content: space-between;
  }
  .comment__input {
    display: grid;
    grid-template-columns: repeat(4,1fr);
    display: flex;
    justify-content: space-between;
    width: 100%;
  }
  .comment__reply {
    display: block;
  }
  #control__edit, #control__delete, .reply__btn {
    text-decoration: none;
    font-weight: 900;
    padding: 5px;
    background-color: #2c3e50;
    color: #d4d3d3;
    border-radius: 8px;
    border: 0;
    margin-left: 10px;
  }
  .btn {
    width: 30px;
    height: 30px;
    border-radius: 15px;
    border: none;
  }
</style>
  