import axios from 'axios';

const BASE_URI = 'http://127.0.0.1:4433/';

const client = axios.create({
 baseURL: BASE_URI,
 json: true
});

class APIClient {
 constructor() {
   // this.accessToken = 0;
 }

 createKudo(songs) {
   return this.perform('post', '/api', songs);
 }

 deleteKudo(song) {
   return this.perform('delete', `/api/${song.id}`);
 }

 getKudos() {
   return this.perform('get', '/api');
 }

 async perform (method, resource, data) {
   return client({
     method,
     url: resource,
     data,
     // headers: {
     //   Authorization: `Bearer ${this.accessToken}`
     // }
   }).then(resp => {
     return resp.data ? resp.data : [];
   })
 }
}

export default APIClient;
