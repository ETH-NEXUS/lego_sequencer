import Vue from 'vue'
import VueRouter from 'vue-router';
import App from './App.vue'

Vue.config.productionTip = false;

// bootstrap-vue
import BootstrapVue from 'bootstrap-vue'

Vue.use(BootstrapVue);

import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';
import './assets/main.css';
import './assets/modal-sidebar.css';

// font-awesome stuff
import { library } from '@fortawesome/fontawesome-svg-core'
import {
  faUserSecret, faSpinner, faTrash, faCircleNotch, faAngleDoubleDown, faQuestion, faSadCry, faExternalLinkAlt
} from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add(faUserSecret, faSpinner, faTrash, faCircleNotch, faAngleDoubleDown, faQuestion, faSadCry, faExternalLinkAlt);

Vue.component('fa-icon', FontAwesomeIcon);

Vue.use(VueRouter);

// route components
import Process from "./views/Process";
import Debug from "./views/Debug";
import Combined from "./views/Combined";

const router = new VueRouter({
  mode: 'history',
  routes: [
    { path: '/', component: Process, name: "home" },
    { path: '/debug', component: Debug, name: "debug" },
    { path: '/designer', component: Combined, name: "designer" },
  ]
});

new Vue({
  render: h => h(App),
  router
}).$mount('#app');
