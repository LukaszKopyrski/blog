<template>
    <div class="parent__addpost" v-if="auth.isLoggedIn">
        <button v-if="!isOpen" class="addpost" @click="show">Add post</button>
        <button v-else class="closepost" @click="hide">X</button>
        <TheAddPostPanel v-if="isOpen" class="addpost__panel" @close="hide" @created="hide"/>
    </div>
</template>

<script setup>
import {ref} from "vue"
import { useAuthStore} from "@/store/auth.store";
import TheAddPostPanel from "./TheAddPostPanel.vue";

const auth = useAuthStore();
const isOpen = ref(false);


const show=()=> isOpen.value=true;
const hide=()=> isOpen.value=false;
</script>

<style scoped>

.addpost__panel{
    justify-content: end;
    z-index: 9999;
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background-color: #c5c5c7;
    padding: 5px;
}
.closepost{
    width: 30px;
    height: 30px;
    border-radius: 15px;
    border: none;
    display: none;
}
.addpost{
    background-color: #2c3e50;
    padding: 5px;
    border-radius: 8px;
    color:  #d4d3d3;
    font-weight: 900;
    bottom: 55px;
    right: 30px;
    position: fixed;
    border-radius: 8px;
    border: 0;

}
</style>

