<template>
    <article id="replies__reply">
        <div class="reply__info">
            <span class="info__author">{{ localReply.username }}</span>
            <span class="info__date">{{ localReply.date }}</span>
        </div>
        <div class="reply__main">
            <p class="main__content">{{ localReply.content }}</p>
        </div>
        <div class="reply__input">
            <span class="input__score">
                <button class="btn score__plus" @click="addScore" v-if="!checkScore() && auth.isLoggedIn">+</button>
                {{ localReply.score }}
                <button class="btn score__minus" @click="deleteScore" v-if="checkScore() && auth.isLoggedIn">-</button>
            </span>
            <div class="input__control">
                <button id="control__edit" v-if="localReply.is_author && auth.isLoggedIn" @click="editReply">Edit</button>
                <button id="control__delete" v-if="(localReply.is_staff || localReply.is_author) && auth.isLoggedIn" @click="deleteReply">Delete</button>
            </div>
        </div>
    </article>
</template>

<script setup>
import {ref, watch} from "vue";
import api from "@/api";
import { useAuthStore } from "@/store/auth.store";
import { useReplyStore } from "@/store/reply.store";

const props = defineProps({
    reply:{
        type:Object,
        required:true,
    },
});
const emit = defineEmits(["edit-reply"]);
const auth = useAuthStore();
const replyStore = useReplyStore();

const localReply = ref({...props.reply});

watch(
    ()=>props.reply,
    (newReply) =>{
        localReply.value = {...newReply};
    },
    {deep:true}
);

const editReply =()=>{
    replyStore.setEditReply(true);
    replyStore.setReplyId(localReply.value.id);
    emit("edit-reply",localReply.value.id);
}

const getReply=async()=>{
    try {
        const response = await api.get(`/api/reply/${localReply.value.id}/`);
        localReply.value = response.data;
    } catch (error) {
        console.error("Error fetching reply:",error);
    }
}

const checkScore=()=>{
    return localReply.value?.scores?.some((score)=>score.username===auth.username);
}

const addScore=async()=>{
  try {
    await api.post(`/api/addreplyscore/${localReply.value.id}/`);
    await getReply();
  } catch (error) {
    console.error("Error adding score:",error);
  }
}

const deleteScore=async()=>{
    try {
        await api.delete(`/api/deletereplyscore/${localReply.value.id}/${auth.username}/`);
        await getReply();
    } catch (error) {
        console.error("Error deleting score:",error);
    }
}

const deleteReply=async()=>{
    try {
        await api.delete(`/api/reply/${localReply.value.id}/`);
        replyStore.setDeletingReply(true);
    } catch (error) {
        console.error("Error reply:",error);
    }
}
</script>

<style scoped>
#replies__reply {
    background-color: #b4b6b6;
    grid-column: 1/-1;
    margin: 5px 0;
}

.reply__info {
    display: flex;
    justify-content: space-between;
}

.reply__input {
    display: flex;
    justify-content: space-between;
}

#control__edit, #control__delete {
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
