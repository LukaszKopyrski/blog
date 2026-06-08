<template>
    <h1 class="header__title" @click="resetTopic">Blog</h1>
  </template>
  
  <script setup>
  import { useTopicStore } from '@/store/topic.store';

  const topicStore = useTopicStore();

  const resetTopic=()=>{
    topicStore.setTopic(null);
  }
  </script>
  
  <style scoped>
  .header__title {
    margin-left: 5px;
    cursor: pointer; 
  }
  </style>
  