import { defineStore } from "pinia";

export const usePostStore = defineStore("post",{
    state: () =>({
        showComponent:"none",
        isTriggered: false,
        isAddPost:false,
        postId:null,
        editPostData:null
    }),

    actions:{
        setShowComponent(value){
            this.showComponent = value;
        },
        setTriggered(value){
            this.isTriggered = value;
        },
        setIsAddPost(value){
            this.isAddPost = value;
        },
        setPostId(id){
            this.postId=id;
        },
        setEditPostData(post){
            this.editPostData = post;
        },
        openEdit(post){
            this.postId = post.id;
            this.editPostData = {
                title:post.title,
                topic:post.topic,
                content:post.content,
            };
            this.showComponent = "flex";
        },
        closeEdit(){
            this.showComponent = "none";
            this.postId = null;
            this.editPostData = null;
        }
    },
})