import { defineStore } from "pinia";

export const useCommentStore = defineStore("comment",{
    state:() =>({
        isEditingComment: false,
        commentId: null,
        isAddComment:false,
        isTriggered: false,
        isDeletingComment: false,
    }),
    actions:{
        setIsAddComment(value){
            this.isAddComment = value;
        },
        setEditComment(value, id=null){
            this.isEditingComment = value;
            this.commentId = value?id:null;
        },
        closeEdit(){
            this.isEditingComment = false;
            this.commentId = null;
        },
        setTriggered(value){
            this.isTriggered = value;
        },
        setDeletingComment(value){
            this.isDeletingComment = value;
        },
        setCommentId(id){
            this.commentId = id;
        }
    },
})