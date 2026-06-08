<template>
   <div>
      <input type="text" placeholder="Search topic" class="search" v-model="searchInput">
      <div v-if="searchInput.length > 0">
         <ul>
            <li v-for="item in filteredSearch" :key="item.id" @click="selectTopic(item)">{{ item.topic }}</li>
         </ul>
      </div>
   </div>
</template>

<style scoped>
ul {
   list-style-type: none;
   margin-top: 10px;
}

li {
   cursor: pointer;
}
.search{
   border-radius: 8px;

}
</style>

<script setup>
import {ref, computed,onMounted} from "vue"
import { useTopicStore } from "@/store/topic.store";
import api from "@/api";

const topicStore = useTopicStore();

const searchInput = ref("");
const results = ref([]);


const fetchData = async()=>{
   try {
      const {data} = await api.get("/api/alltopics/");
      results.value = data;
   } catch (error) {
      console.error("Błąd ",error)
   }
}

const selectTopic = (topic)=>{
   topicStore.setTopic(topic)
}

const filteredSearch = computed(()=>{
   return results.value.filter(item=>
   item.topic.toLowerCase().includes(searchInput.value.toLowerCase())
   );
});

onMounted(()=>{
   fetchData();
});
</script>
