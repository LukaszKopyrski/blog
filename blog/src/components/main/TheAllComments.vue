<template>
    <section class="post__comments">
        <div v-for="comment in comments" :key="comment.id">
            <TheComment :comment="comment" @edit-comment="startEditComment"></TheComment>
        </div>
        <form class="comments__form" @submit.prevent="addComment" v-if="!commentStore.isEditingComment && auth.isLoggedIn">
            <textarea class="form__input" rows="2" v-model="content"></textarea>
            <div v-if="validationError" class="error-message">{{ validationError }}</div>
            <button type="submit" class="comments__add">Add comment</button>
        </form>
        <form class="comments__edit" @submit.prevent="editComment" v-if="commentStore.isEditingComment && auth.isLoggedIn">
            <input type="button" class="form__close" value="X" @click="closePanel">
            <textarea class="form__input" rows="2" v-model="content"></textarea>
            <div v-if="validationError" class="error-message">{{ validationError }}</div>
            <button type="submit" class="comments__add">Edit comment</button>
        </form>
    </section>
</template>

<script setup>
import {ref, onMounted,watch} from "vue";
import TheComment from './TheComment.vue';
import api from '@/api';
import { useAuthStore } from "@/store/auth.store";
import {useCommentStore} from "@/store/comment.store";

const props = defineProps({
    postid:{
        type: [String,Number],
        required: true,
    },
});


const auth = useAuthStore();
const commentStore = useCommentStore();

const comments = ref([]);
const content = ref(""); 
const validationError = ref("");


const getComments=async()=>{
    try {
        const response = await api.get(`/api/comments/${props.postid}/`);
        comments.value = response.data
    } catch (error) {
        console.log(error);
    }
}

const addComment=async()=>{
    try {
        await api.post(`/api/comments/${props.postid}/`,{content:content.value});
        validationError.value = "";
        content.value = "";
        commentStore.setIsAddComment(true);
    } catch (error) {
        const responseData = error?.response?.data;
        if(responseData?.comment){
            validationError.value = responseData.content[0];
        }else{
            validationError.value = "Error adding comment";
        }
        console.error("Error adding comment:",error);
    }
}

const editComment=async()=>{
    try {
        await api.patch(`/api/comment/${commentStore.commentId}/`,{content:content.value});
        validationError.value = "";
        content.value = "";
        commentStore.closeEdit();
        await getComments();
    } catch (error) {
        const responseData = error?.response?.data;
        if(responseData?.comment){
            validationError.value = responseData.content[0];
        }else{
            validationError.value = "Error updating comment";
        }
        console.error("Error updating comment:",error);
    }
}


const startEditComment=(commentId)=>{
    commentStore.setEditComment(true, commentId);

    const comment = comments.value.find((item)=>item.id === commentId);
    if(comment){
        content.value = comment.content;
    }
}


const closePanel=()=>{
    commentStore.closeEdit();
    content.value = "";
    validationError.value = "";
}

onMounted(()=>{
    getComments();
});

watch(
    ()=>commentStore.isAddComment,
    async (newVal)=>{
        if(newVal){
            await getComments();
            commentStore.setIsAddComment(false);
        }
    }
)


watch(
    ()=>commentStore.isTriggered,
    async (newVal) =>{
        if(newVal){
            await getComments();
            commentStore.setTriggered(false);
        }
    }
);

watch(
    ()=>commentStore.isEditingComment,
    async (newVal) =>{
        if(!newVal){
            await getComments();
        }
    }
);

watch(
    ()=>commentStore.isDeletingComment,
    async (newVal) =>{
        if(newVal){
            await getComments();
            commentStore.setDeletingComment(false);
        }
    }
);
</script>

<style scoped>
.form__close {
    width: 30px;
    height: 30px;
    border-radius: 15px;
    border: none;
}

.comments__form, .comments__edit {
    margin-top: 10px;
    width: 100%;
    display: flex;
    justify-content: center;
}

.form__input {
    width: 60%;
    resize: none;
    border-radius: 7px;
}

.comments__add {
    height: 30px;
    text-decoration: none;
    font-weight: 900;
    padding: 5px;
    background-color: #2c3e50;
    color: #d4d3d3;
    border-radius: 8px;
    border: 0;
}

.error-message {
    color: red;
    font-weight: bold;
    text-align: center;
    margin-bottom: 10px;
}
</style>
