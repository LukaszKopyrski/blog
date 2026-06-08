import { defineStore } from "pinia";

export const useTopicStore = defineStore("topic",{
    state:()=>({
        selectedTopic:null
    }),
    actions:{
        setTopic(topic){
            this.selectedTopic = topic;
        },
        clearTopic(){
            this.selectedTopic = null;
        }
    }
});