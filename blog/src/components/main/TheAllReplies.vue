<template>
    <section id="comment__replies">
        <div v-for="reply in replies" :key="reply.id">
            <TheReply :reply="reply" @edit-reply="startEditReply"></TheReply>
        </div>
        <form id="replies__form" @submit.prevent="addReply" v-if="!replyStore.isEditingReply && auth.isLoggedIn">
            <textarea id="form__input" rows="2" v-model="content"></textarea>
            <div v-if="validationError" class="error-message">{{ validationError }}</div>
            <button type="submit" id="replies__add">Add reply</button>
        </form>
        <form id="replies__edit" @submit.prevent="editReply" v-if="replyStore.isEditingReply && auth.isLoggedIn">
            <input type="button" id="form__close" value="X" @click="closePanel">
            <textarea id="form__input" rows="2" v-model="content"></textarea>
            <div v-if="validationError" class="error-message">{{ validationError }}</div>
            <button type="submit" id="replies__add">Edit reply</button>
        </form>
    </section>
</template>

<script setup>
import TheReply from "./TheReply.vue";

import {ref, onMounted,watch} from "vue";
import api from '@/api';
import { useAuthStore } from "@/store/auth.store";
import { useReplyStore } from "@/store/reply.store";

const props = defineProps({
    commentid:{
        type:[String,Number],
        required:true,
    },
});

const auth = useAuthStore();
const replyStore = useReplyStore();

const replies = ref([]);
const content = ref(""); 
const validationError = ref("");


const getReplies=async()=>{
    try {
        const response = await api.get(`/api/replies/${props.commentid}/`);
        replies.value = response.data;
    } catch (error) {
        console.log(error);
    }
}

const addReply=async()=>{
    try {
        await api.post(`/api/replies/${props.commentid}/`,{content:content.value});
        validationError.value = "";
        content.value = "";
        replyStore.setIsAddReply(true);
    } catch (error) {
        const responseData = error?.response?.data;
        if(responseData?.content){
            validationError.value = responseData.content[0];
        }else{
            validationError.value = "Error updating reply";
        }
        console.error("Error adding reply:",error);
    }
}

const editReply=async()=>{
    try {
        await api.patch(`/api/reply/${replyStore.replyId}/`,{content:content.value});
        validationError.value = "";
        content.value = "";
        replyStore.closeEdit();
        await getReplies();
    } catch (error) {
        const responseData = error?.response?.data;
        if(responseData?.content){
            validationError.value = responseData.content[0];
        }else{
            validationError.value = "Error updating reply";
        }
        console.error("Error updating reply:",error);
    }
}

const startEditReply=(replyId)=>{
    replyStore.setReplyId(replyId);
    replyStore.setEditReply(true);

    const reply = replies.value.find((item)=>item.id === replyId);
    if(reply){
        content.value = reply.content;
    }
}

const closePanel=()=>{
    replyStore.closeEdit();
    content.value = "";
    validationError.value = "";
}

onMounted(()=>{
    getReplies();
});

watch(
    ()=>replyStore.isTriggered,
    async (newVal) =>{
        if(newVal){
            await getReplies();
            replyStore.setTriggered(false);
        }
    }
);


watch(
    ()=>replyStore.isAddReply,
    async (newVal) =>{
        if(newVal){
            await getReplies();
            replyStore.setIsAddReply(false);
        }
    }
);

watch(
    ()=>replyStore.isEditingReply,
    async (newVal) =>{
        if(!newVal){
            await getReplies();
        }
    }
);

watch(
    ()=>replyStore.isDeletingReply,
    async (newVal) =>{
        if(newVal){
            await getReplies();
            replyStore.setDeletingReply(false);
        }
    }
);
</script>

<style scoped>
#form__close {
    width: 30px;
    height: 30px;
    border-radius: 15px;
    border: none;
}

#replies__form, #replies__edit {
    margin-top: 10px;
    width: 100%;
    display: flex;
    justify-content: center;
}

#form__input {
    width: 60%;
    resize: none;
    border-radius: 7px;
}

#replies__add {
    height: 30px;
    text-decoration: none;
    font-weight: 900;
    padding: 5px;
    background-color: #2c3e50;
    color: #d4d3d3;
    border-radius: 8px;
    border: 0;
}
</style>
