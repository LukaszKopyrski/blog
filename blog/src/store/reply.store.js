import { defineStore } from "pinia";

export const useReplyStore = defineStore("reply",{
    state:() =>({
        isEditingReply: false,
        replyId: null,
        isAddReply:false,
        isTriggered: false,
        isDeletingReply: false,
    }),
    actions:{
        setIsAddReply(value){
            this.isAddReply = value;
        },
        setEditReply(value){
            this.isEditingReply = value;
            if(!value){
                this.replyId = null;
            }
        },
        setReplyId(id){
            this.replyId = id;
        },
        setDeletingReply(value){
            this.isDeletingReply = value;
        },
        setTriggered(value){
            this.isTriggered = value;
        },
        closeEdit(){
            this.isEditingReply = false;
            this.replyId = null;
        },
    },
});