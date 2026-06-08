import { http } from "./http";

export const authService = {
    async login(payload){
        await http.post('/api/login/',payload)
    },
    async myaccount(){
        const {data} = await http.get('/api/myaccount/');
        return data;
    },
    async logout(){
        await http.post('/api/logout/',{})
    }
}