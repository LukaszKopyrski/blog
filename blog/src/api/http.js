import axios from 'axios';

export const http = axios.create({
    baseURL:'http://localhost:8000',
    withCredentials:true
});

let refreshing = false;

http.interceptors.response.use(
    response => response,

    async error =>{
        const req = error.config;

        const isAuth = req.url.includes("/api/login/") || req.url.includes("/api/register/") || req.url.includes("/api/refreshtoken/")
        if(error.response?.status===401 && !req._retry && !isAuth){
            req._retry=true;
            try {
                if(!refreshing){
                    refreshing = true;
                    await http.post("/api/refreshtoken/");
                    refreshing = false;
                }
                return http(req);
            } catch (error) {
                refreshing = false;
                console.log(`Expired refresh token`);
                return Promise.reject(error);
            }
        }
        return Promise.reject(error);
    }
);