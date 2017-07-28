import Vue from 'vue';
import App from './App.vue';
import VueLazyload from 'vue-lazyload'

import './assets/css/global.css';

Vue.use(VueLazyload, {
  listenEvents: [ 'scroll' ]
});

new Vue({
  el: '#app',
  render: h => h(App)
});
