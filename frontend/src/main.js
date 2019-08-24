import Vue from 'vue'
import VueRouter from 'vue-router';
import App from './App.vue'

Vue.config.productionTip = false;

import 'bootstrap/dist/css/bootstrap.min.css';
import './assets/main.css';

// font-awesome stuff
import { library } from '@fortawesome/fontawesome-svg-core'
import { faUserSecret, faSpinner, faTrash } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add(faUserSecret, faSpinner, faTrash);

Vue.component('fa-icon', FontAwesomeIcon);

Vue.use(VueRouter);

// route components
import Home from "./views/Home";
import Debug from "./views/Debug";

const router = new VueRouter({
  mode: 'history',
  routes: [
    { path: '/', component: Home, name: "home" },
    { path: '/debug', component: Debug, name: "debug" }
  ]
});

new Vue({
  render: h => h(App),
  router
}).$mount('#app');
