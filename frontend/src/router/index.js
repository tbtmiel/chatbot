import Vue from "vue";
import VueRouter from "vue-router";
import Answer from "../components/Answer.vue";
// import { component } from "vue/types/umd";
Vue.use(VueRouter);

const routes = [
    {
        path : '/',
        name : 'Answer',
        component : Answer,
    },
];

const router = new VueRouter({
    mode: "history",
    base: process.env.BASE_URL,
    routes,
  });
  
  export default router;