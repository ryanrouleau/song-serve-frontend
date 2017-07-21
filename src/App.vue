<template>
  <div id="app">
    <sidebar></sidebar>
    <main-view></main-view>
  </div>
</template>

<script>
import Sidebar from './components/Sidebar.vue';
import MainView from './components/MainView.vue';

export default {
  name: 'app',

  components: {
    Sidebar,
    MainView
  },

  data () {
    return {
    }
  }
}
</script>

<style lang="scss">
#app {
  height: 100%;
  width: 100%;
}
</style>
