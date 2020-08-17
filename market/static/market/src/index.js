import { InertiaApp } from '@inertiajs/inertia-vue'
import Vue from 'vue'
import axios from "axios";

axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFToken";
axios.defaults.headers.common.accept = "application/json";

Vue.config.productionTip = true;

Vue.use(InertiaApp);

Vue.mixin({ methods: { route: window.reverseUrl } });

const app = document.getElementById('app');
const page = JSON.parse(document.getElementById("page").textContent);

import Index from "./Pages/Index";
import Login from "./Pages/Login";

const pages = {
  'Index': Index,
  'Login': Login,
}


new Vue({
  render: h => h(InertiaApp, {
    props: {
      initialPage: page,
      resolveComponent: (name) => {
//        console.log("resolveComponent ", name)
        return pages[name];
      },
    },
  }),
}).$mount(app)
