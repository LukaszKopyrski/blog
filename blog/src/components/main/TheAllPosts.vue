<template>
  <section id="main__posts">
    <div v-for="post in posts" :key="post.id">
      <ThePost :post-id="post.id"></ThePost>
    </div>
    <TheAddPostBtn ></TheAddPostBtn>
    <TheEditPost :style="{ display: postStore.showComponent }" />
  </section>
</template>

<script setup>
import {ref, onMounted,watch} from "vue";
import api from '@/api';

import ThePost from "./ThePost.vue";
import TheAddPostBtn from "./TheAddPostBtn.vue";
import TheEditPost from "./TheEditPost.vue";

import { useTopicStore } from "@/store/topic.store";
import { usePostStore } from "@/store/post.store";

const posts = ref([]);

const topicStore = useTopicStore();
const postStore = usePostStore();


const getPosts=async()=>{
  let url = "/api/posts/";
  if(topicStore.selectedTopic?.topic){
    url = `/api/findposts/${topicStore.selectedTopic.topic}`;
  }

  try {
    const response = await api.get(url);
    posts.value = response.data;
  } catch (error) {
    console.error("Error fatching posts:",error);
  }
}

onMounted(()=>{getPosts();});

watch(
    ()=>postStore.isAddPost,
    async (newVal) =>{
        if(newVal){
            await getPosts();
            postStore.setIsAddPost(false);
        }
    }
);

watch(
    ()=>postStore.isTriggered,
    async (newVal) =>{
        if(newVal){
            await getPosts();
            postStore.setTriggered(false);
        }
    }
);

watch(
    ()=>topicStore.selectedTopic,
    async () =>{
        await getPosts();
    },
    {deep:true}
);

watch(
    ()=>postStore.isDeletingPost,
    async (newVal) =>{
        if(newVal){
            await getPosts();
            postStore.setDeletingPost(false);
        }
    }
);
</script>
