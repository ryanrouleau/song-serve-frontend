<template>
  <div id="app">
    <sidebar></sidebar>
  </div>
</template>

<script>
import Sidebar from './components/Sidebar.vue';

export default {
  name: 'app',

  components: {
    Sidebar
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
